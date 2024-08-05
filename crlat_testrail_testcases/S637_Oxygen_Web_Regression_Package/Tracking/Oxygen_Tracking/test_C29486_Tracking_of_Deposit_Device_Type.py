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
class Test_C29486_Tracking_of_Deposit_Device_Type(Common):
    """
    TR_ID: C29486
    NAME: Tracking of Deposit Device Type
    DESCRIPTION: This test case verifies tracking of **deviceType** value during **Depositing**.
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-6363 (As a Data Analyst (BI) I want to tag the device type upon which a Deposit and Withdrawal requests are made)
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: *   [Playtech IMS][3] creds
    PRECONDITIONS: **NOTE**: **"ID":31001 **request body can be checked also in Console.
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/MOB/Playtech+IMS
    """
    keep_browser_open = True

    def test_001_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 'Deposit' page is opened
        """
        pass

    def test_002_select_payment_method_from_drop_down_list(self):
        """
        DESCRIPTION: Select payment method from drop-down list
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Deposit transaction has been successful
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

    def test_007_search_for_request_withid33016(self):
        """
        DESCRIPTION: Search for request with **"ID":33016**
        EXPECTED: Request is found
        """
        pass

    def test_008_check_the_sentparameters(self):
        """
        DESCRIPTION: Check the sent parameters
        EXPECTED: The following parameter is present:
        EXPECTED: Clienttype = Sportsbook
        EXPECTED: Client Platform = Web / Mobile
        EXPECTED: *Client Planform should be Mobile in all cases according to BMA-16608*
        EXPECTED: *Delivery Platform = HTML5*
        EXPECTED: *OS = Windows / iOS / Android*
        EXPECTED: deviceType=(device specific: e.g. iPhone 6, Nexus 5 or can be Unknown Device)
        """
        pass

    def test_009_search_for_response_with_id_id33015(self):
        """
        DESCRIPTION: Search for response with id **"ID":33015**
        EXPECTED: The following parameters is present:
        EXPECTED: - amount:<deposit amount value>
        EXPECTED: - code:<reference id>
        """
        pass

    def test_010_load_ims_system(self):
        """
        DESCRIPTION: Load IMS system
        EXPECTED: IMS is loaded
        """
        pass

    def test_011_go_to_customer_search_and_find_the_customer_who_performed(self):
        """
        DESCRIPTION: Go to customer search and find the customer who performed
        EXPECTED: Customer details are shown
        """
        pass

    def test_012_go_to_wallet_transactions_section(self):
        """
        DESCRIPTION: Go to 'Wallet Transactions' section
        EXPECTED: 'Wallet Transactions' section is shown
        """
        pass

    def test_013_find_the_deposit_via_reference_id_reference_id_from_front_endor_33015_value_in_the_code_field_should_be_equal_to_the_remote__on_the_wallet_transactions(self):
        """
        DESCRIPTION: Find the Deposit via reference id ('Reference id' from front end(or 33015 value in the code field) should be equal to the 'Remote #' on the 'Wallet Transactions')
        EXPECTED: Deposit is found
        """
        pass

    def test_014_open_the_particular_wallet_transaction_details_via_tapping_transaction__link(self):
        """
        DESCRIPTION: Open the particular 'Wallet Transaction Details' via tapping 'Transaction #' link
        EXPECTED: 'Wallet Transaction Details' is opened in a pop-up window
        """
        pass

    def test_015_verify_data_correctness_in_ims__client_platform__client_type__device_type(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: - Client platform
        DESCRIPTION: - Client Type
        DESCRIPTION: - Device Type
        EXPECTED: Received IMS data match with all data on step №8
        EXPECTED: Client platform = Web / Mobile
        EXPECTED: *Client Planform should be Mobile in all cases according to BMA-16608*
        EXPECTED: Client Type = Sportsbook
        EXPECTED: Device Type = device from which deposit was performed
        EXPECTED: *NOTE, if deposit was from web - the empty space will be shown*
        """
        pass

    def test_016_verify_data_correctness_in_ims__delivery_platform__os(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: - Delivery Platform
        DESCRIPTION: - OS
        EXPECTED: Received IMS data match with all data on step  №9
        EXPECTED: Those parameters may be found in 'Logins' or 'General player information'
        EXPECTED: NOTE, OS field is marked as 'Last login operating system name:'
        """
        pass

    def test_017_repeat_steps_1___16_for_wrapper_application(self):
        """
        DESCRIPTION: Repeat steps 1 - 16 for wrapper application
        EXPECTED: Note that Delivery platform should be **Wrapper**
        """
        pass
