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
class Test_C2031104_Tracking_of_clicking_on_Right_Left_Navigation_arrow_at_In_Play_widget_on_Sports_Landing_page(Common):
    """
    TR_ID: C2031104
    NAME: Tracking of clicking on Right/Left Navigation arrow at 'In-Play' widget on Sports Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on Right/Left Navigation arrow at 'In-Play' widget on Sports Landing page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
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

    def test_003_hover_the_mouse_over_event_cards_in_in_play_widget_and_click_on_the_right_navigation_arrow(self):
        """
        DESCRIPTION: Hover the mouse over event cards in 'In-Play' widget and click on the Right Navigation Arrow
        EXPECTED: Event cards are swiped to the left side
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'widget',
        EXPECTED: 'eventAction': 'in play',
        EXPECTED: 'eventLabel': 'navigate right',
        EXPECTED: 'sport': '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_005_hover_the_mouse_over_event_cards_in_in_play_widget_and_click_on_the_left_navigation_arrow(self):
        """
        DESCRIPTION: Hover the mouse over event cards in 'In-Play' widget and click on the Left Navigation Arrow
        EXPECTED: Event cards are swiped to the right side
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'widget',
        EXPECTED: 'eventAction': 'in play',
        EXPECTED: 'eventLabel': 'navigate left',
        EXPECTED: 'sport': '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_007_repeat_steps_3_6_several_times(self):
        """
        DESCRIPTION: Repeat steps 3-6 several times
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_6_but_for_another_sport(self):
        """
        DESCRIPTION: Repeat steps 2-6 but for another Sport
        EXPECTED: 
        """
        pass
