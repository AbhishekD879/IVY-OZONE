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
class Test_C1992658_Tracking_of_headerfooter_menu_navigation_items(Common):
    """
    TR_ID: C1992658
    NAME: Tracking of header&footer menu navigation items
    DESCRIPTION: This test case verifies tracking in Google Analytics clicking on Sports Menu navigation items on Home page
    DESCRIPTION: Should be covered on Mobile, Tablet and Wrappers
    PRECONDITIONS: - Oxygen app is loaded > Home page is opened
    PRECONDITIONS: - Browser Console is opened
    """
    keep_browser_open = True

    def test_001_click_on_any_sports_menu_navigation_items_eg_in_play_all_sports_etc(self):
        """
        DESCRIPTION: Click on any Sports menu navigation items (e.g. In-Play, All Sports etc)
        EXPECTED: Corresponding page is opened
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press 'Enter'
        EXPECTED: The following tracking record is available:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'main',
        EXPECTED: 'eventLabel' : '<< NAVIGATION ITEM >>'  e.g. In-Play, All Sports etc
        EXPECTED: });
        """
        pass

    def test_003_click_on_any_footer_menu_navigation_items_eg_home_all_sports_in_play_etc(self):
        """
        DESCRIPTION: Click on any Footer menu navigation items (e.g. Home, All Sports, In Play etc)
        EXPECTED: Corresponding page is opened
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press 'Enter'
        EXPECTED: The following tracking record is available:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'footer',
        EXPECTED: 'eventLabel' : '<< NAVIGATION ITEM >>' e.g. Home, All Sports, In Play etc
        EXPECTED: });
        """
        pass

    def test_005_repeat_steps_1_4_for_a_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-4 for a logged in user
        EXPECTED: 
        """
        pass
