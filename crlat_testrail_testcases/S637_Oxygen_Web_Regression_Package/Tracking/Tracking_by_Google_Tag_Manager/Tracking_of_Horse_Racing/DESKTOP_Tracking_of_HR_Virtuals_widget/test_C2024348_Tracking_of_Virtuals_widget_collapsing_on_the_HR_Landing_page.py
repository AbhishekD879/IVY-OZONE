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
class Test_C2024348_Tracking_of_Virtuals_widget_collapsing_on_the_HR_Landing_page(Common):
    """
    TR_ID: C2024348
    NAME: Tracking of 'Virtuals' widget collapsing on the HR Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when collapsing the 'Virtuals' widget on HR Landing page.
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

    def test_002_navigate_to_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' Landing page
        EXPECTED: 'Horse Racing' Landing page is opened
        """
        pass

    def test_003_scroll_the_page_down_to_the_inspired_virtuals_widget(self):
        """
        DESCRIPTION: Scroll the page down to the inspired 'Virtuals' widget
        EXPECTED: Inspired 'Virtuals' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_004_click_on_virtuals_widgets_header_to_collapse_it(self):
        """
        DESCRIPTION: Click on 'Virtuals' widget's Header to collapse it
        EXPECTED: Header accordion is collapsed and widget content is hidden
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'virtuals',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_006_click_on_virtuals_widgets_header_to_expand_it(self):
        """
        DESCRIPTION: Click on 'Virtuals' widget's Header to expand it
        EXPECTED: Header accordion is expanded and widget content is visible
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * Tracking is NOT applied for widget expanding
        EXPECTED: * There are no data related to 'Virtuals' widget in 'dataLayer' after expanding of it
        """
        pass

    def test_008_repeat_steps_4_5_one_more_time(self):
        """
        DESCRIPTION: Repeat steps 4-5 one more time
        EXPECTED: * Tracking is applied only for the first click
        EXPECTED: * There are no data related to 'Virtuals' widget in 'dataLayer' after the second/third/etc. click on widget header for collapsing it
        """
        pass
