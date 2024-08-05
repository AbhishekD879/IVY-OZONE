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
class Test_C2031418_Tracking_of_clicking_on_Right_Left_Navigation_arrow_in_Next_Races_widget_on_the_HR_Landing_page(Common):
    """
    TR_ID: C2031418
    NAME: Tracking of clicking on Right/Left Navigation arrow in 'Next Races' widget on the HR Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on Right/Left Navigation arrow in 'Next Races' widget on the HR Landing page.
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

    def test_002_navigate_to_the_horse_racing_landing_page_and_make_sure_that_next_races_widget_contains_several_event_cards_for_example_4(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' Landing page and make sure that 'Next Races' widget contains several event cards (for example 4)
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'Next Races' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_003_hover_the_mouse_over_event_cards_in_next_races_widget_and_click_on_the_right_navigation_arrow(self):
        """
        DESCRIPTION: Hover the mouse over event cards in 'Next Races' widget and click on the Right Navigation Arrow
        EXPECTED: Event cards are swiped to the left side
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'next races',
        EXPECTED: 'eventLabel' : 'navigate right'
        EXPECTED: })
        """
        pass

    def test_005_hover_the_mouse_over_event_cards_in_next_races_widget_and_click_on_the_left_navigation_arrow(self):
        """
        DESCRIPTION: Hover the mouse over event cards in 'Next Races' widget and click on the Left Navigation Arrow
        EXPECTED: Event cards are swiped to the right side
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'widget',
        EXPECTED: 'eventAction': 'next races',
        EXPECTED: 'eventLabel': 'navigate left'
        EXPECTED: })
        """
        pass

    def test_007_repeat_steps_3_6_several_times(self):
        """
        DESCRIPTION: Repeat steps 3-6 several times
        EXPECTED: 
        """
        pass
