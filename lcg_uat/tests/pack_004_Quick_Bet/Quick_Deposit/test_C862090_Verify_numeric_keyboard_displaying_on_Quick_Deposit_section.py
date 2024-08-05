import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.quick_bet
@pytest.mark.numeric_keyboard
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C862090_Verify_numeric_keyboard_displaying(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C862090
    VOL_ID: C9698351
    NAME: Verify numeric keyboard displaying on 'Quick Deposit' section
    DESCRIPTION: This test case verifies numeric keyboard displaying with Quick Deposit section on Quick Bet
    PRECONDITIONS: User account with zero balance and supported card types added
    PRECONDITIONS: User account with positive balance and supported card types added
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def enter_value_using_keyboard(self, value):
        keyboard = self.site.quick_bet_panel.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=value)

    def clear_input_using_keyboard(self, value=None):
        keyboard = self.site.quick_bet_panel.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        value = len(str(value)) if value else self.max_number_of_symbols_in_stake_input
        for i in range(0, value):
            keyboard.enter_amount_using_keyboard(value='delete')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Oxygen application is loaded
        DESCRIPTION: User account with zero balance and supported card types added
        DESCRIPTION: User account with positive balance and supported card types added
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            event = event_params.ss_response
        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
        market_name = next((market.get('market').get('name') for market in event['event']['children']
                            if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        self._logger.info(f'*** Using event "{self.eventID}" with market "{market_name}"')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.__class__.username_small_balance = tests.settings.quick_deposit_user

    def test_001_log_in_as_user_with_zero_balance(self):
        """
        DESCRIPTION: Log in as user with zero balance
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.user_0_balance_with_card)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Event Details page
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_click_on_football_event_bet_button(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        """
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_004_tap_deposit_validate_keyboard(self):
        """
        DESCRIPTION: Fill valid 'Stake" and tap on 'MAKE A QUICK DEPOSIT' button
        EXPECTED: Quick Bet is displayed
        EXPECTED: Numeric keyboard with 'Quick stakes' buttons is not shown
        """
        self.__class__.over_balance = self.user_balance + 5
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(timeout=5),
                        msg='Amount input field is not displayed')
        self.site.quick_bet_panel.selection.content.amount_form.input.click()
        self.enter_value_using_keyboard(value=self.over_balance)

        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(), msg='Quick Deposit is not shown')
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.assertFalse(self.quick_deposit.has_keyboard(expected_result=False, timeout=3),
                         msg='Numeric keyboard is shown')
        self.site.wait_content_state_changed()

    def test_005_click_cvv_and_verify_numeric_keyboard(self):
        """
        DESCRIPTION: Set focus over 'Stake' field / 'Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons appears
        """
        self.quick_deposit.cvv_2.click()
        self.assertTrue(self.quick_deposit.has_keyboard(expected_result=True, timeout=3),
                        msg='Numeric keyboard is not shown')

        keyboard = self.quick_deposit.keyboard
        keyboard.enter_amount_using_keyboard(value='enter')

        self.assertFalse(self.quick_deposit.has_keyboard(expected_result=False, timeout=3),
                         msg='Numeric keyboard is not shown')
        self.quick_deposit.switch_to_main_page()

    def test_006_tap_on_quick_deposit_section_header_or_x_button_in_quick_deposit_section(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header / 'X' button in 'Quick Deposit' section / 'Quick Deposit' link in the Quick Bet header
        EXPECTED: - Numeric Keyboard disappears
        EXPECTED: - 'Quick Deposit' section is collapsed
        """
        close_button = self.site.quick_bet_panel.quick_deposit_panel.close_button
        self.assertTrue(close_button.is_enabled(), msg='Close button is not enabled.')
        close_button.click()
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_deposit_panel(expected_result=False),
                         msg='"Quick Deposit" is not closed')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.assertFalse(self.site.quick_bet_panel.keyboard.is_displayed(name='Quick Stake keyboard not shown',
                                                                         expected_result=False, timeout=7),
                         msg='Numeric keyboard is shown')
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_deposit_panel(expected_result=False),
                         msg='Quick Deposit section is shown')

    def test_007_enter_value_into_stake_field(self):
        """
        DESCRIPTION: Enter value into 'Stake' field
        EXPECTED: - 'Quick Deposit' section remains collapsed
        """
        self.__class__.over_balance = 5.00
        self.site.wait_splash_to_hide(5)
        self.site.quick_bet_panel.selection.content.amount_form.input.click()  # TODO: VOL-4378
        self.assertTrue(self.site.quick_bet_panel.keyboard.is_displayed(name='Quick Stake keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')

        self.enter_value_using_keyboard(value=self.user_balance + self.over_balance)
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_deposit_panel(expected_result=False),
                         msg='"Quick Deposit" section is expanded')

    def test_008_tap_on_info_message_or_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message / 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is opened
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='Quick Deposit section is not shown')

    def test_009_click_on_amount_field(self):
        """
        DESCRIPTION: Set focus over 'Stake' field / 'Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons appears
        """
        quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        quick_deposit.cvv_2.input.click()
        self.assertTrue(quick_deposit.has_keyboard(expected_result=True, timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard = quick_deposit.keyboard
        keyboard.enter_amount_using_keyboard(value='enter')
        self.assertFalse(quick_deposit.has_keyboard(expected_result=False, timeout=3),
                         msg='Numeric keyboard is not shown')
        quick_deposit.switch_to_main_page()
        # close quick deposit

        close_button = self.site.quick_bet_panel.quick_deposit_panel.close_button
        self.assertTrue(close_button.is_enabled(), msg='Close button is not enabled.')
        close_button.click()
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_deposit_panel(expected_result=False),
                         msg='Quick Deposit is not closed')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')

        # close quick bet panel
        self.site.wait_splash_to_hide(3)
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_010_log_out_and_log_in_as_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log out and Log in as user account with positive balance
        """
        self.site.logout()
        self.site.wait_content_state(state_name='Homepage')

        self.site.login(username=self.username_small_balance)
        self.__class__.user_balance = self.site.header.user_balance

    def test_011_select_one_selection_to_quick_bet_and_enter_higher_stake_than_user_balance(self):
        """
        DESCRIPTION: Select one selection to Quick Bet and enter higher stake than user balance
        EXPECTED: - 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message appears
        EXPECTED: - Numeric keyboard is shown
        """
        self.navigate_to_edp(event_id=self.eventID)
        counter_value = len(self.site.header.bet_slip_counter.counter_value)
        if counter_value > 0:
            self.site.header.bet_slip_counter.click()
            self.clear_betslip()
            # self.device.go_back()
        self.test_003_click_on_football_event_bet_button()
        self.test_007_enter_value_into_stake_field()
        self.assertTrue(self.site.quick_bet_panel.keyboard.is_displayed(name='Quick Stake keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')

    def test_012_tap_on_make_a_deposit_button_or_info_message(self):
        """
        DESCRIPTION: Tap on 'MAKE A DEPOSIT' button / Message 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message to user
        EXPECTED: - 'Quick Deposit' section is displayed
        EXPECTED: - Numeric keyboard is hidden
        EXPECTED: - 'Quick stakes' buttons are displayed
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='Quick Deposit section is not shown')

        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.assertFalse(self.quick_deposit.has_keyboard(expected_result=False, timeout=3),
                         msg='Numeric keyboard is not shown')

    def test_013_set_focus_over_deposit_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' field / 'Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons appears
        """
        self.quick_deposit.cvv_2.click()
        self.assertTrue(self.quick_deposit.has_keyboard(expected_result=True, timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard = self.quick_deposit.keyboard
        keyboard.enter_amount_using_keyboard(value='enter')
        self.assertFalse(self.quick_deposit.has_keyboard(expected_result=False, timeout=3),
                         msg='Numeric keyboard is not shown')
        self.quick_deposit.switch_to_main_page()

    def test_014_tap_on_quick_deposit_section_header_or_x_button_in_quick_deposit_section(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header / 'X' button in 'Quick Deposit' section/'Quick Deposit' link in the Betslip header
        EXPECTED: -'Quick Deposit' section disappears
        EXPECTED: -Numeric keyboard is no longer available
        """
        close_button = self.site.quick_bet_panel.quick_deposit_panel.close_button
        self.assertTrue(close_button.is_enabled(), msg='Close button is not enabled.')
        close_button.click()
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_deposit_panel(expected_result=False),
                         msg='Quick Deposit is not closed')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.assertFalse(self.site.quick_bet_panel.keyboard.is_displayed(name='Quick Stake keyboard shown',
                                                                         expected_result=False, timeout=3),
                         msg='Numeric keyboard is not hidden')
