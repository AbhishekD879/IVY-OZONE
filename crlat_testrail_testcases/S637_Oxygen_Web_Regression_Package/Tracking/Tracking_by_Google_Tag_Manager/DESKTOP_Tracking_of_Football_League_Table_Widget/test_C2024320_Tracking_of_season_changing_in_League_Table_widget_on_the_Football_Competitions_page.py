import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2024320_Tracking_of_season_changing_in_League_Table_widget_on_the_Football_Competitions_page(Common):
    """
    TR_ID: C2024320
    NAME: Tracking of season changing in 'League Table' widget on the Football Competitions page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when changing the season in the 'League Table' widget on the Football Competitions page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_competitions_details_page_with_available_league_table_widget(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page with available 'League Table' widget
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'League Table' Widget is displayed in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_003_verify_subheader_of_league_table_widget_if_more_than_1_season_is_available(self):
        """
        DESCRIPTION: Verify subheader of League Table Widget if more than 1 season is available
        EXPECTED: Subheader contains:
        EXPECTED: * season name of competition user is viewing (e.g. Championship 17/18)
        EXPECTED: * left/right arrows in case of multiple seasons within the same competition
        """
        pass

    def test_004_click_on_right_navigation_arrow_in_subheader_at_the_league_table_widget(self):
        """
        DESCRIPTION: Click on Right Navigation Arrow in subheader at the 'League Table' widget
        EXPECTED: * season name of competition is changed
        EXPECTED: * appropriate data related to the chosen season is displayed in 'League Table' widget
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'league table',
        EXPECTED: 'eventLabel' : 'change season'
        EXPECTED: })
        """
        pass

    def test_006_click_on_left_navigation_arrow_in_subheader_at_the_league_table_widget(self):
        """
        DESCRIPTION: Click on Left Navigation Arrow in subheader at the 'League Table' widget
        EXPECTED: * season name of competition is changed
        EXPECTED: * appropriate data related to the chosen season is displayed in 'League Table' widget
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'league table',
        EXPECTED: 'eventLabel' : 'change season'
        EXPECTED: })
        """
        pass

    def test_008_repeat_steps_4_7_several_times(self):
        """
        DESCRIPTION: Repeat steps 4-7 several times
        EXPECTED: 
        """
        pass
