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
class Test_C2064822_Verify_Callback_to_Casino_app_after_happy_path_of_depositing_via_Neteller(Common):
    """
    TR_ID: C2064822
    NAME: Verify Callback to Casino app after happy path of depositing via Neteller
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after successful completion of the Oxygen depositing via Neteller
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has a valid NETELLER account from which they can deposit funds from  (NETELLER accounts: http://www.scribd.com/doc/61457666/API-Testing-101022#scribd)
    PRECONDITIONS: *   Balance is enough for deposit from
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_load_casino_appeg_httpswpl_stg5_public_coralcoralcouk(self):
        """
        DESCRIPTION: Load Casino app
        DESCRIPTION: (e.g. https://wpl-stg5-public-coral.coral.co.uk)
        EXPECTED: Casino app is loaded
        """
        pass

    def test_002_call_url_httpsbma_urldepositregisteredeg_httpsbet_hlcoralcoukdepositregistered(self):
        """
        DESCRIPTION: Call URL https://BMA_url/**#/deposit/registered?
        DESCRIPTION: (e.g. https://bet-hl.coral.co.uk/deposit/registered)
        EXPECTED: * 'Deposit' page is opened
        EXPECTED: * 'My Payments' tab is selected by default
        """
        pass

    def test_003_select_neteller_method_from_payments_dropdown_list(self):
        """
        DESCRIPTION: Select **Neteller method** from payments dropdown list
        EXPECTED: **Neteller method** is selected in payments dropdown list
        """
        pass

    def test_004_enter_valid_security_id_into_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Enter valid Security ID into 'Secure ID or Authentication Code:' field
        EXPECTED: Secure ID or Authentication Code is displayed
        """
        pass

    def test_005_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: *   Amount is displayed in Amount edit field
        EXPECTED: *   'Deposit' button is enabled
        """
        pass

    def test_006_click_deposit_button(self):
        """
        DESCRIPTION: Click 'Deposit' button
        EXPECTED: *   Successfull message is shown
        EXPECTED: *   **User is redirected to Casino application (e.g. https://wpl-stg5-public-coral.coral.co.uk)**
        EXPECTED: *   User is logged in there automaticaly
        EXPECTED: *   User Balance is increased accordingly
        """
        pass
