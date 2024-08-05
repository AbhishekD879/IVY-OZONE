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
class Test_C10397562_Added_for_OX98_Verify_that_Forecast_Tricast_Sections_are_added_to_the_Betslip(Common):
    """
    TR_ID: C10397562
    NAME: [Added for OX98] Verify that Forecast/Tricast Sections are added to the Betslip
    DESCRIPTION: This test case verifies that Forecast/Tricast Sections are added to the Betslip (No Quick Bet )
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Navigate to 'HR/Greyhounds' page
    PRECONDITIONS: Choose event -> see that Ferecast/Tricast Tab is available
    PRECONDITIONS: Navigate to Ferecast/Tricast Tab
    """
    keep_browser_open = True

    def test_001___select_two_selections_in_forecast_tab_and_tap_add_to_bet_slip_button__verify_that_sections_are_added_to_the_betslip(self):
        """
        DESCRIPTION: - Select two Selections in Forecast Tab and tap "Add to bet slip" button.
        DESCRIPTION: - Verify that Sections are added to the Betslip
        EXPECTED: Sections are added to the Betslip (No Quick Bet)
        """
        pass

    def test_002___select_three_selections_in_tricast_tab_and_tap_add_to_bet_slip_button__verify_that_sections_are_added_to_the_betslip(self):
        """
        DESCRIPTION: - Select three Selections in Tricast Tab and tap "Add to bet slip" button.
        DESCRIPTION: - Verify that Sections are added to the Betslip
        EXPECTED: Sections are added to the Betslip (No Quick Bet)
        """
        pass
