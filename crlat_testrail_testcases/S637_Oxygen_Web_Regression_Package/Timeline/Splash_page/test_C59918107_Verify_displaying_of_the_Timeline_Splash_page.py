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
class Test_C59918107_Verify_displaying_of_the_Timeline_Splash_page(Common):
    """
    TR_ID: C59918107
    NAME: Verify displaying of the Timeline Splash page
    DESCRIPTION: This test cases verifies displaying of Splash page for timeline
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.User is logged in
    PRECONDITIONS: 3.User haven't seen Splash page (OX.timelineTutorialOverlay is missed in the local storage)
    PRECONDITIONS: Toggles for Timeline:
    PRECONDITIONS: 4.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 5.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 6.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 7.Live Campaign is created
    PRECONDITIONS: 8.Toggle for Splash page is turned on (Timeline->Timeline Splash Page-> Show Splash Page : checked on)
    PRECONDITIONS: 9.All pop-ups are closed
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_navigate_to_page_where_timeline_is_configured(self):
        """
        DESCRIPTION: Navigate to page where timeline is configured
        EXPECTED: The tutorial page will be displayed at the end of the existing pop-up sequence
        """
        pass

    def test_002_verify_tutorial_ui(self):
        """
        DESCRIPTION: Verify Tutorial UI
        EXPECTED: Header styled as per design and content as configured in CMS
        EXPECTED: Phone svg icon as per design
        EXPECTED: Arrow svg icons as per design
        EXPECTED: Text bubbles as per design
        EXPECTED: Option to select 'X'
        """
        pass

    def test_003_tap_on_close_x_button(self):
        """
        DESCRIPTION: Tap on 'Close' ('X') button
        EXPECTED: The Tutorial page should be closed and user should see Timeline header
        """
        pass

    def test_004_refresh_page_where_timeline_is_configured(self):
        """
        DESCRIPTION: Refresh Page where timeline is configured
        EXPECTED: The tutorial page should not be shown
        """
        pass

    def test_005_navigate_to_application_local_storage__timeline_system_config_and_verify_campaignid(self):
        """
        DESCRIPTION: Navigate to application->Local storage-> Timeline System Config and verify campaignID
        EXPECTED: CampaignID should be the same as id for the live Campaign
        EXPECTED: Network-> WS-> wss://timeline-api-...->POST PAGE->page-> campaignId value
        """
        pass

    def test_006_remove_timelinetutorialoverlay_value_from_local_storage_and_refresh_the_page(self):
        """
        DESCRIPTION: Remove 'TimelineTutorialOverlay' value from local storage and refresh the page
        EXPECTED: The tutorial page should be displayed at the end of the existing pop-up sequence
        """
        pass

    def test_007_tap_on_the_ok_thanks_button(self):
        """
        DESCRIPTION: Tap on the 'Ok Thanks' button
        EXPECTED: The Tutorial page should be closed and user should see Timeline header
        """
        pass

    def test_008_go_to_cms_and_change_existing_campaign_to_new_oneandrefresh_ladbrokes_ui(self):
        """
        DESCRIPTION: Go to CMS and change existing campaign to new one
        DESCRIPTION: and
        DESCRIPTION: Refresh Ladbrokes UI
        EXPECTED: The tutorial page should be displayed at the end of the existing pop-up sequence
        """
        pass
