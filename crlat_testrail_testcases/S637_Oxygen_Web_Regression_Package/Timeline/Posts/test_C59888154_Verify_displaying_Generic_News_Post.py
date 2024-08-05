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
class Test_C59888154_Verify_displaying_Generic_News_Post(Common):
    """
    TR_ID: C59888154
    NAME: Verify displaying Generic News Post
    DESCRIPTION: This test case verifies displaying Horse Racing Result Post
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_go_to_cms__gt_timeline__gt_timeline_campaign__gt_gt_create_and_publish_posts_with_the_following_configuration1_sport_icon_select_from_list_of_available_icons_eg_horse_racing_football_should_be_configured_in_template2_show_timestamp_should_be_configured_in_template3_header_text_eg_canford_can4_sub_header_optional__eg_harry_kane_9mins5_text_eg_three_favourites_have_(self):
        """
        DESCRIPTION: Go to CMS -&gt; Timeline -&gt; Timeline Campaign -&gt;
        DESCRIPTION: -&gt; Create and Publish Posts with the following configuration:
        DESCRIPTION: 1. Sport Icon (Select from list of available icons e.g horse racing, football) *(should be configured in Template)*
        DESCRIPTION: 2. Show Timestamp *(should be configured in Template)*
        DESCRIPTION: 3. Header Text: e.g CANFORD CAN
        DESCRIPTION: 4. Sub Header (Optional) : e.g Harry Kane (9mins)
        DESCRIPTION: 5. Text: e.g Three favourites have ….."
        EXPECTED: Post is successfully created and published
        """
        pass

    def test_002_load_the_app__gt_login__gt_gt_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -&gt; Login -&gt;
        DESCRIPTION: -&gt; Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_003_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - **Newly created posts on CMS appears instantly on the frontend**
        """
        pass

    def test_004_verify_displaying_newly_created_generic_news_post(self):
        """
        DESCRIPTION: Verify displaying newly created Generic News post
        EXPECTED: Generic News post is displayed as per designs:
        EXPECTED: - Sport Icon (Select from list of available icons e.g horse racing, football)
        EXPECTED: - Timestamp to show age of the post : e.g 23 Min
        EXPECTED: - Title: e.g CANFORD CAN
        EXPECTED: - Sub Header (Optional) : e.g Harry Kane (9mins)
        EXPECTED: - Description: e.g Three favourites have …..
        EXPECTED: ![](index.php?/attachments/get/118677252)
        """
        pass
