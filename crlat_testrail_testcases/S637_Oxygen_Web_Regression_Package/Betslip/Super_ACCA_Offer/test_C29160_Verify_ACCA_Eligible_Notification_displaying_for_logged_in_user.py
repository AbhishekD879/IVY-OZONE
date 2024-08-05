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
class Test_C29160_Verify_ACCA_Eligible_Notification_displaying_for_logged_in_user(Common):
    """
    TR_ID: C29160
    NAME: Verify ACCA Eligible Notification displaying for logged in user
    DESCRIPTION: This test case verifies ACCA Eligible Notification displaying for logged in user
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: * BMA-10234 ACCA Suggested Notification on Betslip
    DESCRIPTION: * BMA-10235 ACCA Eligibility Notification on Betslip
    DESCRIPTION: * BMA-17369 Reactivating Suggested Notifications for ACCA Insurance
    PRECONDITIONS: There should be events with available ACCA Offers.
    PRECONDITIONS: For configuration of ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: The number of selections, which the user needs to add in order to be eligible for ACCA, corresponds to the trigger type. E.g., if trigger type is TBL - user will be ACCA eligible after adding 3 selections, if trigger type is ACC4 - 4 selections, and so on.
    PRECONDITIONS: To verify ACCA Offer details please check requests:
    PRECONDITIONS: To check potential stake, go to buildBet -> bets -> betTypeRef":"id": "ACC5" -> payout -> potential
    PRECONDITIONS: User should be **logged in**
    """
    keep_browser_open = True

    def test_001_add_selections_to_betslip_that_are_applicable_for_acca_insurance_and_their_combined_odds_are_above_31note_in_order_to_see_acca_eligilble_notification_the_number_of_selections_should_correspond_to_the_trigger_type_see_preconditions(self):
        """
        DESCRIPTION: Add selections to Betslip that are applicable for ACCA Insurance and their combined odds are above 3/1
        DESCRIPTION: NOTE: In order to see ACCA Eligilble Notification, the number of selections should correspond to the trigger type (see preconditions).
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        pass

    def test_002_verify_acca_eligible_notification_displaying_in_betslip_for_appropriate_multiples(self):
        """
        DESCRIPTION: Verify ACCA Eligible Notification displaying in Betslip for appropriate Multiples
        EXPECTED: ACCA Eligible Notification is displayed
        """
        pass

    def test_003_enter_value_that_is_less_than_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is less than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Eligible Notification disappears
        """
        pass

    def test_004_enter_value_that_is_equal_to_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is equal to 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Eligible Notification appears
        """
        pass

    def test_005_enter_value_that_is_more_than_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is more than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Eligible Notification is still displayed
        """
        pass
