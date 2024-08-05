import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C28289_Verify_exceeding_Monthly_Limit_for_Deposit(Common):
    """
    TR_ID: C28289
    NAME: Verify exceeding Monthly Limit for Deposit
    DESCRIPTION: This test case verifies exceeding Monthly Limit for Deposit
    DESCRIPTION: AUTOTEST Desktop: [C2496058]
    DESCRIPTION: AUTOTEST Mobile: [C2493540]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has registered Debit/Credit Cards from which they can deposit funds from
    PRECONDITIONS: 3. User has registered PayPal account from which can deposit funds via
    PRECONDITIONS: 4. User has registered NETELLER account from which can deposit funds from
    PRECONDITIONS: 5. User has registered Skrill account from which can deposit funds from
    PRECONDITIONS: 6. User has registered PaySafeCard account from which can deposit funds from
    PRECONDITIONS: 7. User has Monthly Limit set
    PRECONDITIONS: In order to register new payment method use:
    PRECONDITIONS: Debit/Credit Cards:
    PRECONDITIONS: *   http://www.getcreditcardnumbers.com/how-to-get-a-master-card-credit-card
    PRECONDITIONS: *   http://www.getcreditcardnumbers.com/how-to-get-a-visa-credit-card
    PRECONDITIONS: PayPal:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: NETELLER: http://www.scribd.com/doc/61457666/API-Testing-101022#scribd
    PRECONDITIONS: **For testing exceeding of the Monthly limit, the ****Weekly ****limit should be exceeded before.**
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 'Deposit' page is opened
        """
        pass

    def test_002_select_debitcredit_card_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select Debit/Credit Card payment method from drop-down
        EXPECTED: 
        """
        pass

    def test_003_enter_valid_cvv_code_value(self):
        """
        DESCRIPTION: Enter valid CVV code value
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_that_exceeds_monthly_limit(self):
        """
        DESCRIPTION: Enter amount that exceeds Monthly Limit
        EXPECTED: 
        """
        pass

    def test_005_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Error message: "This deposit would exceed your self-imposed deposit limit. Check your current limit here." is shown
        EXPECTED: * User stays on 'My Payments' tab
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        EXPECTED: * 'CV2' is cleared
        """
        pass

    def test_006_click_on_here_error_message_link(self):
        """
        DESCRIPTION: Click on 'here' error message link
        EXPECTED: 'here' is hyperlinked and takes user to the 'My Limits' page
        """
        pass

    def test_007_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Back button takes user to the 'Deposit' page
        """
        pass

    def test_008_select_paypal_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select PayPal payment method from drop-down
        EXPECTED: 
        """
        pass

    def test_009_enter_amount_that_exceeds_monthly_limit(self):
        """
        DESCRIPTION: Enter amount that exceeds Monthly Limit
        EXPECTED: 
        """
        pass

    def test_010_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Error message: "This deposit would exceed your self-imposed deposit limit. Check your current limit here." is shown
        EXPECTED: * User stays on 'My Payments' tab
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        """
        pass

    def test_011_click_on_here_error_message_link(self):
        """
        DESCRIPTION: Click on 'here' error message link
        EXPECTED: 'here' is hyperlinked and takes user to the 'My Limits' page
        """
        pass

    def test_012_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Back button takes user to the 'Deposit' page
        """
        pass

    def test_013_select_neteller_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select NETELLER payment method from drop-down
        EXPECTED: 
        """
        pass

    def test_014_enter_valid_secure_id_value(self):
        """
        DESCRIPTION: Enter valid 'SECURE ID' value
        EXPECTED: 
        """
        pass

    def test_015_enter_amount_that_exceeds_monthly_limit(self):
        """
        DESCRIPTION: Enter amount that exceeds Monthly Limit
        EXPECTED: 
        """
        pass

    def test_016_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Error message: "This deposit would exceed your self-imposed deposit limit. Check your current limit here." is shown
        EXPECTED: * User stays on 'My Payments' tab
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        EXPECTED: * NETELLER - 'SECURE ID' is cleared
        """
        pass

    def test_017_click_on_here_error_message_link(self):
        """
        DESCRIPTION: Click on 'here' error message link
        EXPECTED: 'here' is hyperlinked and takes user to the 'My Limits' page
        """
        pass

    def test_018_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Back button takes user to the 'Deposit' page
        """
        pass

    def test_019_select_skrill_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select Skrill payment method from drop-down
        EXPECTED: 
        """
        pass

    def test_020_enter_amount_that_exceeds_monthly_limit(self):
        """
        DESCRIPTION: Enter amount that exceeds Monthly Limit
        EXPECTED: 
        """
        pass

    def test_021_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Error message: "This deposit would exceed your self-imposed deposit limit. Check your current limit here." is shown
        EXPECTED: * User stays on 'My Payments' tab
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        """
        pass

    def test_022_click_on_here_error_message_link(self):
        """
        DESCRIPTION: Click on 'here' error message link
        EXPECTED: 'here' is hyperlinked and takes user to the 'My Limits' page
        """
        pass

    def test_023_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Back button takes user to the 'Deposit' page
        """
        pass

    def test_024_select_paysafecard_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select PaySafeCard payment method from drop-down
        EXPECTED: 
        """
        pass

    def test_025_enter_amount_that_exceeds_monthly_limit(self):
        """
        DESCRIPTION: Enter amount that exceeds Monthly Limit
        EXPECTED: 
        """
        pass

    def test_026_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Error message: "This deposit would exceed your self-imposed deposit limit. Check your current limit here." is shown
        EXPECTED: * User stays on 'My Payments' tab
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        """
        pass
