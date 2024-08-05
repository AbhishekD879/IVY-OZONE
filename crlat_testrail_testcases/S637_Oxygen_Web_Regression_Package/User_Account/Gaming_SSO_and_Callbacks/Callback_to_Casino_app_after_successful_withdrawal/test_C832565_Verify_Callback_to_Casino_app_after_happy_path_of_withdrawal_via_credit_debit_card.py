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
class Test_C832565_Verify_Callback_to_Casino_app_after_happy_path_of_withdrawal_via_credit_debit_card(Common):
    """
    TR_ID: C832565
    NAME: Verify Callback to Casino app after happy path of withdrawal via credit/debit card
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after successful completion of the BMA withdrawal via credit/debit card
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has more than one registered debit/credit cards
    PRECONDITIONS: The general rule should be: if there is no cbURL attribute the stay within the BMA app, if there is a cbURL then take the user to the URL in a separate tab.
    PRECONDITIONS: BMA-5238
    """
    keep_browser_open = True

    def test_001_call_url_httpsbma_urlwithdrawcburlcasino_urleghttpsinvictuscoralcoukwithdrawcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/**#/withdraw?cbURL=**<Casino_url>
        DESCRIPTION: (e.g. https://invictus.coral.co.uk/#/withdraw?cbURL=http://mcasino-tst2.coral.co.uk
        EXPECTED: 'Withdraw Funds' page is opened
        """
        pass

    def test_002_select_creditdebit_cards_from_drop_down(self):
        """
        DESCRIPTION: Select Credit/Debit Cards from drop-down
        EXPECTED: 
        """
        pass

    def test_003_enter_valid_amount_manually_or_using_quick_quick_withdraw_buttons_and_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick quick withdraw buttons and tap 'Withdraw Funds' button
        EXPECTED: *   Withdrawing is successfully completed
        EXPECTED: *   **Page is redirected to Casino application**
        EXPECTED: *   User is logged in automaticaly
        EXPECTED: *   User Balance is decreased accordingly
        """
        pass
