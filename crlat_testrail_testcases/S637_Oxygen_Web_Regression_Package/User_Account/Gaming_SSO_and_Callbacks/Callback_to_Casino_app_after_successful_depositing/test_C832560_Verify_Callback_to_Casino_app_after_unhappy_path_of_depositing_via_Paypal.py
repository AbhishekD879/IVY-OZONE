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
class Test_C832560_Verify_Callback_to_Casino_app_after_unhappy_path_of_depositing_via_Paypal(Common):
    """
    TR_ID: C832560
    NAME: Verify Callback to Casino app after unhappy path of depositing via Paypal
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after unhappy path of the BMA depositing via Paypal
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has a valid (unrestricted) PayPal account from which his/her can deposit funds via
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

    def test_001_call_url_httpsbma_urldepositpaypalcburlcasino_urleghttpsinvictuscoralcoukdepositpaypalcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/**#/deposit/paypal?****cbURL=**<Casino_url>
        DESCRIPTION: (e.g. https://invictus.coral.co.uk/#/deposit/paypal?cbURL=http://mcasino-tst2.coral.co.uk
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   'Paypal' tab is selected
        """
        pass

    def test_002_verify_unsuccessful_depositingenter_amount_than_is_higher_than_balance_on_the_users_cards_manually_or_using_quick_deposit_buttons_and_tap_deposit_button(self):
        """
        DESCRIPTION: Verify unsuccessful depositing:
        DESCRIPTION: Enter amount than is higher than balance on the user's cards manually or using quick deposit buttons and tap 'Deposit' button
        EXPECTED: *   Error message is shown
        EXPECTED: *   **User stays on the 'Paypal' tab on BMA app**
        """
        pass

    def test_003_enter_valid_amount_manually_or_using_quick_deposit_buttons_and_tap_deposit_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons and tap 'Deposit' button
        EXPECTED: *   Pop-up is shown
        EXPECTED: *   Paypal page is opened
        """
        pass

    def test_004_submit_paypal_form(self):
        """
        DESCRIPTION: Submit PayPal form
        EXPECTED: 
        """
        pass

    def test_005_tap_pay_now_button(self):
        """
        DESCRIPTION: Tap 'Pay Now' button
        EXPECTED: *   Successfull message is shown
        EXPECTED: *   **User is redirected to Casino application (e.g. http://mcasino-tst2.coral.co.uk)**
        EXPECTED: *   User is logged in there automaticaly
        EXPECTED: *   User Balance is increased accordingly
        """
        pass
