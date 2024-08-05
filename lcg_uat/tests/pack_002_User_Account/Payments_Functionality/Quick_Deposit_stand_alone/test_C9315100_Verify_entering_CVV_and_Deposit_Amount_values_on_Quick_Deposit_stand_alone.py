import pytest
import voltron.environments.constants as vec
import tests
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name, switch_to_main_page
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.mobile_only
@pytest.mark.quick_deposit
@vtest
class Test_C9315100_Verify_entering_CVV_and_Deposit_Amount_values_on_Quick_Deposit_stand_alone(BaseBetSlipTest,
                                                                                               BaseSportTest):
    """
    TR_ID: C9315100
    VOL_ID: C16706458
    NAME: Verify entering 'CVV' and 'Deposit Amount' values on 'Quick Deposit' stand alone
    DESCRIPTION: This test case verifies entering stake value in a 'CVV' and 'Deposit Amount' fields using numeric keyboard for 'Quick Deposit' stand alone
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile: C16706458
    """
    keep_browser_open = True
    device_name = 'Nexus 5X' if not tests.use_browser_stack else tests.default_pixel
    valid_cvv = "123"
    deposit_amount = "5.00"
    invalid_cvv = "1234"
    cvv = tests.settings.visa_card_cvv

    def clear_input_using_keyboard(self, value=None, on_betslip=True):
        keyboard = self.site.quick_deposit_panel.keyboard if on_betslip \
            else self.quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        value = len(str(value)) if value else self.max_number_of_symbols_in_stake_input
        for i in range(0, value):
            keyboard.enter_amount_using_keyboard(value='delete')

    def test_000_preconditions(self, user=None):
        """
        PRECONDITIONS: 1. Application is loaded
        PRECONDITIONS: 2. User with credit cards added is logged into an app
        PRECONDITIONS: 3. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         expected_template_market=vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting)
            event = choice(events)
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            market_name = next((market['market']['name'] for market in event['event']['children']
                                if vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting in market['market'][
                                    'templateMarketName']), '')
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
        user = tests.settings.quick_deposit_user if user is None else user
        self.site.login(username=user)
        self.site.wait_content_state('HomePage')
        betslip_counter = self.get_betslip_counter_value()
        if int(betslip_counter) != 0:
            self.site.open_betslip()
            self.site.betslip.remove_all_button.click()
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
            dialog.continue_button.click()
        user_balance = self.site.header.user_balance
        self.navigate_to_edp(self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        over_balance = user_balance + 5
        self.site.quick_bet_panel.selection.content.amount_form.input.click()
        self.site.quick_bet_panel.keyboard.enter_amount_using_keyboard(value=over_balance)

    def test_001_set_focus_on_cvv_field(self):
        """
        DESCRIPTION: Set focus on 'CVV' field
        EXPECTED: - 'CVV' field is focused
        EXPECTED: - Numeric keyboard is opened with '.' button disabled
        EXPECTED: - 'Quick Stakes' are not displayed
        EXPECTED: - 'Deposit' button is disabled
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" section is not shown')
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.quick_deposit.cvv_2.click()
        self.assertTrue(self.quick_deposit.keyboard.is_displayed(),
                        msg='Numeric keyboard on quick deposit is not present')
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False),
                         msg='"Deposit button is not disabled"')

    def test_002_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: - Entered numbers are displayed in the 'CVV' field
        EXPECTED: - 'Deposit' button is enabled
        """
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value=self.valid_cvv)
        self.assertEquals(self.quick_deposit.cvv_2.input.value, self.valid_cvv,
                          msg='Entered numbers are not displayed in CVV field')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg='"Deposit" button is disabled"')

    def test_003_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: Last entered symbol is deleted from 'CVV' field
        """
        self.clear_input_using_keyboard(value=self.valid_cvv, on_betslip=False)
        expected_clear_cvv = ""
        self.assertEquals(self.quick_deposit.cvv_2.input.value, expected_clear_cvv,
                          msg=f'Last entered CVV: "{self.valid_cvv}" is not deleted.'
                              f'Actual: "{self.quick_deposit.cvv_2.input.value}", Expected: "{expected_clear_cvv}"')

    def test_004_enter_value_more_than_max_allowed_value_in_cvv_field(self):
        """
        DESCRIPTION: Enter value more than max allowed value in 'CVV' field
        EXPECTED: It is impossible to enter more than 3 digits in 'CVV' field
        """
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value=self.invalid_cvv)
        result = wait_for_result(lambda: str(self.quick_deposit.cvv_2.input.value) != str(self.invalid_cvv),
                                 name='Extra CVV symbol to remove',
                                 timeout=2)
        self.assertTrue(result, msg=f'It is impossible to enter more than 3 digit CVV:'
                                    f'Actual: "{self.quick_deposit.cvv_2.input.value}" Expected: "{self.invalid_cvv}')
        self.assertEquals(len(self.quick_deposit.cvv_2.input.value), 3,
                          msg='"CVV" field has more than 3 digits')

    def test_005_set_focus_on_deposit_amount_field(self):
        """
        DESCRIPTION: Set focus on 'Deposit Amount' field
        EXPECTED: - Numeric keyboard remains opened without Quick Stakes buttons
        EXPECTED: - 'CVV' field is unfocused
        EXPECTED: - 'Deposit Amount' field is focused
        EXPECTED: -  '.' button becomes enabled
        """
        self.quick_deposit.amount.click()
        self.assertTrue(self.quick_deposit.keyboard.is_enabled(),
                        msg='Numeric keyboard is not opened')
        self.assertTrue(self.quick_deposit.quick_stake_panel, msg='Quick stakes buttons are not displayed')
        self.assertTrue(self.quick_deposit.amount.is_enabled(),
                        msg='"Deposit Amount" field is not focused')

    def test_006_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: - Entered numbers are displayed in the 'Deposit Amount' field
        EXPECTED: - 'Deposit' button becomes enabled once input is equal or higher than '0.01'
        """
        min_amount = "0.01"
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value=self.deposit_amount)
        self.assertEquals(self.quick_deposit.amount.input.value, self.deposit_amount,
                          msg=f'Entered numbers are not displayed in "Deposit Amount" field.'
                              f'Actual: "{self.quick_deposit.amount.input.value}" Expected: "{self.deposit_amount}"')
        self.assertGreater(self.deposit_amount, min_amount,
                           msg=f'Deposit amount "{self.deposit_amount}" is not higher than minimum amount "{min_amount}"')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg='"Deposit button is not enabled"')

    def test_007_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: - Last entered symbol is deleted from 'Deposit Amount' field
        """
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
        self.assertNotEquals(self.quick_deposit.amount.input.value, self.deposit_amount,
                             msg=f'Last entered symbol: "{self.deposit_amount}" is not deleted')
        self.clear_input_using_keyboard(on_betslip=False)

    def test_008_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: - 'Amount' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        EXPECTED: - '.' button becomes greyed out (disabled) on keyboard
        """
        # NA

    def test_009_enter_value_more_than_max_allowed_value_in_amount_field(self):
        """
        DESCRIPTION: Enter value more than max allowed value in 'Amount' field
        EXPECTED: It is impossible to enter more than 7 digits and 2 decimal: e.g. "XXXXXXX.XX"
        """
        max_amount = "12345678.123"
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value=max_amount)
        expected_amount = "12345678.12"
        self.assertEquals(self.quick_deposit.amount.input.value, expected_amount,
                          msg=f'It is impossible to enter more than 7 digits'
                              f'Actual: "{self.quick_deposit.amount.input.value}", Expected: "{expected_amount}"')

    def test_010_set_cursor_anywhere_within_the_quick_deposit_section__tap_return_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: - Set cursor anywhere within the 'Quick Deposit' section
        DESCRIPTION: or
        DESCRIPTION: - Tap 'Enter' button on numeric keyboard
        EXPECTED: - 'Deposit Amount' field is NOT focused
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - All fields remain populated
        """
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        self.assertFalse(self.quick_deposit.amount.is_selected(),
                         msg='"Deposit Amount" field is focused')
        self.assertFalse(self.quick_deposit.has_keyboard(),
                         msg='Numeric keyboard is shown')
        self.assertTrue(self.quick_deposit.cvv_2.is_displayed(), msg='"CVV" field is not populated')

    def test_011_set_cursor_over_deposit_amount_field_again(self, currency='£'):
        """
        DESCRIPTION: Tap within the 'Deposit Amount' field again
        EXPECTED: - Selected field is focused
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: - Quick Stakes buttons are NOT shown on keyboard
        EXPECTED: - '<currency symbol> amount value' remains shown within 'Deposit Amount' field
        EXPECTED: - When user enters new value > new value is shown instead of an old one
        EXPECTED: - When user taps 'Remove' on keyboard > each digit is removed one by one
        """
        self.quick_deposit.amount.click()
        self.clear_input_using_keyboard(on_betslip=False)
        self.assertTrue(self.quick_deposit.amount.is_enabled(),
                        msg='"Deposit Amount" field is not focused')
        self.assertTrue(self.quick_deposit.keyboard.is_enabled(),
                        msg='Numeric keyboard is shown')
        self.assertTrue(self.quick_deposit.quick_stake_panel, msg='Quick stakes buttons are not displayed')
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value=self.deposit_amount)
        self.assertEquals(self.quick_deposit.amount.input.value, self.deposit_amount,
                          msg=f'New value is not entered in "Deposit Amount" field'
                              f'Actual: "{self.quick_deposit.amount.input.value}", Expected: "{self.deposit_amount}"')
        actual_currency_symbol = self.quick_deposit.currency
        self.assertEquals(actual_currency_symbol, currency,
                          msg=f'Actual currency symbol: "{actual_currency_symbol}" '
                              f'does not match expected symbol: "{currency}"')
        self.clear_input_using_keyboard(on_betslip=False)
        switch_to_main_page()
        self.quick_deposit.close_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.site.quick_bet_panel.close()
        self.site.open_betslip()
        self.site.betslip.remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.site.logout()
        self.navigate_to_page('Homepage')

    def test_012_repeat_steps_1_11_for_all_currencies_gbp_usd_eur_sek(self):
        """
        DESCRIPTION: Repeat steps #1-11 for all currencies ('GBP','USD','EUR')
        """
        for user, self.currency in [(tests.settings.user_with_usd_currency_and_card, '$'),
                                    (tests.settings.user_with_euro_currency_and_card, '€')]:
            self.test_000_preconditions(user=user)
            self.test_001_set_focus_on_cvv_field()
            self.test_002_enter_numeric_values()
            self.test_003_tap_remove_button_on_numeric_keyboard()
            self.test_004_enter_value_more_than_max_allowed_value_in_cvv_field()
            self.test_005_set_focus_on_deposit_amount_field()
            self.test_006_enter_numeric_values()
            self.test_007_tap_remove_button_on_numeric_keyboard()
            self.test_008_enter_value_under_1_in_decimal_format()
            self.test_009_enter_value_more_than_max_allowed_value_in_amount_field()
            self.test_010_set_cursor_anywhere_within_the_quick_deposit_section__tap_return_button_on_numeric_keyboard()
            self.test_011_set_cursor_over_deposit_amount_field_again(currency=self.currency)
