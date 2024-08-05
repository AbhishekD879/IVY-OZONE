import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870199_Racing_Result_Verify_that_when_user_navigates_via_Race_Landing_page_to_Results_tab_the_data_is_displayed_under_two_tabs_By_latest_Results_and_By_Meetings_Verify_results_contents_Tricast_Forecast_dividends_Non_runners_Runner_silk_Runner_number(Common):
    """
    TR_ID: C44870199
    NAME: "Racing Result : "Verify that when user navigates via Race Landing page to Results tab, the data is displayed under two tabs, By latest Results and By Meetings -Verify results contents: Tricast/Forecast dividends Non-runners Runner silk Runner number
    DESCRIPTION: "Verify that when user navigates via Race Landing page to Results tab, the data is displayed under two tabs, By latest Results and By Meetings
    DESCRIPTION: -Verify results contents:
    DESCRIPTION: Dividends
    DESCRIPTION: Non-runners
    DESCRIPTION: Runner silk
    DESCRIPTION: Runner number
    DESCRIPTION: Runner name"
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_the_contents_of_resulted_raceon_racing_scroll_panel___click_on_the_raceevent_with_the_resultpost_sign(self):
        """
        DESCRIPTION: Verify the contents of Resulted Race
        DESCRIPTION: On Racing scroll panel - Click on the Race/Event with the Result/post sign
        EXPECTED: User should be able to see
        EXPECTED: Event Name, Day, Time, Date.
        EXPECTED: E/W terms
        EXPECTED: Race Result - Selection Name, Place, silks and odds
        EXPECTED: Dividends: Forecast
        """
        pass
