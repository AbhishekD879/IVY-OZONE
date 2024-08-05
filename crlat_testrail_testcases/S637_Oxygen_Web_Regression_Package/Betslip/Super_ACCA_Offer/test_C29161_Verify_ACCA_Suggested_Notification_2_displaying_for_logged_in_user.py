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
class Test_C29161_Verify_ACCA_Suggested_Notification_2_displaying_for_logged_in_user(Common):
    """
    TR_ID: C29161
    NAME: Verify ACCA Suggested Notification 2 displaying for logged in user
    DESCRIPTION: Verify ACCA Suggested Notification 2 displaying for logged in user
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: * BMA-10234 ACCA Suggested Notification on Betslip
    DESCRIPTION: * BMA-10235 ACCA Eligibility Notification on Betslip
    DESCRIPTION: * BMA-17369 Reactivating Suggested Notifications for ACCA Insurance
    DESCRIPTION: **!!! TEST CASE IS APPLICABLE FOR LADBROKES RELEASES PRECEDING OX 99; CORAL RELEASES REMAIN WITH CURRENT LOGIC DESCRIBED IN TEST CASE !!!**
    PRECONDITIONS: There are events with available ACCA Offers.
    PRECONDITIONS: For configuration of ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: The number of selections, which the user needs to add in order to be eligible for ACCA, corresponds to the trigger type. E.g., if trigger type is TBL - user will be ACCA eligible after adding 3 selections, if trigger type is ACC4 - 4 selections, and so on.
    PRECONDITIONS: To verify ACCA Offer details please check requests:
    PRECONDITIONS: - BuildBet  -> Bets-> Bet Offer
    PRECONDITIONS: To check potential stake, go to buildBet -> bets -> betTypeRef":"id": "ACC5" -> payout -> potential
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_login_with_user_who_use_gbpeuro_currency(self):
        """
        DESCRIPTION: Login with user who use GBP/Euro currency
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_selections_to_betslip_that_are_applicable_for_acca_insurance_and_their_combined_odds_are_below_31in_order_to_see_acca_eligilble_notification_the_number_of_selections_should_correspond_to_the_trigger_type_see_preconditions(self):
        """
        DESCRIPTION: Add selections to Betslip that are applicable for ACCA Insurance and their combined odds are below 3/1
        DESCRIPTION: In order to see ACCA Eligilble Notification, the number of selections should correspond to the trigger type (see preconditions).
        EXPECTED: ACCA Offer is received from Open Bet for the user
        EXPECTED: ACCA Suggested Notification 2 is displayed
        """
        pass

    def test_004_verify_acca_suggested_notification_2_displaying_in_betslip_for_appropriate_multiple(self):
        """
        DESCRIPTION: Verify ACCA Suggested Notification 2 displaying in Betslip for appropriate Multiple
        EXPECTED: ACCA Suggested Notification 2 is displayed
        """
        pass

    def test_005_enter_value_that_is_less_than_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is less than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Suggested Notification 2 disappears
        """
        pass

    def test_006_enter_value_that_is_equal_to_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is equal to 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Suggested Notification 2 appears
        """
        pass

    def test_007_enter_value_that_is_more_than_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is more than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Suggested Notification 2 is still displayed
        """
        pass
