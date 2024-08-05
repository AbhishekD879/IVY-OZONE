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
class Test_C2064595_Verify_Callback_to_Casino_app_after_happy_path_of_depositing_via_Skrill_1_Tap(Common):
    """
    TR_ID: C2064595
    NAME: Verify Callback to Casino app after happy path of depositing via Skrill 1-Tap
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after successful completion of the Oxygen depositing via Skrill 1-Tap
    PRECONDITIONS: 1) User is logged in
    PRECONDITIONS: 2) User has a valid Skrill 1-Tap account from which he/her can deposit funds
    PRECONDITIONS: 3) Balance is enough for deposit from
    PRECONDITIONS: Available Skrill Accounts:
    PRECONDITIONS: Skrill STG/TST Login details
    PRECONDITIONS: mbgctest01@galacoral.com mbgc0101
    PRECONDITIONS: mbgctest02@galacoral.com mbgc0202
    PRECONDITIONS: mbgctest03@galacoral.com mbgc0303
    PRECONDITIONS: mbgctest04@galacoral.com mbgc0404
    PRECONDITIONS: Skrill PROD Login details
    PRECONDITIONS: IanTevez33@gmail.com Lanzini6260
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: In order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
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

    def test_003_select_skrill_1_tap_method_from_payments_dropdown_list(self):
        """
        DESCRIPTION: Select **Skrill 1-Tap method** from payments dropdown list
        EXPECTED: **Skrill 1-Tab method** is selected in payments dropdown list in the format: Skrill 1-Tap (Account ID)
        """
        pass

    def test_004_enter_valid_amount_manually_or_via_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or via quick deposit buttons
        EXPECTED: Enter amount is displayed in 'Amount' field
        """
        pass

    def test_005_click_deposit_button(self):
        """
        DESCRIPTION: Click 'Deposit' button
        EXPECTED: * Skrill 1-Tap iframe page is opened where user is able to submit Skrill 1-Tap form (Skrill 1-Tap iframe page is only opened when user performs first transaction via this payment method)
        EXPECTED: * Skrill 1-Tap merchant page is bypassed and Amount is increased on entered value automatically when user has already enabled Skrill 1-Tap before
        """
        pass

    def test_006_submit_skrill_1_tap_form(self):
        """
        DESCRIPTION: Submit Skrill 1-Tap form
        EXPECTED: *   Successfull message is shown
        EXPECTED: *   **User is redirected to Casino application (e.g. https://wpl-stg5-public-coral.coral.co.uk)**
        EXPECTED: *   User is logged in there automaticaly
        EXPECTED: *   User Balance is increased accordingly
        """
        pass
