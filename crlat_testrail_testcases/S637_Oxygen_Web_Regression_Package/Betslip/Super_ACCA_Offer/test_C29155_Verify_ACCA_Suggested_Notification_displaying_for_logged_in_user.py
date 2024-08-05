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
class Test_C29155_Verify_ACCA_Suggested_Notification_displaying_for_logged_in_user(Common):
    """
    TR_ID: C29155
    NAME: Verify ACCA Suggested Notification displaying for logged in user
    DESCRIPTION: This test case verifies Super ACCA Notification message is displayed for logged in user
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: * BMA-10234 Acca Suggested Notification on Betslip
    DESCRIPTION: * BMA-10235 Acca Eligibility Notification on Betslip
    DESCRIPTION: * BMA-17369 Reactivating Suggested Notifications for ACCA Insurance
    DESCRIPTION: AUTOTEST [C1502047]
    DESCRIPTION: AUTOTEST [C527751]
    DESCRIPTION: **!!! TEST CASE IS APPLICABLE FOR LADBROKES RELEASES PRECEDING OX 99; CORAL RELEASES REMAIN WITH CURRENT LOGIC DESCRIBED IN TEST CASE !!!**
    PRECONDITIONS: * There are events with available ACCA Offers.
    PRECONDITIONS: * For configuration of ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests: BuildBet -> Bets-> Bet Offer
    """
    keep_browser_open = True

    def test_001_log_in_with_user_who_uses_gbpeuro_currency(self):
        """
        DESCRIPTION: Log in with user who uses GBP/Euro currency
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        pass

    def test_003_verify_acca_notification_message_displaying_in_betslip_for_appropriate_multiple(self):
        """
        DESCRIPTION: Verify ACCA Notification message displaying in Betslip for appropriate Multiple
        EXPECTED: ACCA Notification message is displayed for the user with next elements:
        EXPECTED: * number of extra selections required in order for User to trigger the Acca offer
        EXPECTED: * available Bonus amount
        EXPECTED: * maximum lose legs that the user will benefit from with the offer
        EXPECTED: NOTE: In case if trigger type is TBL, ACCA eligible instead of ACCA suggested notification will be displayed.
        """
        pass

    def test_004_check_if_the_displayed_data_is_correct(self):
        """
        DESCRIPTION: Check if the displayed data is correct
        EXPECTED: Number of selections, still needed to be added to betslip in order for User to trigger the Acca offer can be found from next sequence: **[TBL, ACC4, ACC5, ...., ACCn]**.
        EXPECTED: For example, if in **buildBet** Response **betTypeRef** is TBL and trigger_id point to **freebetTriggerBetType** in reqFreebetGetOffersResponse to ACC5, then number of additional legs is 2.
        """
        pass

    def test_005_add_one_more_selection_with_applicable_acca_insurance_and_verify_message_content_update(self):
        """
        DESCRIPTION: Add one more selection with applicable ACCA Insurance and verify message content update
        EXPECTED: * Number of extra selections required for Acca Offer is appropriately decreased by 1 in the message
        EXPECTED: * Number of extra selections is updated in real time without page refresh
        """
        pass

    def test_006_remove_selection_with_applicable_acca_offer_from_the_betslip_and_verify_message_content_update(self):
        """
        DESCRIPTION: Remove selection with applicable Acca Offer from the Betslip and verify message content update
        EXPECTED: * Number of extra selections required for Acca Offer is appropriately increased by 1 in the message
        EXPECTED: * Number of extra selections is updated in real time without page refresh
        """
        pass
