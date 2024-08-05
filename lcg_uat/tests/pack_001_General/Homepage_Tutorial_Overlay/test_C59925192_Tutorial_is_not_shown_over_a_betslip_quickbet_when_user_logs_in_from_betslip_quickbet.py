import pytest
import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import ElementClickInterceptedException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@pytest.mark.tutorial_overlay
@pytest.mark.cookies
@pytest.mark.local_storage
@vtest
class Test_C59925192_Tutorial_is_not_shown_over_a_betslip_quickbet_when_user_logs_in_from_betslip_quickbet(BaseBetSlipTest):
    """
    TR_ID: C59925192
    NAME: Tutorial is not shown over a betslip/quickbet when user logs in from betslip/quickbet
    DESCRIPTION: Information that Homepage Tutorial Overlay was shown is saved in Local Storage: name - OX.tutorial, value - true. Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
    DESCRIPTION: ![](index.php?/attachments/get/119596341)
    PRECONDITIONS:
    """
    keep_browser_open = True
    bet_amount = 50
    username = tests.settings.user_with_minimum_balance

    def login(self):
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.dialog.username = self.username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        try:
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            self._logger.warning(e)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
        self.site.wait_logged_in()

    def test_000_preconditons(self):
        """
        DESCRIPTION: Create events for test environment
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_premier_league_football_event()

    def test_001_clear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application
        EXPECTED: Do not login to application and go to the Homepage/Football Landing page
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_add_any_selection_to_betslip(self):
        """
        DESCRIPTION: Add any Selection to Betslip.
        EXPECTED: Selection is added to Betslip
        """
        bet_buttons_list = self.site.home.bet_buttons
        if not bet_buttons_list:
            self.navigate_to_page('/')
            bet_buttons_list = self.site.home.bet_buttons

        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')

        for selection in range(len(bet_buttons_list)):
            selection_btn = bet_buttons_list[selection]
            self.site.contents.scroll_to_we(selection_btn)
            if selection_btn.is_enabled():
                try:
                    selection_btn.click()
                    break
                except ElementClickInterceptedException:
                    self._logger.info('ElementClickInterceptedException ..')
                    continue
            else:
                continue
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True, timeout=15),
                        msg='Quick Bet is not opened')

    def test_003_open_betslip_and_provide_a_stake_that_is_smallerbigger_than_user_balance_ie_150gbp(self):
        """
        DESCRIPTION: Open Betslip and provide a stake that is smaller/bigger than user balance (i.e. 150GBP)
        EXPECTED: 'Stake' field contains provided amount
        """
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)

    def test_004_click_on_login__place_bet_and_log_in_as_a_user_with_little_balance_lower_than_provided_stake(self):
        """
        DESCRIPTION: Click on "Login & Place Bet" and log in as a user with little balance (lower than provided stake)
        EXPECTED: User remains on betslip, but no Tutorial overlay is shown
        """
        betnow_btn = self.get_betslip_content().bet_now_button
        betnow_btn.click()
        self.login()
        self.assertFalse(self.site.tutorial_overlay, msg='Tutorial overlay is shown for not logged user')
        self.navigate_to_page('/')

    def test_005_log_out_from_appclear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Log out from App
        DESCRIPTION: Clear browser cookies and load Oxygen application
        EXPECTED: Do not login to application and go to the Homepage/Football Landing page
        """
        self.site.logout()
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.refresh_page()
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')

    def test_006_add_any_selection_to_quickbet(self):
        """
        DESCRIPTION: Add any Selection to Quickbet
        EXPECTED: Selection is added to Quickbet
        """
        self.test_002_add_any_selection_to_betslip()

    def test_007_provide_a_stake_that_is_smallerbigger_than_user_balance_ie_150gbp(self):
        """
        DESCRIPTION: Provide a stake that is smaller/bigger than user balance (i.e. 150GBP)
        EXPECTED: 'Stake' field contains provided amount
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.click()
        quick_bet.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), msg='The button "Place bet" is not active')
        self.site.quick_bet_panel.place_bet.click()

    def test_008_click_on_login__place_bet_and_log_in_as_a_user_with_little_balance_lower_than_provided_stake(self):
        """
        DESCRIPTION: Click on "Login & Place Bet" and log in as a user with little balance (lower than provided stake)
        EXPECTED: User remains on Quickbet, but no Tutorial overlay is shown
        """
        self.login()
        self.assertTrue(self.site.quick_bet_overlay, msg='Overlay is closed')
        self.assertFalse(self.site.tutorial_overlay, msg='Tutorial overlay is shown for not logged user')
