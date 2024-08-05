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
class Test_C1232390_Tracking_of_View_All_YourCall_specials_link_clicks(Common):
    """
    TR_ID: C1232390
    NAME: Tracking of “View All YourCall specials” link clicks
    DESCRIPTION: This test case verifies GA tracking of “View All YourCall specials” link clicks.
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_on_horse_racing_landing_page_scroll_to_yourcall_specials_module_click_on_view_all_yourcall_specials_link(self):
        """
        DESCRIPTION: On Horse Racing landing page scroll to YourCall Specials module .
        DESCRIPTION: Click on “View All YourCall specials” link.
        EXPECTED: --
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'your call',
        EXPECTED: 'eventLabel' : 'more your call specials'
        EXPECTED: })
        """
        pass
