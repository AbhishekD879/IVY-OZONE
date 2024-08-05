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
class Test_C29491_Tracking_of_Registration_Device_Details_from_IMS_side(Common):
    """
    TR_ID: C29491
    NAME: Tracking of Registration Device Details from IMS side
    DESCRIPTION: This test case verifies tracking of** Device Details** during **Registration** from **IMS **side.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-6364 (As a Data Analyst (BI) I want to have device type/platform information passed to IMS when a user registers for a GCI account)
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   UAT assistance is needed
    PRECONDITIONS: **NOTE**: **"ID":31007 **request body can be checked also in Console.
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_register_new_user(self):
        """
        DESCRIPTION: Register new user
        EXPECTED: User has been registered successfully
        """
        pass

    def test_003_in_developer_tools_go_to_network_tab__websocket_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab -> 'WebSocket' tab
        EXPECTED: 
        """
        pass

    def test_004_tap_the_request_and_select_frame_tab(self):
        """
        DESCRIPTION: Tap the request and select 'Frame' tab
        EXPECTED: 
        """
        pass

    def test_005_search_for_request_withid31007(self):
        """
        DESCRIPTION: Search for request with **"ID":31007**
        EXPECTED: Request is found
        """
        pass

    def test_006_check_the_following_parameters_indatamap_request_part1__signupdevicebrowseregchrome_47025261112__signuposnameegandroid3__signuposversioneg4414__deliveryplatform___html5__bmain_case_of_html___wrapper__bmain_case_of_wrapper_app(self):
        """
        DESCRIPTION: Check the following parameters in "**dataMap**" request part:
        DESCRIPTION: 1.  **signupDeviceBrowser** (e.g.:"Chrome 47.0.2526.111")
        DESCRIPTION: 2.  **signupOsName **(e.g."Android")
        DESCRIPTION: 3.  **signupOsVersion** (e.g."4.4.1")
        DESCRIPTION: 4.  **deliveryPlatform**:** **
        DESCRIPTION: *   ****"HTML5 - BMA"** **(in case of HTML)
        DESCRIPTION: *   **"Wrapper - BMA"** (in case of Wrapper app)
        EXPECTED: 
        """
        pass

    def test_007_send_to_uat_team_username_of_just_registered_user(self):
        """
        DESCRIPTION: Send to UAT team **username **of just registered user
        EXPECTED: 
        """
        pass

    def test_008_ask_to_send_you_info_related_to_the_verified_registered_user_from_ims_system(self):
        """
        DESCRIPTION: Ask to send you info related to the verified Registered user from IMS system
        EXPECTED: 
        """
        pass

    def test_009_verify_datacorrectness(self):
        """
        DESCRIPTION: Verify data correctness
        EXPECTED: Received IMS data on step №8 match with data on step №6
        """
        pass
