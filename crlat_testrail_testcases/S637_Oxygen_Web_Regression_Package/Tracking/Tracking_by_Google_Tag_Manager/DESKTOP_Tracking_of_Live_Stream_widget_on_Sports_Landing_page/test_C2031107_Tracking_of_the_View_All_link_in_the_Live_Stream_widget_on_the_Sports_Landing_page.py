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
class Test_C2031107_Tracking_of_the_View_All_link_in_the_Live_Stream_widget_on_the_Sports_Landing_page(Common):
    """
    TR_ID: C2031107
    NAME: Tracking of the 'View All' link in the 'Live Stream' widget on the Sports Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'View All' link in the 'Live Stream' widget on the Sports Landing page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_the_sports_landing_page_with_available_live_events_that_have_mapped_stream(self):
        """
        DESCRIPTION: Navigate to the 'Sports' Landing page with available live events that have mapped stream
        EXPECTED: * 'Sports' Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * 'Live Stream' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_003_click_on_view_all_link_at_the_footer_in_live_stream_widget(self):
        """
        DESCRIPTION: Click on "View All" link at the footer in 'Live Stream' widget
        EXPECTED: * 'Live Stream' page is opened
        EXPECTED: * The list of live events with the mapped stream is displayed
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'watch live',
        EXPECTED: 'eventLabel' : 'view all',
        EXPECTED: 'sport' : '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_2_4_for_another_sport(self):
        """
        DESCRIPTION: Repeat steps 2-4 for another Sport
        EXPECTED: 
        """
        pass