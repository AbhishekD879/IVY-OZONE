import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.timeline
@vtest
class Test_C59985458_Verify_Timeline_Infinite_scrolling(Common):
    """
    TR_ID: C59985458
    NAME: Verify Timeline Infinite scrolling
    DESCRIPTION: This test case verifies Timeline Infinite scrolling
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2. More than 20 posts should be created and published in the CMS
    PRECONDITIONS: 3. 'Initial number of messages to display' for Live Campaign should be less than 10
    PRECONDITIONS: 4.Load the app
    PRECONDITIONS: 5.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configuredtimeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured
        DESCRIPTION: 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline should be displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: 1.Timeline should be opened and displayed in the expanded state
        EXPECTED: 2.Timeline posts should be showed as configured in CMS due to 'Initial number of messages to display'
        """
        pass

    def test_003_scroll_down_to_the_next_posts_on_thetimeline_page(self):
        """
        DESCRIPTION: Scroll down to the next Posts on the
        DESCRIPTION: Timeline page
        EXPECTED: Older Post should be loaded
        """
        pass

    def test_004_swipe_gesture(self):
        """
        DESCRIPTION: Swipe gesture
        EXPECTED: Next set of posts (next ‘Initial number of messages to display’)
        EXPECTED: should be loaded
        """
        pass

    def test_005_verify_appearing_skeletons_for_posts_and_use_slow_network_connection_to_seeskeleton_for_longer_time_or_addbreakpoint_for_them_in_console_ofdev_tool(self):
        """
        DESCRIPTION: Verify appearing skeletons for posts and Use slow network connection to see
        DESCRIPTION: skeleton for longer time or add
        DESCRIPTION: breakpoint for them in console of
        DESCRIPTION: Dev tool
        EXPECTED: 1.Skeleton appears for few seconds (till post becomes available)
        EXPECTED: 2.Skeleton does not jump up and down and appears smoothly
        EXPECTED: 3.There is no extra space/area below/beneath the skeleton
        """
        pass

    def test_006_scroll_to_the_end_and_try_to_scroll_down(self):
        """
        DESCRIPTION: Scroll to the end and try to scroll down
        EXPECTED: 1.User should see a 'bounce' animation and the last available post.
        EXPECTED: Note: When we open the Timeline Bubble- posts are opened and the edges are curvy and when user scrolls to the bottom- it will be displayed in rectangular shape.
        """
        pass
