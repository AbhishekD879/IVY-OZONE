import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29413_Verify_Race_events_carousel_UI(Common):
    """
    TR_ID: C29413
    NAME: Verify <Race> events carousel UI
    DESCRIPTION: This test case is for checking UI for <Race> events carousel of module created by <Race> type ID within Featured tab
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: * 'Feature' tab is selected by default
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_004_verify_race_events_carousel_within_verified_module(self):
        """
        DESCRIPTION: Verify <Race> events carousel within verified module
        EXPECTED: <Race> events carousel is displayed below the module header
        """
        pass

    def test_005_verify_width_of_race_events_carousel(self):
        """
        DESCRIPTION: Verify width of <Race> events carousel
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: Fixed width of <Race> events carousel is equal to 270 pixels in portrait and landscape modes
        EXPECTED: **For Desktop:**
        EXPECTED: The width of <Race> events carousel depends on screen resolution and changes the size accordingly
        """
        pass

    def test_006_check_swipinghorizontal_scrolling_between_events_when_there_are_two_or_more_events(self):
        """
        DESCRIPTION: Check swiping/horizontal scrolling between events when there are **Two or more events**
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: *   It is possible to move between events using swiping
        EXPECTED: *   Swiping is fulfilled fluently
        EXPECTED: *   The previous race is not shown when user swipes across the <Race> module
        EXPECTED: *   The next race is shown when user swipes across the <Race> module
        EXPECTED: **For Desktop:**
        EXPECTED: *   It is possible to move between events using Navigation arrows that appear when hovering the mouse over items
        EXPECTED: *   Current visible 'X' race cards will be replaced by following next 'X' races (for example displaying 4 by 4 cards)
        """
        pass

    def test_007_check_swipinghorizontal_scrolling_within_module_when_there_is_justone_event(self):
        """
        DESCRIPTION: Check swiping/horizontal scrolling within module when there is just **one event**
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: *   It is not possible to swipe within module
        EXPECTED: *   Event is shown in the way to cover all width of the module
        EXPECTED: **For Desktop:**
        EXPECTED: * It is NOT possible to move between events
        EXPECTED: * Navigation arrows don't appear when hovering the mouse over items
        """
        pass

    def test_008_try_to_collapse_verified_race_module(self):
        """
        DESCRIPTION: Try to collapse verified <Race> module
        EXPECTED: <Race> module is expandable/collapsible
        """
        pass

    def test_009_verify_case_where_there_are_no_valid_events_to_show(self):
        """
        DESCRIPTION: Verify case where there are no valid events to show
        EXPECTED: Configured <Race> module is absent
        """
        pass

    def test_010_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: *   Default number of selections is 3
        EXPECTED: *   If number of selections is less than 3 -> display the remaining selections
        """
        pass

    def test_011_verify_more_link(self):
        """
        DESCRIPTION: Verify 'More' link
        EXPECTED: Link is shown at right-top corner
        """
        pass
