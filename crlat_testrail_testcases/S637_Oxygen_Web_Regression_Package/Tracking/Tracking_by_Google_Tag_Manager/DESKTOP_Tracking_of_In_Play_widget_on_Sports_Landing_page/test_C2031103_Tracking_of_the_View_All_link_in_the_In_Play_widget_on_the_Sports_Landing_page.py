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
class Test_C2031103_Tracking_of_the_View_All_link_in_the_In_Play_widget_on_the_Sports_Landing_page(Common):
    """
    TR_ID: C2031103
    NAME: Tracking of the 'View All' link in the 'In-Play' widget on the Sports Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'View All' link in the 'In-Play' widget on the Sports Landing page.
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

    def test_002_navigate_to_the_sports_landing_page_with_available_live_events(self):
        """
        DESCRIPTION: Navigate to the 'Sports' Landing page with available live events
        EXPECTED: * 'Sports' Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * 'In-Play' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_003_click_on_view_all_link_at_the_footer_in_in_play_widget_in_case_if_only_one_live_event_is_available(self):
        """
        DESCRIPTION: Click on "View All" link at the footer in 'In-Play' widget in case if only one live event is available
        EXPECTED: * 'In-Play' page is opened with selected 'All Sports' icon
        EXPECTED: * The list of live events is displayed
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'view all',
        EXPECTED: 'sport' : '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_005_click_on_view_all_link_at_the_footer_in_case_if_1_live_events_are_available(self):
        """
        DESCRIPTION: Click on "View All" link at the footer in case if >1 live events are available
        EXPECTED: * 'In-Play' page is opened with selected particular 'Sports' icon
        EXPECTED: * The list of live events is displayed
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'view all',
        EXPECTED: 'sport' : '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_007_repeat_steps_2_6_for_another_sport(self):
        """
        DESCRIPTION: Repeat steps 2-6 for another Sport
        EXPECTED: 
        """
        pass
