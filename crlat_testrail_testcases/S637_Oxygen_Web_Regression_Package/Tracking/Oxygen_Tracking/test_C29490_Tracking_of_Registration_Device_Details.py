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
class Test_C29490_Tracking_of_Registration_Device_Details(Common):
    """
    TR_ID: C29490
    NAME: Tracking of Registration Device Details
    DESCRIPTION: This test case verifies tracking of** Device Details** during **Registration**.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-6364 (As a Data Analyst (BI) I want to have device type/platform information passed to IMS when a user registers for a GCI account)
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: *   [Playtech IMS][3] creds
    PRECONDITIONS: **NOTE**: **"ID":31007 **and **"ID":31001 **requests body can be checked also in Console.
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

    def test_002_tap_join_button(self):
        """
        DESCRIPTION: Tap 'Join' button
        EXPECTED: 'Join Us - Step 1 of 2' is shown
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_tap_go_to_step_2_button(self):
        """
        DESCRIPTION: Tap 'Go to Step 2' button
        EXPECTED: 'Join Us - Step 2 of 2' is shown
        """
        pass

    def test_005_fill_in_all_required_fields_with_valid_data_and_tap_complete_registration_button(self):
        """
        DESCRIPTION: Fill in all required fields with valid data and tap 'Complete Registration' button
        EXPECTED: 
        """
        pass

    def test_006_in_developer_tools_go_to_network_tab__websocket_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab -> 'WebSocket' tab
        EXPECTED: 
        """
        pass

    def test_007_tap_the_request_and_select_frame_tab(self):
        """
        DESCRIPTION: Tap the request and select 'Frame' tab
        EXPECTED: 
        """
        pass

    def test_008_search_for_request_withid31007(self):
        """
        DESCRIPTION: Search for request with **"ID":31007**
        EXPECTED: Request is found
        """
        pass

    def test_009_check_the_sentparameters_indatamap_request_part(self):
        """
        DESCRIPTION: Check the sent parameters in "**dataMap**" request part
        EXPECTED: The following parameters are present:
        EXPECTED: 1.  **signupDeviceBrowser** (e.g.:"Chrome 47.0.2526.111")
        EXPECTED: 2.  **signupOsName **(e.g."Android")
        EXPECTED: 3.  **signupOsVersion** (e.g."4.4.1")
        EXPECTED: 4.  **signupDeliveryPlatform**:** **
        EXPECTED: *   ****"HTML5 - BMA"** **(in case of HTML)
        EXPECTED: *   **"Wrapper - BMA"** (in case of Wrapper app)
        EXPECTED: 5.  Client Platform (Client Planform should be Mobile in all cases according to BMA-16608)
        """
        pass

    def test_010_search_for_request_withid31001_and_check_the_following_parameters___devicebrowser___osname___osversion___deliveryplatform(self):
        """
        DESCRIPTION: Search for request with **"ID":31001** and check the following parameters:
        DESCRIPTION: *   deviceBrowser
        DESCRIPTION: *   osName
        DESCRIPTION: *   osVersion
        DESCRIPTION: *   deliveryPlatform
        EXPECTED: 
        """
        pass

    def test_011_compare_data_of_request_id31007_andid31001(self):
        """
        DESCRIPTION: Compare data of request "ID":31007 and "ID":31001
        EXPECTED: *   **signupDeviceBrowser** is the same as **deviceBrowser**
        EXPECTED: *   **signupOsName **is the same as **osName**
        EXPECTED: *   **signupOsVersion** is the same as **osVersion**
        EXPECTED: *   **signupdeliveryPlatform **is the same as **deliveryPlatform **
        """
        pass

    def test_012_load_ims_system(self):
        """
        DESCRIPTION: Load IMS system
        EXPECTED: IMS is loaded
        """
        pass

    def test_013_go_to_customer_search_and_find_the_customer_who_performed(self):
        """
        DESCRIPTION: Go to customer search and find the customer who performed
        EXPECTED: Customer details are shown
        """
        pass

    def test_014_scroll_to_general_player_information(self):
        """
        DESCRIPTION: Scroll to 'General player information'
        EXPECTED: 'General player information' section is shown
        """
        pass

    def test_015_verify_data_correctness_in_imsplus__signupdevicebrowser_egchrome_4702526111plus__sign_up_operating_system_name_egandroidplus__sign_up_platformplus__sign_up_operating_system_versionplus__sign_up_device_delivery_platform(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: +  signupDeviceBrowser (e.g.:"Chrome 47.0.2526.111")
        DESCRIPTION: +  Sign up operating system name (e.g."Android")
        DESCRIPTION: +  Sign up platform
        DESCRIPTION: +  Sign up operating system version
        DESCRIPTION: +  Sign up device delivery platform
        EXPECTED: 
        """
        pass
