import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C518419_Bet_History_tab_with_Finished_Session(Common):
    """
    TR_ID: C518419
    NAME: 'Bet History' tab with Finished Session
    DESCRIPTION: This test case verifies 'Bet History' tab when user is logged out by server automatically when his/her session is over on the server.
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Invictus in one browser tab, go 'Betslip' widget -> 'Open Bets' tab-> 'Regular' filter
    PRECONDITIONS: *   Login to Invictus in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_load_invictus_application_on_desktoptablet_device(self):
        """
        DESCRIPTION: Load Invictus application on desktop/tablet device
        EXPECTED: - Homepage is opened
        """
        pass

    def test_002_log_in_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log in with User account with positive balance
        EXPECTED: - User is Logged In
        """
        pass

    def test_003_navigate_to_bet_history_tab(self):
        """
        DESCRIPTION: Navigate to 'Bet History' tab
        EXPECTED: - Tab is opened with filter 'Regular'
        EXPECTED: - List of Recent Bets is displayed
        """
        pass

    def test_004_make_steps_from_preconditions_to_finish_user_session(self):
        """
        DESCRIPTION: Make steps from preconditions to finish user session
        EXPECTED: 
        """
        pass

    def test_005_open_any_collapsed_section(self):
        """
        DESCRIPTION: Open any collapsed section
        EXPECTED: -  Pop-up message about logging out is shown
        EXPECTED: - (Vanilla) User is redirected to login form with "Your session expired." message
        """
        pass

    def test_006_vanillaclose_login_form(self):
        """
        DESCRIPTION: **Vanilla:**
        DESCRIPTION: Close login form
        EXPECTED: -  User is logged out from the application and Betslip tab is selected in Betslip widget
        EXPECTED: -   User is not able to see content of 'Bet History' tab
        EXPECTED: -  Coral: 'Please log in to see your Bet History.' message and 'Log In' button are shown
        EXPECTED: Ladbrokes: 'Your settled bets will appear here, Please login to view.' message is shown
        """
        pass

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_008_tap_lotto_filter_and_make_steps_from_preconditions_to_finish_user_session(self):
        """
        DESCRIPTION: Tap 'Lotto' filter and make steps from preconditions to finish user session
        EXPECTED: -  Pop-up message about logging out is shown
        EXPECTED: - **(Vanilla)** User is redirected to login form with "Your session expired." message
        """
        pass

    def test_009_vanillaclose_login_form(self):
        """
        DESCRIPTION: **Vanilla:**
        DESCRIPTION: Close login form
        EXPECTED: -  User is logged out from the application and Betslip tab is selected in Betslip widget
        EXPECTED: -   User is not able to see content of 'Bet History' tab
        EXPECTED: -  Coral: 'Please log in to see your Bet History.' message and 'Log In' button are shown
        EXPECTED: Ladbrokes: 'Your settled bets will appear here, Please login to view.' message is shown
        """
        pass

    def test_010_repeat_steps_6_7_for_pools_filter(self):
        """
        DESCRIPTION: Repeat steps #6-7 for 'Pools' filter
        EXPECTED: 
        """
        pass
