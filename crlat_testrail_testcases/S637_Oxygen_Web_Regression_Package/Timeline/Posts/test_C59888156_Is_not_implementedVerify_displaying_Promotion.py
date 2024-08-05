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
class Test_C59888156_Is_not_implementedVerify_displaying_Promotion(Common):
    """
    TR_ID: C59888156
    NAME: [Is not implemented]Verify displaying Promotion
    DESCRIPTION: This test case verifies displaying Promotion
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.User is logged in
    PRECONDITIONS: 5.Confluence instruction - How to create Timeline Template, Campaign, Posts-https://confluence.egalacoral.com/display/SPI/Creating+Timeline+
    PRECONDITIONS: Template%2C+Campaign+and+Posts (TBD)
    PRECONDITIONS: Note:
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    PRECONDITIONS: Desktop means Mobile Emulator"
    """
    keep_browser_open = True

    def test_001_go_to_cms___timeline___timeline_campaign____create_and_publish_posts__with_the_following_configuration1_icon_stats_price_boost__or_sports_specific_like_horse_racing_football_should_be_configured_in_template2_show_timestamp_should_be_configured_in_template3_header_text_eg_priceboost4_text_short_description_of_promotions(self):
        """
        DESCRIPTION: Go to CMS -> Timeline -> Timeline Campaign ->
        DESCRIPTION: -> Create and Publish Posts  with the following configuration:
        DESCRIPTION: 1. Icon (stats, Price boost , or sports specific like horse racing, football) *(should be configured in Template)*
        DESCRIPTION: 2. Show Timestamp *(should be configured in Template)*
        DESCRIPTION: 3. Header Text: e.g Priceboost
        DESCRIPTION: 4. Text: short description of promotions
        EXPECTED: Post is successfully created and published
        """
        pass

    def test_002_load_the_app___login____navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -> Login ->
        DESCRIPTION: -> Navigate to the page with configured 'Timeline' (e.g./home/featured)
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

    def test_004_verify_displaying_newly_created_results_post(self):
        """
        DESCRIPTION: Verify displaying newly created results post
        EXPECTED: Results post is displayed as per designs:
        EXPECTED: - Icon (stats, Price boost , or sports specific like horse racing, football)
        EXPECTED: - Timestamp to show age of the post : e.g 23 Min
        EXPECTED: - Title: Title of promotion e.g Priceboost
        EXPECTED: - Description: Short description of promotions
        EXPECTED: ![](index.php?/attachments/get/118677255)
        """
        pass
