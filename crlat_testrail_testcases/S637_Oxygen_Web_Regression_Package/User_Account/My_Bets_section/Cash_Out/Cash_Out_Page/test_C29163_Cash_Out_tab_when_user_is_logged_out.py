import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C29163_Cash_Out_tab_when_user_is_logged_out(Common):
    """
    TR_ID: C29163
    NAME: 'Cash Out' tab when user is logged out
    DESCRIPTION: This test case verifies 'Cash Out' tab when the user is logged out.
    PRECONDITIONS: **JIRA ticket:** BMA-3925, BMA-17728
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_my_bets_page__bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'My Bets' page / 'Bet Slip' widget
        EXPECTED: 'My Bets' page / 'Bet Slip' widget is opened
        """
        pass

    def test_003_tap_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'Cash Out' tab
        EXPECTED: *   **"Please log in to see your Cash Out bets."** message is displayed
        EXPECTED: *   **'Log In'** button is shown below the message
        """
        pass

    def test_004_log_in_from_cash_out_tab(self):
        """
        DESCRIPTION: Log in from 'Cash Out' tab
        EXPECTED: *   User is logged in
        EXPECTED: *   Content of page is visible
        """
        pass
