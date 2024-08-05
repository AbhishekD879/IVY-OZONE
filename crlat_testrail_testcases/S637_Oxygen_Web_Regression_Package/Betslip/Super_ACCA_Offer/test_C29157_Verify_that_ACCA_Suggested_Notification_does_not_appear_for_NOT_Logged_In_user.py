import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29157_Verify_that_ACCA_Suggested_Notification_does_not_appear_for_NOT_Logged_In_user(Common):
    """
    TR_ID: C29157
    NAME: Verify that ACCA Suggested Notification does not appear for NOT Logged In user
    DESCRIPTION: This test case verifies that ACCA Suggested Notification does not appear for NOT Logged In user
    DESCRIPTION: Jira tikets:
    DESCRIPTION: * BMA-10234 ACCA Suggested Notification on Betslip
    DESCRIPTION: * BMA-10235 ACCA Eligibility Notification on Betslip
    PRECONDITIONS: * There are events with available ACCA Offers.
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet  -> Bets-> Bet Offer
    PRECONDITIONS: * User should be **logged out**
    """
    keep_browser_open = True

    def test_001_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: Selections are added to the Betslip
        """
        pass

    def test_002_open_betslip_and_verify_acca_notification_message_displaying(self):
        """
        DESCRIPTION: Open Betslip and verify ACCA Notification message displaying
        EXPECTED: ACCA Notification message is NOT displayed for user in the Betslip for appropriate Multiple
        """
        pass

    def test_003_log_in_to_application_and_verify_acca_notification_message_displaying(self):
        """
        DESCRIPTION: Log in to application and verify ACCA Notification message displaying
        EXPECTED: ACCA Notification message is displayed for user after login
        """
        pass

    def test_004_log_out_and_open_betslip(self):
        """
        DESCRIPTION: Log out and open Betslip
        EXPECTED: ACCA Notification message is no longer displayed
        """
        pass
