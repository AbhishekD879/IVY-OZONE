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
class Test_C2064823_Verify_Callback_to_Casino_app_after_happy_path_of_withdrawal_via_Neteller(Common):
    """
    TR_ID: C2064823
    NAME: Verify Callback to Casino app after happy path of withdrawal via Neteller
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after successful completion of the Oxygen withdrawal via Neteller
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered NETELLER account, the balance of the account is enough for withdraw from (NETELLER accounts: http://www.scribd.com/doc/61457666/API-Testing-101022#scribd)
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
        EXPECTED: 'Withdraw Funds' page is opened
        """
        pass

    def test_003_select_neteller_method_from_payments_dropdown_list(self):
        """
        DESCRIPTION: Select **Neteller method** from payments dropdown list
        EXPECTED: **Neteller method** is selected in payments dropdown list
        """
        pass

    def test_004_enter_valid_amount_manually_or_using_quick_withdraw_buttons_and_clicktap_withdraw_funds_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick withdraw buttons and click/tap 'Withdraw Funds' button
        EXPECTED: *   Withdrawing is successfully completed
        EXPECTED: *   **Page is redirected to Casino application**
        EXPECTED: *   User is logged in automaticaly
        EXPECTED: *   User Balance is decreased accordingly
        """
        pass
