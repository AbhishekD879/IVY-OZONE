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
class Test_C29488_Tracking_of_Withdraw_Device_Type(Common):
    """
    TR_ID: C29488
    NAME: Tracking of Withdraw Device Type
    DESCRIPTION: This test case verifies tracking of **deviceType** value during **Withdrawing**.
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-6363 (As a Data Analyst (BI) I want to tag the device type upon which a Deposit and Withdrawal requests are made)
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has valid registered Credit Card/PayPal/NETELLER
    PRECONDITIONS: *   Balance of accounts is enough for withdraw from
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: *   [Playtech IMS][3] creds
    PRECONDITIONS: **NOTE**: **"ID":33017 **request body can be checked also in Console.
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/MOB/Playtech+IMS
    """
    keep_browser_open = True

    def test_001_go_to_withdraw_funds_page(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page
        EXPECTED: 'Withdraw Funds' page is opened
        """
        pass

    def test_002_select_payment_method_from_drop_down_list(self):
        """
        DESCRIPTION: Select payment method from drop-down list
        EXPECTED: 
        """
        pass

    def test_003_enter_amount_and_tap_withdraw_button(self):
        """
        DESCRIPTION: Enter amount and tap 'Withdraw' button
        EXPECTED: 
        """
        pass

    def test_004_in_developer_tools_go_to_network_tab__websocket_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab -> 'WebSocket' tab
        EXPECTED: 
        """
        pass

    def test_005_tap_the_request_and_select_frame_tab(self):
        """
        DESCRIPTION: Tap the request and select 'Frame' tab
        EXPECTED: 
        """
        pass

    def test_006_search_for_request_withid33017(self):
        """
        DESCRIPTION: Search for request with **"ID":33017**
        EXPECTED: Request is found
        """
        pass

    def test_007_check_the_sentparameters(self):
        """
        DESCRIPTION: Check the sent parameters
        EXPECTED: The following parameter is present:
        EXPECTED: * Clienttype = Sportsbook
        EXPECTED: * Client Platform = Web / Mobile
        EXPECTED: *Client Planform should be Mobile in all cases according to BMA-16608*
        EXPECTED: * Delivery Platform = HTML5 /Wrapper
        EXPECTED: * OS = Windows / iOS / Android
        EXPECTED: Note, values for fields depend on device and type of app (html5 or wrapper)
        """
        pass

    def test_008_search_for_response_with_id_id33018(self):
        """
        DESCRIPTION: Search for response with id "ID":33018
        EXPECTED: The following parameters is present:
        EXPECTED: - code:<reference id>
        """
        pass

    def test_009_load_ims_system(self):
        """
        DESCRIPTION: Load IMS system
        EXPECTED: IMS is loaded
        """
        pass

    def test_010_go_to_customer_search_and_find_the_customer_who_performed(self):
        """
        DESCRIPTION: Go to customer search and find the customer who performed
        EXPECTED: Customer details are shown
        """
        pass

    def test_011_go_to_wallet_transactions_section(self):
        """
        DESCRIPTION: Go to 'Wallet Transactions' section
        EXPECTED: 'Wallet Transactions' section is shown
        """
        pass

    def test_012_find_the_withdraw_request_via_reference_id_reference_id_from_front_end_should_be_equal_to_the_remote__on_the_wallet_transactions(self):
        """
        DESCRIPTION: Find the Withdraw request via reference id ('Reference id' from front end should be equal to the 'Remote #' on the 'Wallet Transactions')
        EXPECTED: Withdraw is found
        """
        pass

    def test_013_open_the_particular_wallet_transaction_details_via_tapping_transaction__link(self):
        """
        DESCRIPTION: Open the particular 'Wallet Transaction Details' via tapping 'Transaction #' link
        EXPECTED: 'Wallet Transaction Details' is opened in a pop-up window
        """
        pass

    def test_014_verify_data_correctness_in_imsclient_platformclient_typedevice_type(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: Client platform
        DESCRIPTION: Client Type
        DESCRIPTION: Device Type
        EXPECTED: Received IMS data match with all data on step №7
        EXPECTED: Client platform = Web / Mobile
        EXPECTED: *Client Planform should be Mobile in all cases according to BMA-16608*
        EXPECTED: Client Type = Sportsbook
        EXPECTED: Device Type = device from which withdrawal was performed
        EXPECTED: *NOTE, if deposit was from web - the empty space will be shown*
        """
        pass

    def test_015_verify_data_correctness_in_ims_delivery_platform_os(self):
        """
        DESCRIPTION: Verify data correctness in IMS:
        DESCRIPTION: -Delivery Platform
        DESCRIPTION: -OS
        EXPECTED: Received IMS data match with all data on step №8
        EXPECTED: Those parameters may be found in 'Logins' or 'General player information' sections
        EXPECTED: NOTE, OS field is marked as 'Last login operating system name:'
        """
        pass

    def test_016_repeat_steps__1___15_for_different_devices_and_types_of_app(self):
        """
        DESCRIPTION: Repeat steps # 1 - 15 for different devices and types of app
        EXPECTED: 
        """
        pass
