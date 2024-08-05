import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C10375630_Added_for_OX98_Verify_Forecast_Tricast_bet_placing(Common):
    """
    TR_ID: C10375630
    NAME: [Added for OX98] Verify Forecast/Tricast bet placing
    DESCRIPTION: This test case verifies Forecast/Tricast bet placing
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Navigate to 'HR/Greyhounds' page
    PRECONDITIONS: Choose event -> see that Forecast/Tricast Tab is available
    PRECONDITIONS: Navigate to Forecast/Tricast Tab
    """
    keep_browser_open = True

    def test_001_add_tote_bets_to_the_betslip_in_forecasttricast_tab(self):
        """
        DESCRIPTION: Add tote bets to the Betslip in Forecast/Tricast Tab
        EXPECTED: Selections are added to the Betslip
        """
        pass

    def test_002_add_stake_value(self):
        """
        DESCRIPTION: Add Stake value
        EXPECTED: 'Stake value' is added
        """
        pass

    def test_003_tap_place_bet_button_and_verify_that_the_staked_bets_in_the_betslip_are_placed(self):
        """
        DESCRIPTION: Tap 'Place Bet' button and verify that the staked bets in the betslip are placed
        EXPECTED: The staked bets in the betslip are placed
        """
        pass

    def test_004_verify_that_the_bet_receipt_is_displayed_on_successful_bet_placement(self):
        """
        DESCRIPTION: Verify that the bet receipt is displayed on successful bet placement
        EXPECTED: The bet receipt is displayed on successful bet placement
        """
        pass
