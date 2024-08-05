import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.desktop
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only, test case is not applicable for Ladbrokes
@pytest.mark.crl_stg2
@pytest.mark.high
@pytest.mark.popup
@pytest.mark.login
@pytest.mark.widgets
@pytest.mark.user_account
@pytest.mark.safari
@vtest
class Test_C2211708_Accessing_Log_In_popup_Desktop_Mode(BaseUserAccountTest):
    """
    TR_ID: C2211708
    TR_ID: C16268964
    VOL_ID: C9698093
    NAME: Accessing Log In popup Desktop mode
    DESCRIPTION: This test case verifies accessing Log In popup from different places of the application
    PRECONDITIONS: Oxygen app is opened. User is logged out
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_check_log_in_button_present_on_the_header(self):
        """
        DESCRIPTION: Check "LOG IN" button is displayed on the screen
        EXPECTED: "LOG IN" button must be displayed on the screen
        """
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='"LOG IN" button is not displayed on site header')
        self.site.header.sign_in.click()

    def test_002_check_log_in_pop_up_is_displayed(self):
        """
        DESCRIPTION: Check 'Log In' pop-up is displayed on the screen
        EXPECTED: 'Log In' pop-up must be displayed on the screen
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(dialog, msg='"Log In" dialog does not appear')
        dialog.close_dialog()
        dialog.wait_dialog_closed()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=2)
        self.assertFalse(dialog,
                         msg='"Log In" dialog should not be displayed on the screen')

    def test_003_check_log_in_button_present_on_cash_out(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "CASH OUT" widget
        EXPECTED: "Log In" button must be displayed at "CASH OUT" widget
        """
        self.site.open_my_bets_cashout()
        log_in_button = self.site.cashout.tab_content.login_button
        self.assertTrue(log_in_button.is_displayed(), msg='"Log In" button is not displayed at "CASH OUT" widget')
        log_in_button.click()

    def test_004_repeat_step_2_for_cash_out(self):
        """
        DESCRIPTION: Repeat step #2 for 'Cash Out' widget
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()

    def test_005_check_log_in_button_present_on_open_bets(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "OPEN BETS" widget
        EXPECTED: "Log In" button must be displayed at "OPEN BETS" widget
        """
        self.site.open_my_bets_open_bets()
        log_in_button = self.site.open_bets.tab_content.login_button
        self.assertTrue(log_in_button.is_displayed(), msg='"Log In" button is not displayed at "OPEN BETS" widget')
        log_in_button.click()

    def test_006_repeat_step_2_for_open_bets(self):
        """
        DESCRIPTION: Repeat step #2 for 'Open Bets' widget
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()

    def test_007_check_log_in_button_present_on_bet_history(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "SETTLED BETS" widget
        EXPECTED: "Log In" button must be displayed at "SETTLED BETS" widget
        """
        self.site.open_my_bets_settled_bets()
        log_in_button = self.site.bet_history.login_button
        self.assertTrue(log_in_button.is_displayed(), msg='"Log In" button is not shown at "Settled Bets" widget')
        log_in_button.click()

    def test_008_repeat_step_2_for_bet_history(self):
        """
        DESCRIPTION: Repeat step #2 for 'Settled Bets' widget
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()

    def test_009_check_log_in_button_present_on_favorite_matches(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "FAVOURITE MATCHES" widget
        EXPECTED: "Log In" button must be displayed at the "FAVOURITE MATCHES" widget
        """
        log_in_button = self.site.favourites.login_button
        self.assertTrue(log_in_button.is_displayed(),
                        msg='"Log In" button is not shown at "FAVOURITE MATCHES" widget')
        log_in_button.click()

    def test_010_repeat_step_2_for_favourite_matches(self):
        """
        DESCRIPTION: Repeat step #2 for 'Favourite Matches' page
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()
