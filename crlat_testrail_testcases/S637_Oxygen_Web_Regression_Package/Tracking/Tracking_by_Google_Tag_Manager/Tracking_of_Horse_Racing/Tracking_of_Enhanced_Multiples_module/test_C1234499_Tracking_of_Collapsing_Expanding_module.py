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
class Test_C1234499_Tracking_of_Collapsing_Expanding_module(Common):
    """
    TR_ID: C1234499
    NAME: Tracking of Collapsing/Expanding module
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Collapse/Expand the Enhanced multiples Carousel module
    DESCRIPTION: AUTOTEST [C1952775]
    PRECONDITIONS: 1. Test case should be run on Mobile
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

    def test_003_scroll_down_to_enhanced_multiples_module(self):
        """
        DESCRIPTION: Scroll down to 'Enhanced multiples' module
        EXPECTED: 'Enhanced multiples' module is shown as carousel
        """
        pass

    def test_004_ollapse_the_enhanced_multiples_module(self):
        """
        DESCRIPTION: Сollapse the 'Enhanced multiples' module
        EXPECTED: Module is collapsed
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in Data Layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'enhanced multiples',
        EXPECTED: 'eventLabel' : 'collapse'
        """
        pass

    def test_006_expands_and_collapses_the_enhanced_multiples_module_one_more_time(self):
        """
        DESCRIPTION: Expands and collapses the 'Enhanced multiples' module one more time
        EXPECTED: Module is collapsed
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event is **NOT** present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'enhanced multiples',
        EXPECTED: 'eventLabel' : 'collapse'
        """
        pass

    def test_008_leave_the_page_and_come_back_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Leave the page and come back to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_009_ollapse_the_enhanced_multiples_module(self):
        """
        DESCRIPTION: Сollapse the 'Enhanced multiples' module
        EXPECTED: Module is collapsed
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'enhanced multiples',
        EXPECTED: 'eventLabel' : 'collapse'
        """
        pass

    def test_011_repeat_steps_1_10_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-10 for Logged In user
        EXPECTED: 
        """
        pass
