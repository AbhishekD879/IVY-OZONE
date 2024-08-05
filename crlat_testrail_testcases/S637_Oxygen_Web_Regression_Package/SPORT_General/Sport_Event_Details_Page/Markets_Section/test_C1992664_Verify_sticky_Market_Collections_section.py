import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1992664_Verify_sticky_Market_Collections_section(Common):
    """
    TR_ID: C1992664
    NAME: Verify sticky Market Collections section
    DESCRIPTION: This test case verifies sticky Market Collections section on Sport EDP
    PRECONDITIONS: * Test case is applicable to **Mobile** and **Tablet** only
    PRECONDITIONS: * User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_sport_event_details_page(self):
        """
        DESCRIPTION: Go to <Sport> Event Details page
        EXPECTED: * <Sport> Event Details page is opened
        EXPECTED: * List of market collections are displayed below event name and date
        """
        pass

    def test_003_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: * Market collections are sticky and displayed below <Sport> header
        EXPECTED: * Event name and date are NOT shown
        """
        pass

    def test_004_expandcollapse_any_market_panel(self):
        """
        DESCRIPTION: Expand/collapse any market panel
        EXPECTED: * Chosen market panel is expanded/collapsed
        EXPECTED: * Market collections remain sticky
        """
        pass

    def test_005_tap_any_collection_on_sticky_market_collections_section(self):
        """
        DESCRIPTION: Tap any collection on sticky Market collections section
        EXPECTED: * Particular market collection is opened with corresponding markets
        EXPECTED: * Page is auto-scrolled to the top of the market collection
        """
        pass

    def test_006_scroll_down_the_page_until_the_end_of_its_content(self):
        """
        DESCRIPTION: Scroll down the page until the end of its content
        EXPECTED: * Market collections is NOT displayed when no content is present
        EXPECTED: * Global Footer is displayed only
        """
        pass

    def test_007_log_in_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in and repeat steps #2-6
        EXPECTED: 
        """
        pass
