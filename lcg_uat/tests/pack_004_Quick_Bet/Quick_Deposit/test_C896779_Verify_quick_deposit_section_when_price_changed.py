import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.numeric_keyboard
@pytest.mark.bet_placement
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C896779_Verify_Quick_Deposit_section_when_price_for_bet_is_changed(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C896779
    VOL_ID: C9698034
    NAME: Verify Quick Deposit section when price for bet is changed
    DESCRIPTION: This test case verifies Quick Deposit section when price for bet is changed
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in, has 0 or very low balance
    PRECONDITIONS: * Users have the payment cards added to his account
    PRECONDITIONS: * Open OpenBet TI tool for price changing:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True
    new_price = '4/5'
    new_price_2 = '1/5'

    username_visa = None
    bet_amount = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as user with balance at least 100 pounds. Tap Right menu icon
        DESCRIPTION: Create event
        EXPECTED: User is logged in with 100 pounds
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        self.__class__.username_visa = tests.settings.quick_deposit_user

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids, self.__class__.event_id = \
            event_params.team1, event_params.team2, event_params.selection_ids, event_params.event_id
        self.__class__.event_name = f'{self.team1} v {self.team2}'

    def test_001_load_oxygen_app_and_login_under_user_from_preconditions(self):
        """
        DESCRIPTION: Load Oxygen app and login under user from preconditions
        """
        self.site.login(username=self.username_visa)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        self.navigate_to_edp(event_id=self.event_id)

        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='No markets found')

        section = markets_list.get(self.expected_market_sections.match_result)
        self.assertTrue(section, msg=f'"{self.expected_market_sections.match_result}" section is not found in "{markets_list.keys()}"')

        output_prices_list = section.outcomes.items_as_ordered_dict
        self.assertTrue(output_prices_list, msg='Match result output prices were not found on Event Details page')

        team_name = self.team1.upper() if self.brand == 'ladbrokes' else self.team1
        output_prices_list[team_name].bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Please deposit a min <currency symbol>XX.XX to continue placing your bet' error message is displayed on red background below 'QUICK BET' header
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: * Buttons 'ADD TO BETSLIP' and 'MAKE A DEPOSIT' are enabled
        """
        self.__class__.over_balance = 10
        self.__class__.bet_amount = self.user_balance + self.over_balance

        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        result = self.site.quick_bet_panel.wait_for_quick_bet_info_panel() if self.brand == 'bma' \
            else self.site.quick_bet_panel.wait_for_deposit_info_panel()
        self.assertTrue(result, msg='Quick Bet Info Panel is not present')

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance)
        if self.brand == 'ladbrokes':
            actual_message = self.site.quick_bet_panel.deposit_info_message.text
        else:
            actual_message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO BETSLIP" button is disabled')
        self.assertTrue(self.site.quick_bet_panel.make_quick_deposit_button.is_enabled(),
                        msg='"MAKE A DEPOSIT" button is disabled')

    def test_004_change_price_in_backoffice_ti_and_save_changes(self):
        """
        DESCRIPTION: Change price in Backoffice TI and save changes
        EXPECTED: * Price is updated
        """
        selection_id = self.selection_ids[self.team1]
        self.__class__.old_price = self.site.quick_bet_panel.selection.content.odds_value

        self.ob_config.change_price(selection_id, self.new_price)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=selection_id, price=self.new_price)
        self.assertTrue(price_update, msg=f'Price update for selection id "{selection_id}" is not received')

    def test_005_check_quick_bet_displaying(self):
        """
        DESCRIPTION: Check Quick Bet displaying
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: * For Horse Racing Old Odds are absent and New Odds are present
        EXPECTED: * Est. Returns is recalculated
        """
        self.site.quick_bet_panel.wait_for_message_to_change(
            previous_message=vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance))
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=True),
                        msg='Quick Bet Info Panel is not present')

        expected_message = vec.quickbet.PRICE_IS_CHANGED. \
            format(old=self.old_price, new=self.new_price)
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns, odds=[self.new_price], bet_amount=self.bet_amount)

    def test_006_click_on_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Click on 'MAKE A QUICK DEPOSIT' button
        EXPECTED: * Quick Deposit section is opened
        EXPECTED: * Warning Message on yellow background is not shown
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" section is not shown')
        quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.assertTrue(quick_deposit.deposit_and_place_bet_button,
                        msg='"DEPOSIT & PLACE BET" buttons is not present')
        self.assertFalse(quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False),
                         msg='"DEPOSIT & PLACE BET" buttons is not disabled by default')
        switch_to_main_page()
        self.assertFalse(self.site.quick_bet_panel.quick_deposit_panel.wait_for_quick_deposit_info_panel(expected_result=False),
                         msg='Warning Message on yellow background is shown')

    def test_007_change_price_in_backoffice_ti_and_check_quick_deposit_section(self):
        """
        DESCRIPTION: Change price in Backoffice TI and check Quick Deposit section
        EXPECTED: * Warning Message on yellow background appears message with text: 'Some of your prices have changed'
        """
        selection_id = self.selection_ids[self.team1]
        self.ob_config.change_price(selection_id, self.new_price_2)

        self.site.quick_bet_panel.quick_deposit_panel.wait_for_message_to_change(
            previous_message=vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance))

        expected_message = vec.quickbet.PRICE_IS_CHANGED. \
            format(old=self.new_price, new=self.new_price_2)
        message = self.site.quick_bet_panel.quick_deposit_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

    def test_008_tap_on_close_x_button(self):
        """
        DESCRIPTION: Tap on close (X) button
        """
        self.site.quick_bet_panel.quick_deposit_panel.close_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='"Quick Bet" section is not shown')

    def test_009_tap_make_a_quick_deposit_button_and_change_price_in_backoffice_ti(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button and change price in Backoffice TI
        EXPECTED: * Warning Message on yellow background appears 'Some of your prices have changed'
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()

        selection_id = self.selection_ids[self.team1]
        self.ob_config.change_price(selection_id, self.new_price)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=selection_id, price=self.new_price)
        self.assertTrue(price_update, msg=f'Price update for selection id "{selection_id}" is not received')

        self.site.quick_bet_panel.quick_deposit_panel.wait_for_message_to_change(
            previous_message=vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance))

        expected_message = vec.quickbet.PRICE_IS_CHANGED. \
            format(old=self.new_price_2, new=self.new_price)
        message = self.site.quick_bet_panel.quick_deposit_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

    def test_010_make_a_successful_deposit_and_check_bet_is_placed(self):
        """
        DESCRIPTION: Make a successful deposit and check bet is placed
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown to user with new price and recalculated  Total Est. Returns
        """
        quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        quick_deposit.cvv_2.click()

        keyboard = quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv, delay=0.7)
        keyboard.enter_amount_using_keyboard(value='enter')

        deposit_button = quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_displayed(expected_result=True),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not displayed')
        deposit_button.click()
        switch_to_main_page()

        self.site.close_all_dialogs(async_close=False, timeout=10)

        actual_balance = str(self.site.header.user_balance)
        expected_balance = '0.0'
        self.assertEqual(actual_balance, expected_balance,
                         msg=f'Actual amount "{actual_balance}" does not match expected "{expected_balance}"')

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed(timeout=5)
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
