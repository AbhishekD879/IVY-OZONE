import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import switch_to_main_page, normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod # QD will open for some users on beta/prod
@pytest.mark.high
@pytest.mark.quick_bet
@pytest.mark.quick_deposit
@pytest.mark.mobile_only
@pytest.mark.login
@pytest.mark.numeric_keyboard
@vtest
class Test_C23820446_Vanilla_Quick_Bet_Verify_entering_CVV_and_Amount_value(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C23820446
    VOL_ID: C34792792
    NAME: [Vanilla]- Quick Bet - Verify entering 'CVV' and 'Amount' value
    DESCRIPTION: This test case verifies entering stake value in a 'CVV' and 'Amount' fields using numeric keyboard for Quick Deposit within Quick Bet
    """
    keep_browser_open = True
    cvv = tests.settings.visa_card_cvv

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Application is loaded
        DESCRIPTION: 2. Log in under user account with positive balance
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         expected_template_market=vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting)
            event = choice(events)
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            market_name = next((market['market']['name'] for market in event['event']['children']
                                if vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting in market['market']['templateMarketName']), '')
            if not market_name:
                raise SiteServeException(f'There is no market name in event with id: "{self.eventID}"')
            market_name = normalize_name(market_name)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
            self.__class__.eventID = event_params.event_id
            market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result
        self._logger.info(f'*** Using event "{self.eventID}" with market {market_name}')

        self._logger.info(f'*** Using event id "{self.eventID}" and market name "{market_name}"')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        username = tests.settings.quick_deposit_user
        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance
        self.site.wait_content_state('HomePage')

    def test_001_select_one_sportraces_selection(self):
        """
        DESCRIPTION: Select one <Sport>/<Races> selection
        EXPECTED: * Quick Bet is opened
        EXPECTED: * Added selection is displayed
        EXPECTED: * Numeric keyboard is collapsed by default
        """
        self.navigate_to_edp(self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.assertEqual(self.quick_bet.content.event_name, self.event_name,
                         msg=f'Actual event name "{self.quick_bet.content.event_name}" does not match '
                             f'expected "{self.event_name}"')
        self.assertFalse(self.site.quick_bet_panel.keyboard.is_displayed(name='Numeric keyboard not shown', timeout=3,
                                                                         expected_result=False),
                         msg='Numeric keyboard is not collapsed by default.')

    def test_002_enter_higher_than_user_balance_stake_and_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Enter higher than user balance stake and tap on 'Make a Deposit' button
        EXPECTED: * Quick Deposit iFrame appears
        EXPECTED: * Numeric keyboard is not shown
        EXPECTED: * 'CVV' field is empty by default
        EXPECTED: * 'Deposit Amount' field is pre-populated with amount with the difference from the balance and stake
        EXPECTED: * '-' and '+' buttons are displayed on both sides of deposit amount input field
        EXPECTED: * 'Quick Stakes' buttons are displayed below 'Deposit Amount' and 'CVV' fields
        """
        self.__class__.over_balance = 1.0
        stake = self.user_balance + self.over_balance
        self.quick_bet.content.amount_form.input.value = stake
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        sleep(10)

        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" section is not shown')
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.assertFalse(self.quick_deposit.has_keyboard(expected_result=False, timeout=3),
                         msg='Numeric keyboard is shown')

        self.__class__.cvv2 = self.quick_deposit.cvv_2
        self.site.wait_content_state_changed()
        self.assertTrue(self.cvv2.is_displayed(), msg='CVV2 field is not displayed.')
        current_cvv = self.cvv2.input.value
        self.assertEqual(current_cvv, '', msg=f'CVV field is not empty by default. Actual result "{current_cvv}"')

    def test_003_focus_cvv_field(self):
        """
        DESCRIPTION: Focus 'CVV' field
        EXPECTED: * 'CVV' field is focused
        EXPECTED: * 'DEPOSIT AND PLACE BET' button is disabled
        """
        self.cvv2.perform_click()
        self.assertTrue(self.cvv2.is_focused(), msg='CVV field is not in focus.')
        self.__class__.keyboard = self.quick_deposit.keyboard
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')

        self.__class__.deposit_button = self.quick_deposit.deposit_and_place_bet_button
        self.assertTrue(self.deposit_button.is_displayed(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not present')
        self.assertFalse(self.deposit_button.is_enabled(expected_result=False),
                         msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is enabled')
        self.assertEqual(self.deposit_button.name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name: "{self.deposit_button.name}"'
                             f'is not equal to expected: "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')

    def test_004_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: * Entered numbers are displayed in the 'CVV' field
        EXPECTED: * 'DEPOSIT AND PLACE BET' button is disabled (becomes enabled when 3 digits are entered)
        """
        self.keyboard.enter_amount_using_keyboard(value=self.cvv)
        self.assertEqual(self.cvv2.input.value, self.cvv,
                         msg=f'CVV field value is not "{self.cvv}". CVV value is "{self.cvv2.input.value}" instead.')
        self.assertTrue(self.deposit_button.is_enabled(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled.')

    def test_005_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'CVV' field
        """
        self.keyboard.enter_amount_using_keyboard(value='delete')
        current_cvv = self.cvv2.input.value
        self.assertEqual(current_cvv, self.cvv[:-1],
                         msg=f'Last digit was not erased from CVV field. '
                             f'Actual result {current_cvv}, expected "{self.cvv[:-1]}"', )

    def test_006_tap_any_quick_stake_button_20_50_100_200(self):
        """
        DESCRIPTION: Tap any Quick Stake button
        DESCRIPTION: * 20
        DESCRIPTION: * 50
        DESCRIPTION: * 100
        DESCRIPTION: * 200
        EXPECTED: * Value in 'Deposit Amount' field is displayed according to chosen Quick Stake button value
        """
        self.__class__.amount = self.quick_deposit.amount
        quick_stake_buttons = self.quick_deposit.quick_stake_panel.items_as_ordered_dict
        self.assertTrue(quick_stake_buttons, msg='Quick stake buttons not found.')
        button_20 = next((button for name, button in quick_stake_buttons.items() if '20' in name), None)
        self.assertTrue(button_20, msg=f'Quick stake button 20 is not present in "{quick_stake_buttons.keys()}"')
        button_20.click()
        expected_amount = '20.00'
        actual_amount = self.amount.input.value
        self.assertEqual(expected_amount, actual_amount,
                         msg=f'Amount equals "{actual_amount}", while expected amount is "{expected_amount}"')

    def test_007_tap_plus_button_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '+' button near the deposit amount input field
        EXPECTED: * The deposit amount is increased by value from Deposit amount box (user currency)
        """
        # Clicking on quick deposit header as plus button is not clicked from first attempt otherwise
        switch_to_main_page()
        self.quick_deposit.header.click()
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.quick_deposit.plus_button.click()
        expected_amount = '40.00'
        actual_amount = self.amount.input.value
        self.assertEqual(expected_amount, actual_amount,
                         msg=f'Amount equals "{actual_amount}", while expected amount is "{expected_amount}"')

    def test_008_focus_deposit_amount_field(self):
        """
        DESCRIPTION: Focus 'Deposit Amount' field
        EXPECTED: * 'Deposit Amount' field is focused
        EXPECTED: * Numeric keyboard is opened
        """
        # Wait for amount to be clickable as click is intercepted otherwise
        self.assertTrue(self.amount.is_displayed(timeout=0.5),
                        msg='Amount field is not displayed')
        self.amount.perform_click()
        self.assertTrue(self.amount.is_focused(),
                        msg='Amount field is not in focus.')
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')

    def test_009_tap_button_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '-' button near the deposit amount input field
        EXPECTED: * The deposit amount is decreased by value from Deposit amount box (user currency)
        """
        self.assertTrue(self.quick_deposit.minus_button.is_enabled(timeout=2), msg='Minus button is not enabled.')
        self.quick_deposit.minus_button.click()
        expected_amount = '20.00'
        actual_amount = self.amount.input.value
        self.assertEqual(expected_amount, actual_amount,
                         msg=f'Amount equals "{actual_amount}", while expected amount is "{expected_amount}"')
        switch_to_main_page()
        self.quick_deposit.header.click()
        self.assertFalse(self.keyboard.is_displayed(name='Numeric keyboard not shown', timeout=3, expected_result=False),
                         msg='Numeric keyboard is shown')

        self.assertTrue(self.quick_deposit.close_button.is_enabled(),
                        msg='Quick deposit panel close button is not enabled.')
        self.quick_deposit.close_button.click()
        self.assertTrue(self.site.quick_bet_panel.header.close_button.is_enabled(),
                        msg='Quick bet panel close button is not enabled.')
        self.site.quick_bet_panel.close()
        self.site.wait_quick_bet_overlay_to_hide()
        self.site.logout()

    def test_010_log_in_and_repeat_steps_1_9_for_all_currencies_gbpusd_eur(self):
        """
        DESCRIPTION: Log in and repeat steps #1-9 for all currencies ('GBP','USD', 'EUR')
        EXPECTED: Results are the same
        """
        users = [tests.settings.user_with_usd_currency_and_card,
                 tests.settings.user_with_euro_currency_and_card]

        for username in users:
            self.site.login(username=username)
            self.__class__.user_balance = self.site.header.user_balance
            self.site.open_betslip()
            self.clear_betslip()
            self.test_001_select_one_sportraces_selection()
            self.test_002_enter_higher_than_user_balance_stake_and_tap_on_make_a_deposit_button()
            self.test_003_focus_cvv_field()
            self.test_004_enter_numeric_values()
            self.test_005_tap_remove_button_on_numeric_keyboard()
            self.test_006_tap_any_quick_stake_button_20_50_100_200()
            self.test_007_tap_plus_button_near_the_deposit_amount_input_field()
            self.test_008_focus_deposit_amount_field()
            self.test_009_tap_button_near_the_deposit_amount_input_field()
