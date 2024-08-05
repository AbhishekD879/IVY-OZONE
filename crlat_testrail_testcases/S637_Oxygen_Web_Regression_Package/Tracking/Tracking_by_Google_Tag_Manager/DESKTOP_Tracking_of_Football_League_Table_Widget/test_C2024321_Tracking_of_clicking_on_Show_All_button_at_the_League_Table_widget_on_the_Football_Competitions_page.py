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
class Test_C2024321_Tracking_of_clicking_on_Show_All_button_at_the_League_Table_widget_on_the_Football_Competitions_page(Common):
    """
    TR_ID: C2024321
    NAME: Tracking of clicking on 'Show All' button at the 'League Table' widget on the Football Competitions page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Show More' button at the 'Result' widget on the Football Competitions page.
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
        EXPECTED: * The first 5 teams are displayed in the widget
        EXPECTED: * 'Show All' button is displayed below the last team in widget's footer
        """
        pass

    def test_003_click_on_show_all_button_at_the_footer_on_league_table_widget(self):
        """
        DESCRIPTION: Click on 'Show All' button at the footer on 'League Table' widget
        EXPECTED: * Widget expands downwards to show full League Table
        EXPECTED: * 'Show All' changes to 'Show Less'
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
        EXPECTED: 'eventLabel' : 'show full table'
        EXPECTED: })
        """
        pass

    def test_005_click_on_show_less_button_at_the_footer_on_league_table_widget(self):
        """
        DESCRIPTION: Click on 'Show Less' button at the footer on 'League Table' widget
        EXPECTED: * Widget collapses to show first 5 teams
        EXPECTED: * 'Show Less' changes to 'Show All'
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * Tracking is NOT applied for clicking on 'Show Less' button
        EXPECTED: * There are no data related to 'League Table' widget in 'dataLayer' after clicking on 'Show Less' button
        """
        pass

    def test_007_repeat_steps_3_4_one_more_time(self):
        """
        DESCRIPTION: Repeat steps 3-4 one more time
        EXPECTED: * Tracking is applied only for the first click
        EXPECTED: * There are no data related to 'League Table' widget in 'dataLayer' after the second/third/etc. click on 'Show All' button
        """
        pass
