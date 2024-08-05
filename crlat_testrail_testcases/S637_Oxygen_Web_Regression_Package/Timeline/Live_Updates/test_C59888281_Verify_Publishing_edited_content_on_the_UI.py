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
class Test_C59888281_Verify_Publishing_edited_content_on_the_UI(Common):
    """
    TR_ID: C59888281
    NAME: Verify Publishing edited content on the  UI
    DESCRIPTION: This test case verify displaying content on the  UI
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 3.Timeline should be turned ON in the general System configuration
    PRECONDITIONS: (CMS -> 'System configuration' -> 'Structure' -> 'Feature Toggle' section ->
    PRECONDITIONS: 'Timeline')
    PRECONDITIONS: 4.Timeline is available for the configured pages in CMS (CMS -> 'Timeline'
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field)
    PRECONDITIONS: 5.Live Campaign is created
    PRECONDITIONS: 6.User is logged in
    PRECONDITIONS: 7.Confluence instruction - How to create Timeline Template, Campaign, Posts -
    PRECONDITIONS: 8.https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts (TBD)
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_campanig(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the post in the Live Campanig
        EXPECTED: Post should be created and
        EXPECTED: published
        """
        pass

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline should be displayed at
        EXPECTED: the bottom of the page, above
        EXPECTED: Footer menu
        """
        pass

    def test_003_click_on_the_timeline_bubblelads__ladbrokes_lounge_buttoncoral__coral_pulse_button(self):
        """
        DESCRIPTION: Click on the Timeline Bubble
        DESCRIPTION: Lads- 'Ladbrokes Lounge' button
        DESCRIPTION: Coral- 'Coral Pulse' button
        EXPECTED: 1.Page with the published post should be opened
        EXPECTED: 2.Content should be same as in CMS
        EXPECTED: 3.In WS 'POST' response should be present with all fields form CMS:
        """
        pass

    def test_004_go_to_cms_and_edit_verdictspotlightpost_and_edit_all_fields(self):
        """
        DESCRIPTION: Go to CMS and edit Verdict/Spotlight
        DESCRIPTION: post and edit all fields
        EXPECTED: -1.All fields except text is editable for
        EXPECTED: Verdict/Spotlight post
        EXPECTED: 2.Changes should be saved
        EXPECTED: 3.Post should be Published
        """
        pass

    def test_005_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: 1.Page should be opened with
        EXPECTED: published post
        EXPECTED: 2.Content should be same as in CMS
        EXPECTED: 3.In WS 'POST_CHANGED' response
        EXPECTED: should be present with fields
        """
        pass

    def test_006_go_to_cms_and_edit_simple_post___edit_all_fields_and_click_save_and_publish_button(self):
        """
        DESCRIPTION: Go to CMS and edit simple post - edit all fields and click 'Save and Publish' button
        EXPECTED: All fields should be editable for
        EXPECTED: post-Changes should be saved and Post should be Published
        """
        pass

    def test_007_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: 1.Page should be opened with
        EXPECTED: published post -Content should be same as in CMS
        EXPECTED: 2.In WS 'POST_CHANGED' response
        EXPECTED: should be present with fields
        """
        pass
