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
class Test_C99255_Tracking_of_client_type_parameters_for_Deposit(Common):
    """
    TR_ID: C99255
    NAME: Tracking of client type parameters for Deposit
    DESCRIPTION: This test case verifies Client Type parameter for Deposit when user Log In on Oxygen and Gaming.
    DESCRIPTION: Jira tickets:
    DESCRIPTION: BMA-15345 BI Reporting - Oxygen to send new values when a Gaming player deposits, withdraws or registers
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   User has valid registered Credit Card/PayPal/NETELLER from which they can deposit funds from
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: **NOTE**: **ID:31007** requests body can be checked also in Console.
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Playtech+IMS
    PRECONDITIONS: [3]: Gaming - http://mcasino-tst2.coral.co.uk/
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

    def test_004_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 'Deposit' page is opened
        """
        pass

    def test_005_fill_in_all_required_fields_with_valid_data_and_tap_deposit_button(self):
        """
        DESCRIPTION: Fill in all required fields with valid data and tap 'Deposit' button
        EXPECTED: Deposit transaction has been successful
        """
        pass

    def test_006_load_ims_system(self):
        """
        DESCRIPTION: Load IMS system
        EXPECTED: IMS is loaded
        """
        pass

    def test_007_go_to_customer_search_and_find_the_customer_who_performed(self):
        """
        DESCRIPTION: Go to customer search and find the customer who performed
        EXPECTED: Customer details are shown
        """
        pass

    def test_008_go_to_wallet_transactions_section(self):
        """
        DESCRIPTION: Go to 'Wallet Transactions' section
        EXPECTED: 'Wallet Transactions' section is shown
        """
        pass

    def test_009_find_the_deposit_via_reference_id_reference_id_from_front_end_should_be_equal_to_the_remote__on_the_wallet_transactions(self):
        """
        DESCRIPTION: Find the Deposit via reference id ('Reference id' from front end should be equal to the 'Remote #' on the 'Wallet Transactions')
        EXPECTED: Deposit is found
        """
        pass

    def test_010_open_the_particular_wallet_transaction_details_via_tapping_transaction__link(self):
        """
        DESCRIPTION: Open the particular 'Wallet Transaction Details' via tapping 'Transaction #' link
        EXPECTED: 'Wallet Transaction Details' is opened in a pop-up window
        """
        pass

    def test_011_check_the_client_type_parameter(self):
        """
        DESCRIPTION: Check the Client Type parameter
        EXPECTED: Client Type parameter is 'Sportsbook'
        """
        pass

    def test_012_go_to_oxygen_application_and_navigate_to_the_gaming_page(self):
        """
        DESCRIPTION: Go to Oxygen application and navigate to the gaming page
        EXPECTED: Gaming is opened
        """
        pass

    def test_013_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps 4-11
        EXPECTED: 
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

    def test_017_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 'Deposit' page is opened
        """
        pass

    def test_018_repeat_steps_5_10(self):
        """
        DESCRIPTION: Repeat steps 5-10
        EXPECTED: 
        """
        pass

    def test_019_check_the_client_type_parameter(self):
        """
        DESCRIPTION: Check the Client Type parameter
        EXPECTED: Client Type parameter is 'Casino'
        """
        pass
