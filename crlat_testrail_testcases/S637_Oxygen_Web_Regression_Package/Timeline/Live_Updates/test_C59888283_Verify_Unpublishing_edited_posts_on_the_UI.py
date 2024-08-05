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
class Test_C59888283_Verify_Unpublishing_edited_posts_on_the_UI(Common):
    """
    TR_ID: C59888283
    NAME: Verify Unpublishing edited posts on the UI
    DESCRIPTION: This test case verify displaying content on the UI
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Confluence instruction - How to create Timeline Template, Campaign,
    PRECONDITIONS: Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+
    PRECONDITIONS: Template%2C+Campaign+and+Posts (TBD)
    PRECONDITIONS: 3.Timeline should be enabled in CMS (CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox)
    PRECONDITIONS: 4.Timeline should be turned ON in the general System configuration (CMS
    PRECONDITIONS: ->'System configuration' ->'Structure' ->'Feature Toggle' section ->'Timeline')
    PRECONDITIONS: 5.Timeline is available for the configured pages in CMS (CMS ->'Timeline'
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field)
    PRECONDITIONS: 6.Live Campaign is created
    PRECONDITIONS: 7.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_create_and_publish_thepost_in_the_live_campaign(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the
        DESCRIPTION: Post in the Live Campaign
        EXPECTED: 1.Post should be created and
        EXPECTED: published
        EXPECTED: 2.Post should be displayed on the
        EXPECTED: UI Timeline
        """
        pass

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline should be displayed at the bottom of the page, above
        EXPECTED: Footer menu
        """
        pass

    def test_003_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: 1.Page should be opened with
        EXPECTED: published post
        EXPECTED: 2.Content should be same as in CMS
        EXPECTED: 3.In WS 'Post' response should be present with all fields from CMS
        """
        pass

    def test_004_go_to_cms_and_click_unpublish_button(self):
        """
        DESCRIPTION: Go to CMS and click 'Unpublish' button
        EXPECTED: 1.Changes should be saved
        EXPECTED: 2.Post should be Unpublished
        """
        pass

    def test_005_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: 1.Page should be opened
        EXPECTED: 2.Unpublished post should not be present in the Timeline
        EXPECTED: 3.In WS 'POST_REMOVED' response should be present with fields
        """
        pass
