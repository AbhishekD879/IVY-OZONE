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
class Test_C2031105_Tracking_of_In_Play_widget_collapsing_on_the_Sports_Landing_page(Common):
    """
    TR_ID: C2031105
    NAME: Tracking of 'In-Play' widget collapsing on the Sports Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when collapsing the 'In-Play' widget on Sports Landing page.
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

    def test_003_click_on_in_play_widgets_header_to_collapse_it(self):
        """
        DESCRIPTION: Click on 'In-Play' widget's Header to collapse it
        EXPECTED: Header accordion is collapsed and widget content is hidden
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'collapse',
        EXPECTED: 'sport' : '<< SPORT >>'
        EXPECTED: })
        """
        pass

    def test_005_click_on_in_play_widgets_header_to_expand_it(self):
        """
        DESCRIPTION: Click on 'In-Play' widget's Header to expand it
        EXPECTED: Header accordion is expanded and widget content is visible
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * Tracking is NOT applied for widget expanding
        EXPECTED: * There are no data related to 'In-Play' widget in 'dataLayer' after expanding of it
        """
        pass

    def test_007_repeat_steps_3_4_one_more_time(self):
        """
        DESCRIPTION: Repeat steps 3-4 one more time
        EXPECTED: * Tracking is applied only for the first click
        EXPECTED: * There are no data related to 'In-Play' widget in 'dataLayer' after the second/third/etc. click on 'Show More' button
        """
        pass

    def test_008_repeat_steps_2_7_but_for_another_sport(self):
        """
        DESCRIPTION: Repeat steps 2-7 but for another Sport
        EXPECTED: 
        """
        pass
