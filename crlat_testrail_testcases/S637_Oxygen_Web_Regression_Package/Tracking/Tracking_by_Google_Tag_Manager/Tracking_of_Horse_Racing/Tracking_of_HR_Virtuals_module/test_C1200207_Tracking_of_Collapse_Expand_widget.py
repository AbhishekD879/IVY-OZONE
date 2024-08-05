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
class Test_C1200207_Tracking_of_Collapse_Expand_widget(Common):
    """
    TR_ID: C1200207
    NAME: Tracking of Collapse/Expand widget
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Collapse/Expand the Virtuals X-Sell widget
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_scroll_down_to_the_inspired_virtuals_module(self):
        """
        DESCRIPTION: Scroll down to the inspired Virtuals module
        EXPECTED: Inspired Virtual' module is shown as carousel
        """
        pass

    def test_004_collapse_the_inspired_virtuals_module(self):
        """
        DESCRIPTION: Collapse the inspired Virtuals module
        EXPECTED: Inspired Virtual' module is shown collapsed
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'virtual horse racing',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_006_expend_and_collapse_the_inspired_virtuals_module_again(self):
        """
        DESCRIPTION: Expend and collapse the inspired Virtuals module again
        EXPECTED: 
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event is NOT present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'virtual horse racing',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_008_leave_the_page_and_come_back_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Leave the page and come back to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_009_collapse_the_inspired_virtuals_module(self):
        """
        DESCRIPTION: Collapse the inspired Virtuals module
        EXPECTED: 
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'virtual horse racing',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        pass

    def test_011_repeat_steps_1_10_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-10 for Logged In user
        EXPECTED: 
        """
        pass
