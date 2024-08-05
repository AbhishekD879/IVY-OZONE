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
class Test_C145997_Verify_ACCA_Odds_Notification_displaying_depending_on_Potential_Payout_parameter(Common):
    """
    TR_ID: C145997
    NAME: Verify ACCA Odds Notification displaying depending on Potential Payout parameter
    DESCRIPTION: This test case verifies ACCA Odds Notification displaying depending on Potential Payout parameter when Multiples are available in the Betslip
    DESCRIPTION: Odds calculation on ACCA notification instruction: https://confluence.egalacoral.com/display/SPI/Odds+calculation+on+ACCA+notification
    PRECONDITIONS: - Application is loaded
    PRECONDITIONS: - Any <Sport> landing page is opened
    """
    keep_browser_open = True

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        EXPECTED: * Odds value is shown:
        EXPECTED: a) For Double (1 Bets) in Multiples section
        EXPECTED: b) In case of more than 2 selections in 'Place your ACCA' section
        """
        pass

    def test_002_verify_that_potential_payout_parameter_from_the_buildbet_response_is_displayed_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Verify that potential payout parameter from the buildBet response is displayed on ACCA Odds Notification message
        EXPECTED: Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds
        """
        pass

    def test_003_repeat_steps_2_6_for_races_lp_price_type_only(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Races (LP price type only)
        EXPECTED: 
        """
        pass
