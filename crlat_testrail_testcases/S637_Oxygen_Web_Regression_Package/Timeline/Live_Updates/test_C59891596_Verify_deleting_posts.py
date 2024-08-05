import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@vtest
class Test_C59891596_Verify_deleting_posts(Common):
    """
    TR_ID: C59891596
    NAME: Verify deleting posts
    DESCRIPTION: This test case verifies deleting posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 3.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 4.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 5.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 6.Live Campaign is created.
    PRECONDITIONS: 7.User is logged in app
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_campanig(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the post in the Live Campanig
        EXPECTED: Post should be created and published.
        """
        pass

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline should be displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_003_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: Page with the published post should be opened.Content is the same as in CMS.
        """
        pass

    def test_004_go_to_cms_and_delete_post(self):
        """
        DESCRIPTION: Go to CMS and delete post
        EXPECTED: Post should be deleted.
        """
        pass

    def test_005_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: Page should be opened.
        EXPECTED: Deleted post should not be present in the Timeline.
        EXPECTED: In WS 'POST_REMOVED' response should be present with fields
        """
        pass
