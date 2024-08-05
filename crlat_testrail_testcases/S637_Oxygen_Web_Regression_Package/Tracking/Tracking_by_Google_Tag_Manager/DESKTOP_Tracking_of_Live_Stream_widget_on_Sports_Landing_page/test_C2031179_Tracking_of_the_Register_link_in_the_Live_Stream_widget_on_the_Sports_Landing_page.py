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
class Test_C2031179_Tracking_of_the_Register_link_in_the_Live_Stream_widget_on_the_Sports_Landing_page(Common):
    """
    TR_ID: C2031179
    NAME: Tracking of the 'Register' link in the 'Live Stream' widget on the Sports Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Register' link in the 'Live Stream' widget on the Sports Landing page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. User is NOT logged in
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
        EXPECTED: * '**Login** or **Register** to watch live stream now' message is displayed in expanded 'Live Stream' widget
        """
        pass

    def test_003_click_on_register_link_at_the_footer_in_live_stream_widget(self):
        """
        DESCRIPTION: Click on "Register" link at the footer in 'Live Stream' widget
        EXPECTED: 'Registration' page is opened
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'widget',
        EXPECTED: 'eventAction': 'watch live',
        EXPECTED: 'eventLabel': 'register link',
        EXPECTED: 'sport': '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_005_click_back_button(self):
        """
        DESCRIPTION: Click 'Back' button
        EXPECTED: User is back to the previous page (Sports Landing page in this case)
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_5_for_another_sport(self):
        """
        DESCRIPTION: Repeat steps 2-5 for another Sport
        EXPECTED: 
        """
        pass
