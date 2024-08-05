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
class Test_C29485_Tracking_of_Login_Device_Details_from_IMS_side(Common):
    """
    TR_ID: C29485
    NAME: Tracking of Login Device Details from IMS side
    DESCRIPTION: This test case verifies tracking of Login **Device Detail**s from **IMS **side.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-3382 BI Tracking Open API Login Device Details
    DESCRIPTION: *   BMA-6365 As a Data Analyst (BI) I want the device type logged in the IMS Login Request to follow a defined format.
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: *   UAT assistance is needed
    PRECONDITIONS: **NOTE**: **"ID":33036 **request body can be checked also in Console.
    PRECONDITIONS: **Only the last LOGIN deatils are shown in IMS. That is why testing on different devices should be performed step by step.**
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_into_app_with_valid_credentials(self):
        """
        DESCRIPTION: Log In into app with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_003_in_developer_tools_go_to_network_tab__websocket_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab -> 'WebSocket' tab
        EXPECTED: 
        """
        pass

    def test_004_send_to_uat_team_the_following_log_in_info_fromid33036_request1__devicetypedevice_specific_eg_iphone_6nexus_52__devicebrowserdevice_specific_eg_mobile_safari3__osnamedevice_specific_eg_ios4__osversiondevice_specific_eg_8415__gametypesportsbook6__deliveryplatform___html5___bmain_case_of_html___wrapper___bmain_case_of_wrapper_app(self):
        """
        DESCRIPTION: Send to UAT team the following log in info from **"ID":33036 **request:
        DESCRIPTION: 1.  **deviceType** (device specific: e.g. iPhone 6, Nexus 5)
        DESCRIPTION: 2.  **deviceBrowser ** (device specific: e.g. Mobile Safari)
        DESCRIPTION: 3.  **osName **(device specific: e.g. iOS)
        DESCRIPTION: 4.  **osVersion **(device specific: e.g. 8.4.1)
        DESCRIPTION: 5.  **gameType**: **"Sportsbook"**
        DESCRIPTION: 6.  ****deliveryPlatform**:** ****
        DESCRIPTION: *   ****"HTML5 - BMA"** **(in case of HTML)
        DESCRIPTION: *   **"Wrapper - BMA"** (in case of Wrapper app)
        EXPECTED: 
        """
        pass

    def test_005_ask_to_send_you_info_related_to_the_latest_log_in_of_verified_user_from_ims_system(self):
        """
        DESCRIPTION: Ask to send you info related to the latest log in of verified user from IMS system
        EXPECTED: 
        """
        pass

    def test_006_verify_datacorrectness(self):
        """
        DESCRIPTION: Verify data correctness
        EXPECTED: Received IMS data on step №5 match with all sent data on step №4
        """
        pass
