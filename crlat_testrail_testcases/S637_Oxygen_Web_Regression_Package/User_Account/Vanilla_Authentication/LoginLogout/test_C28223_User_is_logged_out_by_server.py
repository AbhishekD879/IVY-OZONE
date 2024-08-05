import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C28223_User_is_logged_out_by_server(Common):
    """
    TR_ID: C28223
    NAME: User is logged out by server
    DESCRIPTION: This test scenario verifies that user is logged out by the server automatically when his/her session is over on the server and log out the message
    PRECONDITIONS: User has valid account to log in with.
    PRECONDITIONS: Pages to be checked on which user can be logged out by server with the 500 console error (with "code":x401):
    PRECONDITIONS: *   Bet Slip
    PRECONDITIONS: *   'My Bets'/'My history' pages
    PRECONDITIONS: *   'Cash out' page
    PRECONDITIONS: *   Private Markets (navigation to homepage if they are available)
    PRECONDITIONS: *   Stream: view the stream
    PRECONDITIONS: *   Lottery: Bet Placement section
    PRECONDITIONS: Pages to be checked on which user can be logged out by server without the 500 console error:
    PRECONDITIONS: *   Related to all other pages available in Right user menu (Deposit, Withdraw, My Account pages etc.)
    """
    keep_browser_open = True

    def test_001_log_in_with_valid_credentionals(self):
        """
        DESCRIPTION: Log in with valid credentionals
        EXPECTED: User is successfully logged in.
        """
        pass

    def test_002_open_separate_tab_in_the_browser_load_oxygen_app_and_log_in_there_with_the_same_credentials(self):
        """
        DESCRIPTION: Open separate tab in the browser, load oxygen app and log in there with the same credentials
        EXPECTED: User is already logged in
        """
        pass

    def test_003_log_out_from_one_of_opened_tabs(self):
        """
        DESCRIPTION: Log out from one of opened tabs
        EXPECTED: Session is over on the server side
        """
        pass

    def test_004_go_to_another_tab(self):
        """
        DESCRIPTION: Go to another tab
        EXPECTED: Ladbrokes:
        EXPECTED: * User is logged out automatically without performing any actions
        EXPECTED: * 'Log out' pop-up shouldn't be displayed. The user should be able to see a applications header that indicates the user has been logged out. The user shouldn't see a message that asks them to log in again.
        EXPECTED: Coral:
        EXPECTED: User is logged out automatically without performing any actions
        EXPECTED: 'Log out' pop-up is displayed
        """
        pass

    def test_005_only_for_coralverify_log_out_pop_up(self):
        """
        DESCRIPTION: ONLY FOR CORAL
        DESCRIPTION: Verify 'Log out' pop-up
        EXPECTED: Header:
        EXPECTED: * 'You are logged out' label
        EXPECTED: * 'X' button to close the message
        EXPECTED: *Body:*
        EXPECTED: * 'Sorry your session appears to have expired. Please login again. If this problem persists, contact our Customer Service Department' text message
        EXPECTED: * 'Cancel' button to close the message
        EXPECTED: * 'Login' button (after tapping opens login form)
        EXPECTED: * 'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened)
        """
        pass
