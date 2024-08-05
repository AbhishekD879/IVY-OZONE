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
class Test_C59918225_Verify_skeleton_displaying_with_a_lost_internet_connection(Common):
    """
    TR_ID: C59918225
    NAME: Verify  skeleton displaying with a lost internet connection
    DESCRIPTION: This test case verifies displaying the skeleton instead of a spinner in the application.
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.User is logged in
    PRECONDITIONS: Toggles for Timeline:
    PRECONDITIONS: 3.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 4.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'Feature Toggle' section -> 'Timeline' )
    PRECONDITIONS: 5.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page URLs' field )
    PRECONDITIONS: 6.Live Campaign is created
    PRECONDITIONS: Note: Desktop means the Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_camping(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the Post in the Live Camping
        EXPECTED: The post should be created and published
        """
        pass

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline bubble  should be displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_003_click_on_the_timeline_bubble_buttonladbrokes__ladbrokes_loungecoral__coral_pulse(self):
        """
        DESCRIPTION: Click on the 'Timeline Bubble' button
        DESCRIPTION: Ladbrokes- Ladbrokes Lounge
        DESCRIPTION: Coral- Coral Pulse
        EXPECTED: 1.Page with the published post should be opened
        EXPECTED: 2.Content should be same as in CMS
        EXPECTED: 3.In WS 'Post' response should be present with all fields from CMS
        """
        pass

    def test_004_turn_off_the_wi_fimobile_data(self):
        """
        DESCRIPTION: Turn off the Wi-Fi/Mobile Data
        EXPECTED: Wi-Fi/Mobile Data should be
        EXPECTED: turned off
        """
        pass

    def test_005_return_to_the_timeline___open_console_and_wait_for_reconnection(self):
        """
        DESCRIPTION: Return to the Timeline - Open Console and Wait for reconnection
        EXPECTED: 1.On UI new skeleton should be displayed instead of a spinner
        EXPECTED: 2.Skeleton should be displaying in a 'shimmer' effect (video is added)
        EXPECTED: 3.WebSocket connection to 'wss://timeline-api-env Error in connection establishment:
        EXPECTED: net::ERR_INTERNET_DISCONNECTED
        """
        pass

    def test_006_wait_for_the_error_message_on_ui(self):
        """
        DESCRIPTION: Wait for the error message on UI
        EXPECTED: 1.Error message 'Oops! We are having trouble loading this page. Please check your connection'
        EXPECTED: 2.'TRY AGAIN' button should be present
        """
        pass

    def test_007_click_on_try_again_button(self):
        """
        DESCRIPTION: Click on 'TRY AGAIN' button
        EXPECTED: 1.On UI new skeleton should be displayed instead of a spinner
        EXPECTED: 2.Skeleton should be displaying in a 'shimmer' effect (video is added)
        EXPECTED: 3.WebSocket connection to 'wss://timeline-api-env Error in connection establishment: net::ERR_INTERNET_DISCONNECTED
        """
        pass

    def test_008_turn_on_the_wi_fimobile_data(self):
        """
        DESCRIPTION: Turn on the Wi-Fi/Mobile Data
        EXPECTED: Wi-Fi/Mobile Data should be
        EXPECTED: turned on
        """
        pass

    def test_009_return_to_the_timeline___open_console_wait_for_reconnection(self):
        """
        DESCRIPTION: Return to the Timeline - Open Console-Wait for reconnection
        EXPECTED: 1.User should be logged in
        EXPECTED: 2.The page should be in transition from the skeleton to the full page content
        EXPECTED: 3.Posts should be present on the Timeline
        EXPECTED: 4.Open Network ->WS ->wss://timeline-api is present with posts
        """
        pass
