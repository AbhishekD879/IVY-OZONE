import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C34298266_Register_add_credit_card_and_verification_of_Private_Market_through_New_Registration(Common):
    """
    TR_ID: C34298266
    NAME: Register, add credit card and verification of Private Market through New Registration
    DESCRIPTION: Verify that the customer can see Private Markets through New Registration journey.
    DESCRIPTION: * NOTE: TC requires backoffice modifications. If no access/offers created in PROD backoffice, case could be run on TST envs
    PRECONDITIONS: * Make sure that the Private Markets Offer is created and trigger is set for newly registered users ('First deposit' trigger type).
    PRECONDITIONS: * Register new valid user without first deposit
    PRECONDITIONS: General Private Market instruction: https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets
    """
    keep_browser_open = True

    def test_001_presstap_on_deposit_button(self):
        """
        DESCRIPTION: Press/tap on 'Deposit' button
        EXPECTED: User is navigated to Deposit screen
        """
        pass

    def test_002_choose_any_of_the_available_credit_card_deposit_methods_and_fill_in_the_required_data_on_the_next_page_amount_of_deposit_credit_card_number_expiry_date___any_valid_date_in_the_future_cvv2_codeand_click_deposit_button(self):
        """
        DESCRIPTION: Choose any of the available credit card deposit methods and fill in the required data on the next page:
        DESCRIPTION: * Amount of deposit
        DESCRIPTION: * Credit card number
        DESCRIPTION: * Expiry Date - any valid date in the future
        DESCRIPTION: * CVV2 code
        DESCRIPTION: And click "Deposit" button
        EXPECTED: * "Your deposit of XX.XX GBR has been successfully" message is displayed on green background.
        EXPECTED: * Transaction details are displayed
        EXPECTED: * 'OK' and 'Make another deposit' buttons are displayed
        EXPECTED: where XX.XX - amount entered in step 6;
        EXPECTED: GBR - any currency type chosen in step 2
        """
        pass

    def test_003_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button
        EXPECTED: * User is redirected to Homepage
        EXPECTED: * The customer can see the Private Market at the first tab selected by default
        """
        pass
