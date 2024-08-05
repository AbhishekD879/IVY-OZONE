import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28137_Verify_user_cash_balance_correctness(Common):
    """
    TR_ID: C28137
    NAME: Verify user cash balance correctness
    DESCRIPTION: This test case verifies correctness of user balance amount displayed after login and available for betting
    DESCRIPTION: Jira tickets:
    DESCRIPTION: BMA-6328,
    DESCRIPTION: BMA-8179 DeskTop Global Header - Logged in State
    DESCRIPTION: BMA-14549 [OpenAPI] Remove double requests to getPlayerInfo(31082) and getDynamicBalance(31020)
    PRECONDITIONS: Steps to see required info in console:
    PRECONDITIONS: 'Network' -> 'WS' -> Select last available item -> 'Frames'
    PRECONDITIONS: Example of notification (32010) after user log in:
    PRECONDITIONS: **3:::{data: {timestamp: "2017-03-01 15:19:39.095",…}, ID: 32010}
    PRECONDITIONS: ID
    PRECONDITIONS: :
    PRECONDITIONS: 32010
    PRECONDITIONS: data
    PRECONDITIONS: :
    PRECONDITIONS: {timestamp: "2017-03-01 15:19:39.095",…}
    PRECONDITIONS: balances
    PRECONDITIONS: :
    PRECONDITIONS: [{balance: {currencyCode: "EUR", amount: "125796.61"}, balanceType: "sportsbook_gaming_balance"}]
    PRECONDITIONS: 0
    PRECONDITIONS: :
    PRECONDITIONS: {balance: {currencyCode: "EUR", amount: "125796.61"}, balanceType: "sportsbook_gaming_balance"}
    PRECONDITIONS: timestamp
    PRECONDITIONS: :
    PRECONDITIONS: "2017-03-01 15:19:39.095"
    PRECONDITIONS: windowSessionId
    PRECONDITIONS: :
    PRECONDITIONS: "ox0
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: *   Homepage is shown
        EXPECTED: *   User is logged out
        """
        pass

    def test_002_log_in_with_valid_user_credentials_where_balance_is_positive(self):
        """
        DESCRIPTION: Log in with valid user credentials where balance is positive
        EXPECTED: *   User is logged in successfully
        EXPECTED: *   User balance is shown in top menu
        """
        pass

    def test_003_open_console___do_steps_from_preconditions(self):
        """
        DESCRIPTION: Open console -> Do steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_004_in_frames_section_find_the_notification_to_log_in_user_see_example_in_preconditions(self):
        """
        DESCRIPTION: In 'Frames' section find the notification to log in user (see example in Preconditions)
        EXPECTED: *   Notification is present ( as in Preconditions)
        """
        pass

    def test_005_click_on_notification___data__balances(self):
        """
        DESCRIPTION: Click on notification -> data ->balances
        EXPECTED: "balanceType":"sportsbook_gaming_balance" and amount  is present among other balances
        """
        pass

    def test_006_verify_user_balance_correctness_displayed_on_right_menu_slideout_betslip_header_menu(self):
        """
        DESCRIPTION: Verify user balance correctness displayed on Right Menu, SlideOut Betslip, Header Menu
        EXPECTED: * User balance amount is equel to amount of "sportsbook_gaming_balance"
        EXPECTED: * Balance currency is the same as in "currencyCode"
        """
        pass
