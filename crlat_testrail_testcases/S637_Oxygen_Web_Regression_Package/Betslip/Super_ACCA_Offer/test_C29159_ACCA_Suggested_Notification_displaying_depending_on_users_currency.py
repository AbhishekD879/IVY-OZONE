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
class Test_C29159_ACCA_Suggested_Notification_displaying_depending_on_users_currency(Common):
    """
    TR_ID: C29159
    NAME: ACCA Suggested Notification displaying depending on user's currency
    DESCRIPTION: This test case verifies  'Place your ACCA (X selections)' Section currency displaying depending on user's currency
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: * BMA-10234 ACCA Suggested Notification on Betslip
    DESCRIPTION: * BMA-10235 ACCA Eligibility Notification on Betslip
    DESCRIPTION: * BMA-17369 Reactivating Suggested Notifications for ACCA Insurance
    PRECONDITIONS: There are events with available ACCA Offers.
    PRECONDITIONS: For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: To verify ACCA Offer details please check requests:
    PRECONDITIONS: - BuildBet  -> Bets-> Bet Offer
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: - Home page is opened
        """
        pass

    def test_002_login_with_user_who_use_gbp_currency(self):
        """
        DESCRIPTION: Login with user who use GBP currency
        EXPECTED: - User is logged in
        """
        pass

    def test_003_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        pass

    def test_004_verify_acca_notification_displaying(self):
        """
        DESCRIPTION: Verify ACCA Notification displaying
        EXPECTED: ACCA Notification is displayed for user with GBP currency
        EXPECTED: NOTE: In case if trigger type is TBL, ACCA eligible instead of ACCA suggested offer will be displayed.
        """
        pass

    def test_005_repeat_steps_2_4_for_user_with_euro_currency(self):
        """
        DESCRIPTION: Repeat steps 2-4 for user with Euro currency
        EXPECTED: ACCA Notification is displayed for user with Euro currency
        EXPECTED: NOTE: In case if trigger type is TBL, ACCA eligible instead of ACCA suggested offer will be displayed.
        """
        pass

    def test_006_repeat_steps_2_4_for_user_with_usd_currency(self):
        """
        DESCRIPTION: Repeat steps 2-4 for user with USD currency
        EXPECTED: ACCA Notification is NOT displayed for user with USD currency even if in OpenBet response ACCA Offer is present
        """
        pass

    def test_007_repeat_steps_2_4_for_user_with_sek_currency(self):
        """
        DESCRIPTION: Repeat steps 2-4 for user with SEK currency
        EXPECTED: ACCA Notification is NOT displayed for user with SEK currency even if in OpenBet response ACCA Offer is present
        """
        pass
