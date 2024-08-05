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
class Test_C59898183_Verify_that_Timeline_Bubble_is_displayed_for_only_logged_in_user(Common):
    """
    TR_ID: C59898183
    NAME: Verify that Timeline Bubble is displayed for only logged in user
    DESCRIPTION: This test case verifies that Timeline Bubble is displayed only for logged in user
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.Live Campaign is created.
    PRECONDITIONS: Note:
    PRECONDITIONS: Zeplin Design-https://app.zeplin.io/project/5dc59d1d83c70b83632e749cseid5fc912c1dc7b8e4f009ea750
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_1user_is_not_logged_in__navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: 1.User is not logged in- Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.Timeline Bubble should not be display
        EXPECTED: 2.In WS timeline-api is not present
        """
        pass

    def test_002_log_in_to_the_app_and_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Log in to the app and navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline Bubble should be displayed at the bottom of the page, above Footer menu
        EXPECTED: 3.IN WS timeline-api is present
        """
        pass

    def test_003_logout_from_the_app_and_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Logout from the app and navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.Timeline Bubble should not be display
        EXPECTED: 2.In WS timeline-api is not present
        """
        pass

    def test_004_log_in_to_the_app_and_wait_for_log_in_session_expired(self):
        """
        DESCRIPTION: Log in to the app and Wait for log in session expired
        EXPECTED: 1.User is logged out
        EXPECTED: 2.Timeline Bubble is NOT displayed
        EXPECTED: 3.In WS is no timeline-api
        """
        pass
