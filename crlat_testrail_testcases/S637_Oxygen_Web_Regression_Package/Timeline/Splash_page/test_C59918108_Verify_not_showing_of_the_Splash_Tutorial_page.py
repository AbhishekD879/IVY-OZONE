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
class Test_C59918108_Verify_not_showing_of_the_Splash_Tutorial_page(Common):
    """
    TR_ID: C59918108
    NAME: Verify not showing of the Splash/Tutorial page
    DESCRIPTION: This test case verifies that timeline won't be shown for Not logged in customer
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.User is NOT logged in
    PRECONDITIONS: 3.User haven't seen Splash page (OX.timelineTutorialOverlay is missed in the local storage)
    PRECONDITIONS: Toggles for Timeline:
    PRECONDITIONS: 4.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 5.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 6.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 7.Live Campaign is created
    PRECONDITIONS: 8.Toggle for Splash page is turned on (CMS Menu->Timeline->Timeline Splash Page-> Show Splash Page : checked on)
    PRECONDITIONS: 9.All pop-ups are closed
    PRECONDITIONS: NOTE :
    PRECONDITIONS: CMS changes applies after refresh the app
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_where_timeline_is_configured(self):
        """
        DESCRIPTION: Navigate to the page where Timeline is configured
        EXPECTED: Timeline Tutorial should not be visible for not logged in user
        """
        pass

    def test_002_go_to_cms__timline_timeline_splash_page__show_splash_page_and_turn_it_off(self):
        """
        DESCRIPTION: Go to CMS ->Timline->Timeline Splash Page-> Show Splash Page and turn it off
        EXPECTED: Сhanges are saved
        """
        pass

    def test_003___log_in_with_user_that_is_not_saw_timeline_for_current_campaign__navigate_to_the_page_where_timeline_is_configured(self):
        """
        DESCRIPTION: - Log in with user that is not saw timeline for current Campaign
        DESCRIPTION: - Navigate to the page where Timeline is configured
        EXPECTED: Timeline Tutorial should not be visible when it turned off in CMS
        EXPECTED: Response 'timeline-splash-config' with 'showSplashPage: false' attribute should be received in devtools (Network -> XHR -> 'timeline-splash-config')
        EXPECTED: Timeline header should be visible
        """
        pass

    def test_004___go_to_cms__timeline_timeline_splash_page__show_splash_page_and_turn_it_on(self):
        """
        DESCRIPTION: - Go to CMS ->Timeline->Timeline Splash Page-> Show Splash Page and turn it on
        EXPECTED: - Сhanges are saved in CMS
        """
        pass

    def test_005_refresh_the_app_and_verify_timeline_splash_page(self):
        """
        DESCRIPTION: Refresh the app and verify Timeline Splash page
        EXPECTED: Timeline Tutorial should not be visible until closing all user pop-ups
        EXPECTED: Response 'timeline-splash-config' with 'showSplashPage: true' attribute should be received in devtools (Network -> XHR -> 'timeline-splash-config')
        """
        pass

    def test_006_go_to_cms___timeline_section___timeline_system_config_item___disabled_checkboxandcms__timeline_timeline_splash_page__show_splash_page_and_turn_it_on(self):
        """
        DESCRIPTION: Go to CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Disabled' checkbox
        DESCRIPTION: AND
        DESCRIPTION: CMS ->Timeline->Timeline Splash Page-> Show Splash Page and turn it on
        EXPECTED: Timeline Tutorial should not be visible when it turned off in CMS
        EXPECTED: Timeline header should not be visible
        """
        pass

    def test_007_cms___system_configuration___structure___featuretoggle_section___timeline__disabled_checkboxandcms___timeline_section___timeline_system_config_item___disabled_enabledandcms__timeline_timeline_splash_page__show_splash_page_and_turn_it_on(self):
        """
        DESCRIPTION: CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline'-> 'Disabled' checkbox
        DESCRIPTION: AND
        DESCRIPTION: CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Disabled' enabled
        DESCRIPTION: AND
        DESCRIPTION: CMS ->Timeline->Timeline Splash Page-> Show Splash Page and turn it on
        EXPECTED: Timeline Tutorial should not be visible when it turned off in CMS
        EXPECTED: Timeline header should not be visible
        """
        pass
