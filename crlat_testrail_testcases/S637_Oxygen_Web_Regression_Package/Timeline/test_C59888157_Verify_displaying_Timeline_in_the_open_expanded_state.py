import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.timeline
@vtest
class Test_C59888157_Verify_displaying_Timeline_in_the_open_expanded_state(Common):
    """
    TR_ID: C59888157
    NAME: Verify displaying Timeline  in the open (expanded) state
    DESCRIPTION: This test case verifies Timeline in the open (expanded) state
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline
    PRECONDITIONS: should be turned ON in the general System configuration ( CMS -> 'System
    PRECONDITIONS: configuration' -> 'Structure' -> 'Feature Toggle' section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline'
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field )
    PRECONDITIONS: Note: User can add multiple Page URL's to the list but manually need to refresh the page or app to see the reflected changes.
    PRECONDITIONS: 4.Posts should be also created in the CMS
    PRECONDITIONS: 5.Zeplin Links- https://app.zeplin.io/project/5dc59d1d83c70b83632
    PRECONDITIONS: e749c/screen/5fc90fbd08b6a9505bdfe043(Ladbrokes)
    PRECONDITIONS: https://app.zeplin.io/project/5dc59d1d83c70b83632e749c?seid=5fc912c1dc7b8e4f009ea750(Coral)
    PRECONDITIONS: 6.Load the app
    PRECONDITIONS: 7.User is logged in
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_1navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: 1.Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline should be displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline should be opened and displayed in the expanded state
        """
        pass

    def test_003_verify_timeline_in_the_expanded_state(self):
        """
        DESCRIPTION: Verify Timeline in the expanded state
        EXPECTED: 1.The following attributes should be
        EXPECTED: displayed in the Timeline header:
        EXPECTED: 2. a.Ladbrokes Lounge' text on the left side of the header
        EXPECTED: b. Coral Pulse' text on the left side of the header
        EXPECTED: 3.'Minimise' text on the right side of the header across both the brands
        EXPECTED: 4.Timeline has dark background at the top, left/right sides
        EXPECTED: 5.Configured posts are displayed on the white background
        EXPECTED: 6. For Ladbrokes- An icon LL will be displayed in the background.
        EXPECTED: For Coral-  A plain Blue background will be displayed at the back.
        """
        pass

    def test_004_verify_timeline_view_for_the_mostrecent_post_1st_post_in_the_list(self):
        """
        DESCRIPTION: Verify Timeline view for the Most
        DESCRIPTION: Recent Post (1st Post in the list)
        EXPECTED: The Most Recent Post (1st Post in
        EXPECTED: the list) should be displayed with a rounded edge
        """
        pass

    def test_005_scroll_down_to_the_next_posts_on_thetimeline_page(self):
        """
        DESCRIPTION: Scroll down to the next Posts on the
        DESCRIPTION: Timeline page
        EXPECTED: The next posts should be displayed with a straight edge
        """
        pass
