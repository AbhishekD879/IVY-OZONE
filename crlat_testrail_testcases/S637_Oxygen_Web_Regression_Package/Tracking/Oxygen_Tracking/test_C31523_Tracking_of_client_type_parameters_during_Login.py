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
class Test_C31523_Tracking_of_client_type_parameters_during_Login(Common):
    """
    TR_ID: C31523
    NAME: Tracking of client type parameters during Login
    DESCRIPTION: This test case verifies tracking of new parameters during Login.
    DESCRIPTION: Jira tickets:
    DESCRIPTION: BMA-14430 BI Reporting - New parameters during Login
    DESCRIPTION: BMA-15345 BI Reporting - Oxygen to send new values when a Gaming player deposits, withdraws or registers
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: **NOTE**: **ID:31007** requests body can be checked also in Console.
    PRECONDITIONS: [1]: IMS - https://confluence.egalacoral.com/display/SPI/Playtech+IMS
    PRECONDITIONS: [2]: Gaming - http://mcasino-tst2.coral.co.uk/
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
        EXPECTED: 'Log In' pop-up is shown
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data_and_tap_log_in_button(self):
        """
        DESCRIPTION: Fill in all required fields with valid data and tap 'Log In' button
        EXPECTED: User is successful Logged In
        """
        pass

    def test_004_in_developer_tools_go_to_network_tab___websocket_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab -> 'WebSocket' tab
        EXPECTED: 
        """
        pass

    def test_005_tap_the_request_and_select_frame_tab(self):
        """
        DESCRIPTION: Tap the request and select 'Frame' tab
        EXPECTED: 
        """
        pass

    def test_006_search_for_request_with_id33036(self):
        """
        DESCRIPTION: Search for request with **ID:33036**
        EXPECTED: Request is found
        """
        pass

    def test_007_check_the_sent_parameters_in_datamap_request_part(self):
        """
        DESCRIPTION: Check the sent parameters in **dataMap** request part
        EXPECTED: The following parameters are present:
        EXPECTED: 1.  **clientPlatform** ("mobile")
        EXPECTED: 2.  **clientType**("Sportsbook")
        EXPECTED: 3.  **signupDeliveryPlatform**:
        EXPECTED: *   **HTML5** (in case of HTML)
        EXPECTED: *   **Wrapper ** (in case of Wrapper app)
        """
        pass

    def test_008_load_ims_system(self):
        """
        DESCRIPTION: Load IMS system
        EXPECTED: IMS is loaded
        """
        pass

    def test_009_go_to_customer_search_and_find_the_customer_who_performed(self):
        """
        DESCRIPTION: Go to customer search and find the customer who performed
        EXPECTED: Customer details are shown
        """
        pass

    def test_010_scroll_to_logins_section(self):
        """
        DESCRIPTION: Scroll to 'Logins' section
        EXPECTED: 'Logins' section is shown
        """
        pass

    def test_011_verify_data_correctness_in_ims_client_platformtype_delivery_platform(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: -Client platform/type
        DESCRIPTION: -Delivery platform
        EXPECTED: - **Client platform/type** is 'mobile/sportsbook'
        EXPECTED: - **Delivery platform**
        EXPECTED: *   **HTML5** (in case of HTML)
        EXPECTED: *   **Wrapper** (in case of Wrapper app)
        """
        pass

    def test_012_scroll_to_general_player_information(self):
        """
        DESCRIPTION: Scroll to 'General player information'
        EXPECTED: 'General player information' section is shown
        """
        pass

    def test_013_verify_data_correctness_in_ims_last_login_operating_system_name(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: -Last login operating system name
        EXPECTED: - **Last login operating system name**
        EXPECTED: *   **Windows** (in case of desktop)
        EXPECTED: *   **IOS** (in case of IOS devices)
        EXPECTED: *   **Android** (in case of Android devices)
        """
        pass

    def test_014_logged_out_from_oxygen_application(self):
        """
        DESCRIPTION: Logged Out from Oxygen application
        EXPECTED: 
        """
        pass

    def test_015_navigate_to_the_gaming_page(self):
        """
        DESCRIPTION: Navigate to the gaming page
        EXPECTED: 
        """
        pass

    def test_016_log_in_through_gaming(self):
        """
        DESCRIPTION: Log In through Gaming
        EXPECTED: User is successful Logged In
        """
        pass

    def test_017_repeat_steps_8_10(self):
        """
        DESCRIPTION: Repeat steps 8-10
        EXPECTED: 
        """
        pass

    def test_018_verify_login_client_type_parameter_in_ims(self):
        """
        DESCRIPTION: Verify Login client type parameter in IMS
        EXPECTED: Login Client Type parameter is 'Casino'
        """
        pass
