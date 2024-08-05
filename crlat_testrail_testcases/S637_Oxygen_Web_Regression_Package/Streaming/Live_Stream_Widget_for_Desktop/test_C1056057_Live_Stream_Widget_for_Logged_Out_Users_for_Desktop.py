import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C1056057_Live_Stream_Widget_for_Logged_Out_Users_for_Desktop(Common):
    """
    TR_ID: C1056057
    NAME: 'Live Stream' Widget for Logged Out Users for Desktop
    DESCRIPTION: This test case verifies 'Live Stream' Widget for logged out users for Desktop.
    PRECONDITIONS: 1. User is logged out
    PRECONDITIONS: 2. Events with mapped stream are available
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is opened by default
        EXPECTED: * Live Stream widget is present in the Main view column 2
        EXPECTED: * Live Stream widget is expanded
        EXPECTED: * In WS verify:
        EXPECTED: "GET_SPORT" request sent with topLevelType: "STREAM_EVENT" 42["IN_PLAY_SPORTS::16::STREAM_EVENT",…] response is received
        EXPECTED: "GET_TYPE" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORT_TYPE::16::STREAM_EVENT::",…] response is received
        EXPECTED: "subscribe" message for 1 event with livestream available is received
        """
        pass

    def test_003_verify_live_stream_widget_content(self):
        """
        DESCRIPTION: Verify Live Stream widget content
        EXPECTED: Live Stream widget consists of:
        EXPECTED: * 'Watch live' icon, 'Watch live' text and expand/collapse icon in the header(Watch live icon and collapse icon are not displayed for Ladbrokes)
        EXPECTED: * **'Login** or **Register** to watch live streams now'
        """
        pass

    def test_004_click_login_hyperlink(self):
        """
        DESCRIPTION: Click **'Login'** hyperlink
        EXPECTED: 'Log in' pop-up is shown after clicking **'Login'** hyperlink
        """
        pass

    def test_005_click_register_hyperlink(self):
        """
        DESCRIPTION: Click **'Register'** hyperlink
        EXPECTED: 'Registration Step 1' form is shown after clicking **'Register'** hyperlink
        """
        pass

    def test_006_log_out_and_repeat_steps_1_2_but_make_sure_that_events_with_mapped_stream_are_not_available(self):
        """
        DESCRIPTION: Log out and repeat steps 1-2 but make sure that events with mapped stream are NOT available
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is opened by default
        EXPECTED: * Live Stream widget is NOT present in the Main view column 2
        """
        pass
