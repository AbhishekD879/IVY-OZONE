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
class Test_C10386558_Added_for_OX98_Verify_Order_of_Selections_in_the_Bet_Slip(Common):
    """
    TR_ID: C10386558
    NAME: [Added for OX98] Verify Order of Selections in the Bet Slip
    DESCRIPTION: This test case verifies Order of Selections in the Bet Slip
    PRECONDITIONS: Enable Forecast/Tricast Tab in System Configuration (forecastTricastRacing) in CMS
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Navigate to 'HR/Greyhounds' page
    PRECONDITIONS: Choose event -> see that Ferecast/Tricast Tab is available
    PRECONDITIONS: Navigate to Ferecast/Tricast Tab
    """
    keep_browser_open = True

    def test_001_add_to_the_betslip_from_forecast_tab_two_selections_with_any_place_and_verify_that_selections_are_added_in_race_card_runner_number_order(self):
        """
        DESCRIPTION: Add to the betslip from 'Forecast' tab two Selections with 'Any Place' and verify that Selections are added in Race Card Runner Number order
        EXPECTED: Selections are added to the Betslip in Race Card Runner Number order
        """
        pass

    def test_002_add_to_the_betslip_from_tricast_tab_three_selections_with_any_place_and_verify_that_selections_are_added_in_race_card_runner_number_order(self):
        """
        DESCRIPTION: Add to the betslip from 'Tricast' tab three Selections with 'Any Place' and verify that Selections are added in Race Card Runner Number order
        EXPECTED: Selections are added to the Betslip in Race Card Runner Number order
        """
        pass

    def test_003_add_to_the_betslip_from_forecast_tab_two_selections_with_2nd_place_and_1st_place_and_verify_that_selections_are_added_in_1st2nd_place_order(self):
        """
        DESCRIPTION: Add to the betslip from 'Forecast' tab two Selections with '2nd Place' and '1st Place' and verify that Selections are added in 1st/2nd place order
        EXPECTED: Selections are added in 1st/2nd place order
        """
        pass

    def test_004_add_to_the_betslip_from_tricast_tab_three_selections_with_3rd2nd1st_place_and_verify_that_selections_are_added_in_1st2nd_3rd_place_order(self):
        """
        DESCRIPTION: Add to the betslip from 'Tricast' tab three Selections with '3rd/2nd/1st Place' and verify that Selections are added in 1st/2nd /3rd place order
        EXPECTED: Selections are added in 1st/2nd /3rd place order
        """
        pass
