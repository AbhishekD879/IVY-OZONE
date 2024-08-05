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
class Test_C2024339_Tracking_of_clicking_on_Group_Division_tabs_in_League_Table_widget_on_the_Football_Competitions_page(Common):
    """
    TR_ID: C2024339
    NAME: Tracking of clicking on 'Group'/'Division' tabs in 'League Table' widget on the Football Competitions page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when on 'Group'/'Division' tabs in the 'League Table' widget on the Football Competitions page.
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

    def test_002_navigate_to_football_competitions_details_page_of_group_stage_league_ie_the_international_class_euro_cup_league_or_league_with_separate_division_ie_usa_class_major_league_soccer_type_with_available_league_table_widget(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page of Group Stage League (ie. the 'International' class, 'Euro Cup' league) or League with Separate Division (ie. 'USA' class, 'Major League Soccer' type) with available 'League Table' widget
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'League Table' Widget is displayed in 3rd column or below main content (depends on screen resolution)
        EXPECTED: * 'Group'/'Division' tabs are displayed below Sub Header with the league name
        """
        pass

    def test_003_click_on_some_groupdivision_tab(self):
        """
        DESCRIPTION: Click on some 'Group'/'Division' tab
        EXPECTED: * 'Group'/'Division' tab is clickable
        EXPECTED: * Selected 'Group'/'Division' tab is highlighted
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'league table',
        EXPECTED: 'eventLabel' : 'change league'
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_for_different_groupdivision_tabs(self):
        """
        DESCRIPTION: Repeat steps 3-4 for different 'Group'/'Division' tabs
        EXPECTED: 
        """
        pass
