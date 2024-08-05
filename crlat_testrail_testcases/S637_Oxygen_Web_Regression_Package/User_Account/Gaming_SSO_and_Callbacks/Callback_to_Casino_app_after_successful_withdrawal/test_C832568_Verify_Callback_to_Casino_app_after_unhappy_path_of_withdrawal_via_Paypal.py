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
class Test_C832568_Verify_Callback_to_Casino_app_after_unhappy_path_of_withdrawal_via_Paypal(Common):
    """
    TR_ID: C832568
    NAME: Verify Callback to Casino app after unhappy path of withdrawal via Paypal
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after unhappy path of the BMA withdrawal via Paypal
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has a valid restricted PayPal account from which his/her can deposit funds via
    PRECONDITIONS: The general rule should be: if there is no cbURL attribute the stay within the BMA app, if there is a cbURL then take the user to the URL in a separate tab.
    PRECONDITIONS: Available PayPal Accounts:
    PRECONDITIONS: ppone@yopmail.com / devine12
    PRECONDITIONS: pptwo@yopmail.com / devine12
    PRECONDITIONS: ppthree@yopmail.com / devine12
    PRECONDITIONS: ppfour@yopmail.com / devine12
    PRECONDITIONS: ppfive@yopmail.com / devine12
    PRECONDITIONS: BMA-5855
    """
    keep_browser_open = True

    def test_001_call_url_httpsbma_urlwithdrawcburlcasino_urleghttpsinvictuscoralcoukwithdrawcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/**#/withdraw?cbURL=**<Casino_url>
        DESCRIPTION: (e.g. https://invictus.coral.co.uk/#/withdraw?cbURL=http://mcasino-tst2.coral.co.uk
        EXPECTED: 'Withdraw Funds' page is opened
        """
        pass

    def test_002_select_paypal_card_from_drop_down(self):
        """
        DESCRIPTION: Select Paypal Card from drop-down
        EXPECTED: 
        """
        pass

    def test_003_verify_unsuccessful_waithdrawalenter_amount_than_is_higher_than_balance_on_the_users_cards_manually_or_using_quick_withdrawal_buttons_and_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Verify unsuccessful waithdrawal:
        DESCRIPTION: Enter amount than is higher than balance on the user's cards manually or using quick withdrawal buttons and tap 'Withdraw Funds' button
        EXPECTED: *   Error message is shown
        EXPECTED: *   **User stays on the 'Withdraw Funds' tab on BMA app**
        """
        pass

    def test_004_enter_valid_amount_manually_or_using_quick_withdraw_buttons_and_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick withdraw buttons and tap 'Withdraw Funds' button
        EXPECTED: *   Withdrawing is successfully completed
        EXPECTED: *   **Page is redirected to Casino application**
        EXPECTED: *   User is logged in automaticaly
        EXPECTED: *   User Balance is decreased accordingly
        """
        pass
