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
class Test_C29487_Tracking_of_Deposit_Device_Type_from_IMS_side(Common):
    """
    TR_ID: C29487
    NAME: Tracking of Deposit Device Type from IMS side
    DESCRIPTION: This test case verifies tracking of **deviceType** value during **Depositing** from **IMS** side.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6363 (As a Data Analyst (BI) I want to tag the device type upon which a Deposit and Withdrawal requests are made)
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has valid registered Credit Card/PayPal/NETELLER from which they can deposit funds from
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: **NOTE**: **"ID":33016 **request body can be checked also in Console.
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
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

    def test_006_send_to_uat_team_the_following_deposit_info_fromid33016request___devicetypedevice_specific_eg_iphone_6nexus_5___username___the_last_4_digits_of_card_numberpaypal_emailneteller_account_id_or_email___reference_id_number_that_appears_on_the_successful_deposit_message___deposit_amount(self):
        """
        DESCRIPTION: Send to UAT team the following deposit info from **"ID":33016**** **request:
        DESCRIPTION: *   **deviceType** (device specific: e.g. iPhone 6, Nexus 5)
        DESCRIPTION: *   username
        DESCRIPTION: *   the last 4 digits of Card number/PayPal Email/NETELLER Account ID or Email
        DESCRIPTION: *   reference ID (number that appears on the successful deposit message)
        DESCRIPTION: *   deposit amount
        EXPECTED: 
        """
        pass

    def test_007_load_ims_system(self):
        """
        DESCRIPTION: Load IMS system
        EXPECTED: IMS is loaded
        """
        pass

    def test_008_go_to_customer_search_and_find_the_customer_who_performed(self):
        """
        DESCRIPTION: Go to customer search and find the customer who performed
        EXPECTED: Customer details are shown
        """
        pass

    def test_009_go_to_wallet_transactions_section(self):
        """
        DESCRIPTION: Go to 'Wallet Transactions' section
        EXPECTED: 'Wallet Transactions' section is shown
        """
        pass

    def test_010_find_the_deposit_via_reference_id_reference_id_from_front_end_should_be_equal_to_the_remote__on_the_wallet_transactions(self):
        """
        DESCRIPTION: Find the Deposit via reference id ('Reference id' from front end should be equal to the 'Remote #' on the 'Wallet Transactions')
        EXPECTED: Deposit is found
        """
        pass

    def test_011_open_the_particular_wallet_transaction_details_via_tapping_transaction__link(self):
        """
        DESCRIPTION: Open the particular 'Wallet Transaction Details' via tapping 'Transaction #' link
        EXPECTED: 'Wallet Transaction Details' is opened in a pop-up window
        """
        pass

    def test_012_check_the_following_parameters__client_platform__client_type__device_type(self):
        """
        DESCRIPTION: Check the following parameters:
        DESCRIPTION: - Client platform
        DESCRIPTION: - Client Type
        DESCRIPTION: - Device Type
        EXPECTED: Client platform = Web / Mobile
        EXPECTED: Client Type = Sportsbook
        EXPECTED: Device Type = device from which deposit was performed
        EXPECTED: NOTE, if deposit was from web - the empty space will be shown
        """
        pass

    def test_013_check_parameters__delivery_platform__os(self):
        """
        DESCRIPTION: Check parameters
        DESCRIPTION: - Delivery Platform
        DESCRIPTION: - OS
        EXPECTED: Those parameters may be found in 'Logins' or 'General player information'
        EXPECTED: NOTE, OS field is marked as 'Last login operating system name:'
        """
        pass
