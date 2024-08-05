import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29484_Tracking_of_Log_In_Device_Details(Common):
    """
    TR_ID: C29484
    NAME: Tracking of Log In Device Details
    DESCRIPTION: This test case verifies tracking of** Device Details** during **Log In**.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-3382 BI Tracking Open API Login Device Details
    DESCRIPTION: *   BMA-6365 As a Data Analyst (BI) I want the device type logged in the IMS Login Request to follow a defined format
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: *   [Playtech IMS][3] creds
    PRECONDITIONS: **NOTE**: **"ID":33036 **request body can be checked also in Console.
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/MOB/Playtech+IMS
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: Log In pop up appears
        """
        pass

    def test_003_enter_valid_user_credentials(self):
        """
        DESCRIPTION: Enter valid user credentials
        EXPECTED: 
        """
        pass

    def test_004_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: User is logged in
        """
        pass

    def test_005_in_developer_tools_go_to_network_tab__websocket_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab -> 'WebSocket' tab
        EXPECTED: 
        """
        pass

    def test_006_tap_the_request_and_select_frame_tab(self):
        """
        DESCRIPTION: Tap the request and select 'Frame' tab
        EXPECTED: 
        """
        pass

    def test_007_search_for_request_withid33036(self):
        """
        DESCRIPTION: Search for request with **"ID":33036**
        EXPECTED: Request is found
        """
        pass

    def test_008_check_the_sentparameters(self):
        """
        DESCRIPTION: Check the sent parameters
        EXPECTED: The following parameters are present:
        EXPECTED: 1.  deviceId: "xxPxxx" (BMA-4243)
        EXPECTED: 2.  **deviceType** (device specific: e.g. iPhone 6, Nexus 5)
        EXPECTED: 3.  **deviceBrowser **(device specific: e.g. Mobile Safari)
        EXPECTED: 4.  **osName **(device specific: e.g. iOS)
        EXPECTED: 5.  **osVersion **(device specific: e.g. 8.4.1)
        EXPECTED: 6.  **gameType**: **"Sportsbook"**
        EXPECTED: 7.  ****deliveryPlatform**:** ****
        EXPECTED: *   ****"HTML5 - BMA"** **(in case of HTML)
        EXPECTED: *   **"Wrapper - BMA"** (in case of Wrapper app)
        """
        pass

    def test_009_verify_data_correctness_in_the_ims_link_in_preconditions___search_for_user___verify_last_login_info_in_the_general_player_information_and_in_logins_sections(self):
        """
        DESCRIPTION: Verify data correctness in the IMS (link in preconditions):
        DESCRIPTION: -  Search for user
        DESCRIPTION: -  Verify last login info in the 'General player information' and in 'Logins' sections
        EXPECTED: Received IMS data match with all data on step №8
        """
        pass
