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
class Test_C59892776_Verify_displaying_Timeline_in_the_open_expanded_state_if_there_are_no_LIVE_Campaign_Posts_available(Common):
    """
    TR_ID: C59892776
    NAME: Verify displaying Timeline in the open (expanded) state if there are no LIVE Campaign/Posts available
    DESCRIPTION: This test case verifies Timeline in the open (expanded) state if there are no LIVE Campaign/Posts available
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline
    PRECONDITIONS: should be turned ON in the general System configuration ( CMS -> 'System
    PRECONDITIONS: configuration' -> 'Structure' -> 'Feature Toggle' section -> 'Timeline')
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS (CMS -> 'Timeline
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field)
    PRECONDITIONS: 4.There is NO LIVE Campaign available in CMS
    PRECONDITIONS: 5.NOTE: Posts are available only for LIVE Campaign
    PRECONDITIONS: 6.ONLY 1 LIVE Campaign can be created in CMS
    PRECONDITIONS: 7.User is logged in
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
        EXPECTED: Timeline should be opened and displayed in the expanded state
        """
        pass

    def test_003_verify_timeline_in_the_expanded_state_ifthere_is_no_live_campaign_available(self):
        """
        DESCRIPTION: Verify Timeline in the expanded state if
        DESCRIPTION: there is no LIVE Campaign available
        EXPECTED: 1.The following attributes should be displayed in the Timeline header:
        EXPECTED: 2.
        EXPECTED: a.'Ladbrokes Lounge' text on the left side of the header
        EXPECTED: b.'Coral Pulse' text on the left side of the header
        EXPECTED: 3.'Minimise' text on the right side of the header
        EXPECTED: 4.For Ladbrokes- An icon LL will be displayed in the background.
        EXPECTED: For Coral-  A plain Blue background will be displayed at the back.
        EXPECTED: 5.Timeline Response (wss://timelineapidev0.coralsports.dev.cloud.ladbrokescoral.com/socket.io/EIO=&transport=websocket) is NOT present in WS
        EXPECTED: 6.Empty 'Posts' section is displayed
        EXPECTED: 7.Posts are NOT displayed in the 'Posts' section in the Timeline
        """
        pass

    def test_004_navigate_to_cms__timeline__timelinecampaign__create_live_campaign(self):
        """
        DESCRIPTION: Navigate to CMS ->Timeline ->Timeline
        DESCRIPTION: Campaign ->Create LIVE Campaign
        EXPECTED: New LIVE Campaign should be
        EXPECTED: created
        """
        pass

    def test_005_return_to_the_posts_page_on_ui_andverify_timeline_in_the_expanded_state_iflive_campaign_is_available_withoutconfigured_and_published_posts(self):
        """
        DESCRIPTION: Return to the Posts page on UI and
        DESCRIPTION: Verify Timeline in the expanded state if
        DESCRIPTION: LIVE Campaign is available without
        DESCRIPTION: configured and Published Posts
        EXPECTED: 1.The following attributes should be displayed in the Timeline header:
        EXPECTED: 2.'Coral Pulse' text on the left side of the header
        EXPECTED: 3.'Minimise' text on the right side of the header
        EXPECTED: 4.For Ladbrokes- An icon LL will be displayed in the background.
        EXPECTED: For Coral-  A plain Blue background will be displayed at the back.
        EXPECTED: 5.Empty 'Posts' section is displayed
        EXPECTED: 6.Posts are NOT displayed in the 'Posts' section in the Timeline
        EXPECTED: 7.Empty 'POST_PAGE' attribute is received in WS response (wss://timelineapidev0.coralsports.dev.cloud.ladbrokescoral.com/socket.io/?EIO=&transport=WebSocket)
        """
        pass

    def test_006_onfigure_and_publish_the_posts(self):
        """
        DESCRIPTION: Сonfigure and Publish the Posts
        EXPECTED: Posts should be displayed in the 'Posts' section in the Timeline
        """
        pass

    def test_007_1return_to_the_cms___timeline___timeline_campaign2change_camping_status_from_live_to_openclose_3again_change_the_status_to_live(self):
        """
        DESCRIPTION: 1.Return to the CMS -> Timeline -> Timeline Campaign
        DESCRIPTION: 2.Change Camping status from "Live" to "Open/Close "
        DESCRIPTION: 3.Again change the status to "Live"
        EXPECTED: 1.All the posts should be unpublished in CMS.
        EXPECTED: 2.Empty 'Posts' section should be displayed in Front End.
        EXPECTED: 3.Posts should not be displayed in the 'Posts' section in the Timeline.
        """
        pass

    def test_008_in_cms_click_on_republish_posts_button_on_the_campaign_page(self):
        """
        DESCRIPTION: In CMS ,click on 'Republish Posts' button on the Campaign page
        EXPECTED: 1.In CMS all posts should be Republished
        EXPECTED: 2.On UI Posts should be displayed in the 'Posts' section in the Timeline
        """
        pass
