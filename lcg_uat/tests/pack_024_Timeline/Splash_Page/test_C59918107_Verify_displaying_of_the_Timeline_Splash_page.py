import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.mobile_only
@pytest.mark.reg156_fix
@vtest
class Test_C59918107_Verify_displaying_of_the_Timeline_Splash_page(Common):
    """
    TR_ID: C59918107
    NAME: Verify displaying of the Timeline Splash page
    DESCRIPTION: This test cases verifies displaying of Splash page for timeline
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)-
                     Enter the total number of posts count and save it- The same count should be reflected in the FE
                     after page refresh in the FE.
    PRECONDITIONS: 2.User is logged in
    PRECONDITIONS: 3.User haven't seen Splash page (OX.timelineTutorialOverlay is missed in the local storage)

    PRECONDITIONS: Toggles for Timeline:
    PRECONDITIONS: 4.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item ->
                         'Enabled' checkbox )
    PRECONDITIONS: 5.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration'
                    -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 6.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section ->
                    'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 7.Live Campaign is created
    PRECONDITIONS: 8.Toggle for Splash page is turned on (Timeline->Timeline Splash Page-> Show Splash Page :
                     checked on)
    PRECONDITIONS: 9.All pop-ups are closed
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: check and create timeline
        """
        if not self.cms_config.get_timeline_system_configuration()['enabled']:
            self.cms_config.update_timeline_system_config()
        self.__class__.live_campaign_id = self.get_timeline_campaign_id()
        self.assertTrue(self.live_campaign_id, msg='"Live campaign " is not available.')
        if not self.cms_config.get_timeline_splash_page()['showSplashPage']:
            raise CmsClientException('"Timeline Splash page" is disabled in CMS')

    def test_001_navigate_to_page_where_timeline_is_configured(self):
        """
        DESCRIPTION: Navigate to page where timeline is configured
        EXPECTED: The tutorial page will be displayed at the end of the existing pop-up sequence
        """
        self.site.login(timeline=True)
        self.assertTrue(self.site.timeline_tutorial_overlay.is_displayed(),
                        msg='"Timeline Tutorial Overlay" is not displayed')

    def test_002_verify_tutorial_ui(self):
        """
        DESCRIPTION: Verify Tutorial UI
        EXPECTED: Header styled as per design and content as configured in CMS
        EXPECTED: Phone svg icon as per design
        EXPECTED: Arrow svg icons as per design
        EXPECTED: Text bubbles as per design
        EXPECTED: Option to select 'X'
        """
        splash_page_title = self.site.timeline.timeline_splash_page.title
        self.assertTrue(splash_page_title, msg=' "Splash page title" is not displayed.')
        phone_svg_icon = self.site.timeline.timeline_splash_page.phone_svg
        self.assertTrue(phone_svg_icon, msg=' "Splash page phone svg icon" is not displayed.')
        left_bottom_arrow = self.site.timeline.timeline_splash_page.left_bottom_arrow
        self.assertTrue(left_bottom_arrow, msg=' "Splash page left bottom arrow" is not displayed.')
        right_bottom_arrow = self.site.timeline.timeline_splash_page.right_bottom_arrow
        self.assertTrue(right_bottom_arrow, msg=' "Splash page right bottom arrow" is not displayed.')
        left_top_arrow = self.site.timeline.timeline_splash_page.left_top_arrow
        self.assertTrue(left_top_arrow, msg=' "Splash page left top arrow" is not displayed.')
        self.__class__.close_button = self.site.timeline.timeline_splash_page.close_button
        self.assertTrue(self.close_button, msg=' "Close button" is not displayed.')

    def test_003_tap_on_close_x_button(self):
        """
        DESCRIPTION: Tap on 'Close' ('X') button
        EXPECTED: The Tutorial page should be closed and user should see Timeline header
        """
        self.close_button.click()
        self.assertFalse(self.site.root_app.has_timeline_overlay_tutorial(timeout=1, expected_result=False),
                         msg='"Timeline tutorial" is not displayed')
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(),
                        msg='"Timeline bubble" is not displayed')

    def test_004_refresh_page_where_timeline_is_configured(self):
        """
        DESCRIPTION: Refresh Page where timeline is configured
        EXPECTED: The tutorial page should not be shown
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertFalse(self.site.root_app.has_timeline_overlay_tutorial(timeout=1, expected_result=False),
                         msg='"Timeline tutorial" is displayed')

    def test_005_navigate_to_application_local_storage__timeline_system_config_and_verify_campaignid(self):
        """
        DESCRIPTION: Navigate to application->Local storage-> Timeline System Config and verify campaignID
        EXPECTED: CampaignID should be the same as id for the live Campaign
        EXPECTED: Network-> WS-> wss://timeline-api-...->POST PAGE->page-> campaignId value
        """
        timeline_overlay_cookie = self.get_local_storage_cookie_value(cookie_name="OX.timelineTutorialOverlay")
        self.assertIn(self.live_campaign_id, timeline_overlay_cookie,
                      msg=f'live campaign id :"{self.live_campaign_id}" is not in '
                          f'cookie : "{timeline_overlay_cookie}"')

    def test_006_remove_timelinetutorialoverlay_value_from_local_storage_and_refresh_the_page(self):
        """
        DESCRIPTION: Remove 'TimelineTutorialOverlay' value from local storage and refresh the page
        EXPECTED: The tutorial page should be displayed at the end of the existing pop-up sequence
        """
        self.delete_local_storage_cookie(cookie_name="OX.timelineTutorialOverlay")
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.root_app.has_timeline_overlay_tutorial(timeout=1, expected_result=True),
                        msg='"Timeline tutorial" is not displayed')

    def test_007_tap_on_the_ok_thanks_button(self):
        """
        DESCRIPTION: Tap on the 'Ok Thanks' button
        EXPECTED: The Tutorial page should be closed and user should see Timeline header
        """
        self.site.timeline.timeline_splash_page.ok_thanks_button.click()
        self.assertFalse(self.site.root_app.has_timeline_overlay_tutorial(timeout=1, expected_result=False),
                         msg='"Timeline tutorial" is displayed')
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(),
                        msg='"Timeline Bubble" is not displayed')

    def test_008_go_to_cms_and_change_existing_campaign_to_new_oneandrefresh_ladbrokes_ui(self):
        """
        DESCRIPTION: Go to CMS and change existing campaign to new one
        DESCRIPTION: and
        DESCRIPTION: Refresh Ladbrokes UI
        EXPECTED: The tutorial page should be displayed at the end of the existing pop-up sequence
        """
        # This step cannot be automated as it affects the other TC's
