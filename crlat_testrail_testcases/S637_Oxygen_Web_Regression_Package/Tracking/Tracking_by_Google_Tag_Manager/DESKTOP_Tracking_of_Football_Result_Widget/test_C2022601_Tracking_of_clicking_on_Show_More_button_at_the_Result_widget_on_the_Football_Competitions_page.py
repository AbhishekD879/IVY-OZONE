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
class Test_C2022601_Tracking_of_clicking_on_Show_More_button_at_the_Result_widget_on_the_Football_Competitions_page(Common):
    """
    TR_ID: C2022601
    NAME: Tracking of clicking on 'Show More' button at the 'Result' widget on the Football Competitions page
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

    def test_002_navigate_to_football_competitions_details_page_with_available_result_widget(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page with available 'Result' widget
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Results' Widget is displayed in 3rd column or below main content (depends on screen resolution)
        EXPECTED: * Maximum 3 events are displayed in 'Result' widget
        EXPECTED: * 'Show More' button is displayed below the last event in widget's footer
        """
        pass

    def test_003_click_on_show_more_button_at_the_footer_on_result_widget(self):
        """
        DESCRIPTION: Click on 'Show More' button at the footer on 'Result' widget
        EXPECTED: * Previous and 8 more events are displayed
        EXPECTED: * 'Show More' button is still present below the last event if there are more events
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'results',
        EXPECTED: 'eventLabel' : 'show more'
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_several_times(self):
        """
        DESCRIPTION: Repeat steps 3-4 several times
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'results',
        EXPECTED: 'eventLabel' : 'show more'
        EXPECTED: })
        """
        pass
