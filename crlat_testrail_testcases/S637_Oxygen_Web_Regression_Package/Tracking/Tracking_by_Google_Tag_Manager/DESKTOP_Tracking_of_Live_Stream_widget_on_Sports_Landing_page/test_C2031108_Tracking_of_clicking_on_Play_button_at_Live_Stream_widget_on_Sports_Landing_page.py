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
class Test_C2031108_Tracking_of_clicking_on_Play_button_at_Live_Stream_widget_on_Sports_Landing_page(Common):
    """
    TR_ID: C2031108
    NAME: Tracking of clicking on 'Play' button at 'Live Stream' widget on Sports Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Play' button at 'Live Stream' widget on Sports Landing page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
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

    def test_003_click_on_play_button_on_live_stream_widget(self):
        """
        DESCRIPTION: Click on 'Play' button on 'Live Stream' widget
        EXPECTED: * User is taken to event details page where live streaming can be watched
        EXPECTED: * Streaming starts automatically on EDP
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'watch live',
        EXPECTED: 'eventLabel' : 'play',
        EXPECTED: 'sport' : '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_005_click_on_back_button_and_repeat_steps_3_4_one_more_time(self):
        """
        DESCRIPTION: Click on 'Back' button and repeat steps 3-4 one more time
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_2_5_but_for_another_sport(self):
        """
        DESCRIPTION: Repeat steps 2-5 but for another Sport
        EXPECTED: 
        """
        pass
