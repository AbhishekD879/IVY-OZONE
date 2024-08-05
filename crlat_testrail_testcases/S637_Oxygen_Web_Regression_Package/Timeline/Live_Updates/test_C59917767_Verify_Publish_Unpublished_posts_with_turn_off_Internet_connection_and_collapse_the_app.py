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
class Test_C59917767_Verify_Publish_Unpublished_posts_with_turn_off_Internet_connection_and_collapse_the_app(Common):
    """
    TR_ID: C59917767
    NAME: Verify Publish/Unpublished posts with turn off Internet connection and collapse the app
    DESCRIPTION: This test case verifies Publish/Unpublished posts with low internet connection
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

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_campaign(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the post in the Live Campaign
        EXPECTED: 1.Post should be created and
        EXPECTED: published -It should be displayed on the UI Timeline
        """
        pass

    def test_002_navigate_to_the_page_with_configuredtimeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured
        DESCRIPTION: 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline should be displayed at the bottom of the page, above
        EXPECTED: Footer menu
        """
        pass

    def test_003_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: 1.Page should be opened with published post and the Content should be same as in CMS
        EXPECTED: 2.In WS 'Post' response should be present with all fields from CMS
        """
        pass

    def test_004_in_device_turn_off_wi_fimobile_data(self):
        """
        DESCRIPTION: In device turn off Wi-Fi/Mobile Data
        EXPECTED: Wi-Fi/ Mobile data should be turned
        EXPECTED: off
        """
        pass

    def test_005_go_to_cms_and_click_publish_or_unpublish_button(self):
        """
        DESCRIPTION: Go to CMS and click 'Publish' or 'Unpublish' button
        EXPECTED: 1.Changes should be saved
        EXPECTED: 2.Post should be Unpublished/
        EXPECTED: Published
        """
        pass

    def test_006_in_device_turn_on_wi_fimobile_data(self):
        """
        DESCRIPTION: In device turn on Wi-Fi/Mobile Data
        EXPECTED: Wi-Fi/ Mobile data should be turned
        EXPECTED: on
        """
        pass

    def test_007_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: 1.Post Page should be opened
        EXPECTED: 2.Unpublished post should not be present in the Timeline
        EXPECTED: 3.Published post should be present in the Timeline
        EXPECTED: 4.In WS updates should be present
        """
        pass

    def test_008_ollapse_the_app_in_the_background_and_wait_2_3_min(self):
        """
        DESCRIPTION: Сollapse the app in the background and wait 2-3 min
        EXPECTED: app is collapsed
        """
        pass

    def test_009_go_to_cms_and_click_publish_or_unpublish_button(self):
        """
        DESCRIPTION: Go to CMS and click 'Publish' or 'Unpublish' button
        EXPECTED: 1.Changes should be saved
        EXPECTED: 2.Post should be Unpublished/
        EXPECTED: Published
        """
        pass

    def test_010_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: 1.Post Page should be opened
        EXPECTED: 2.Unpublished post should not be present in the Timeline
        EXPECTED: 3.Published post should be present in the Timeline
        EXPECTED: 4.In WS updates should be present
        """
        pass
