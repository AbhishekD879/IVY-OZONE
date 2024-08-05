import pytest
from tests.base_test import vtest
from tests.Common import Common
from json import JSONDecodeError


# @pytest.mark.tst2  # Not configured for tst2
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.reg156_fix
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59898183_Verify_that_Timeline_Bubble_is_displayed_for_only_logged_in_user(Common):
    """
    TR_ID: C59898183
    NAME: Verify that Timeline Bubble is displayed for only logged in user
    DESCRIPTION: This test case verifies that Timeline Bubble is displayed only for logged in user
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    param = 'timeline'
    ss_url = 'timeline'

    def get_response_url(self, url):
        """
        :param url: SS or Commentary url
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
        PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
        PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
        PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
        PRECONDITIONS: 4.Live Campaign is created.
        PRECONDITIONS: Note:
        PRECONDITIONS: Zeplin Design-https://app.zeplin.io/project/5dc59d1d83c70b83632e749cseid5fc912c1dc7b8e4f009ea750    PRECONDITIONS: Timeline feature is for both Brands:
        PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
        PRECONDITIONS: Coral- Coral Pulse
        """
        if not self.cms_config.get_timeline_system_configuration():
            self.cms_config.update_timeline_system_config()

    def test_001_user_is_not_logged_in__navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: 1.User is not logged in- Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.Timeline Bubble should not be display
        EXPECTED: 2.In WS timeline-api is not present
        """
        self.site.wait_content_state('HOMEPAGE')
        timeline_status = self.site.has_timeline(expected_result=True)
        if timeline_status:
            self.assertFalse(self.site.timeline.timeline_bubble, msg="Timeline bubble is displayed before login")

    def test_002_log_in_to_the_app_and_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Log in to the app and navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline Bubble should be displayed at the bottom of the page, above Footer menu
        EXPECTED: 3.IN WS timeline-api is present
        """
        self.site.login()
        self.site.wait_content_state('HOMEPAGE')
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(),
                        msg="Timeline bubble is not displayed after login")
        timeline_url = self.get_response_url(url=self.ss_url)
        self.assertIn(self.param, timeline_url, msg=f'Required "{self.param}" parameter not found')

    def test_003_logout_from_the_app_and_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Logout from the app and navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.Timeline Bubble should not be display
        EXPECTED: 2.In WS timeline-api is not present
        """
        self.site.logout()
        timeline_status = self.site.has_timeline(expected_result=True)
        if timeline_status:
            self.assertFalse(self.site.timeline.timeline_bubble, msg="Timeline bubble is displayed before login")

    def test_004_log_in_to_the_app_and_wait_for_log_in_session_expired(self):
        """
        DESCRIPTION: Log in to the app and Wait for log in session expired
        EXPECTED: 1.User is logged out
        EXPECTED: 2.Timeline Bubble is NOT displayed
        EXPECTED: 3.In WS is no timeline-api
        """
        # Cannot automate
