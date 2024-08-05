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
class Test_C2023953_Tracking_of_Result_widget_collapsing_on_the_Football_Competitions_page(Common):
    """
    TR_ID: C2023953
    NAME: Tracking of 'Result' widget collapsing on the Football Competitions page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when collapsing the 'Result' widget on the Football Competitions page.
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
        """
        pass

    def test_003_click_on_result_widgets_header_to_collapse_it(self):
        """
        DESCRIPTION: Click on 'Result' widget's Header to collapse it
        EXPECTED: Header accordion is collapsed and widget content is hidden
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
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_005_click_on_result_widgets_header_to_expand_it(self):
        """
        DESCRIPTION: Click on 'Result' widget's Header to expand it
        EXPECTED: Header accordion is expanded and widget content is visible
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * Tracking is NOT applied for widget expanding
        EXPECTED: * There are no data related to 'Result' widget in 'dataLayer' after expanding of it
        """
        pass

    def test_007_repeat_steps_3_4_one_more_time(self):
        """
        DESCRIPTION: Repeat steps 3-4 one more time
        EXPECTED: * Tracking is applied only for the first click
        EXPECTED: * There are no data related to 'Result' widget in 'dataLayer' after the second/third/etc. click on 'Show More' button
        """
        pass
