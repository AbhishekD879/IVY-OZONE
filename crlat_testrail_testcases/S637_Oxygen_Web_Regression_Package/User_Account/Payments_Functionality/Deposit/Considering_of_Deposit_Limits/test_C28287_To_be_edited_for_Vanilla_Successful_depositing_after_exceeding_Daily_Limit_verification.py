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
class Test_C28287_To_be_edited_for_Vanilla_Successful_depositing_after_exceeding_Daily_Limit_verification(Common):
    """
    TR_ID: C28287
    NAME: [To be edited for Vanilla] Successful depositing after exceeding Daily Limit verification
    DESCRIPTION: This test case verifies considering Daily Limit for Deposit functionality
    DESCRIPTION: AUTOTEST: [C9697887]
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has registered Debit/Credit Cards from which they can deposit funds from
    PRECONDITIONS: 3.  User has a valid (unrestricted) PayPal account from which his/her can deposit funds via
    PRECONDITIONS: 4.  User has a valid NETELLER account from which they can deposit funds from (http://www.scribd.com/doc/61457666/API-Testing-101022#scribd)
    PRECONDITIONS: 5.  User knows his/her Daily Limit
    PRECONDITIONS: In order to register new payment method use:
    PRECONDITIONS: Debit/Credit Cards:
    PRECONDITIONS: *   http://www.getcreditcardnumbers.com/how-to-get-a-master-card-credit-card
    PRECONDITIONS: *   http://www.getcreditcardnumbers.com/how-to-get-a-visa-credit-card
    PRECONDITIONS: PayPal:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: NETELLER: http://www.scribd.com/doc/61457666/API-Testing-101022#scribd
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   'My Payments' tab is selected by default
        """
        pass

    def test_002_verify_my_payments_tab(self):
        """
        DESCRIPTION: Verify 'My Payments' tab
        EXPECTED: *   Drop-down list with existing registered cards is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_003_select_creditdebit_card_from_drop_down_and_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Select **Credit/Debit Card** from drop-down and fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_thatexceeds_daily_limit(self):
        """
        DESCRIPTION: Enter amount that exceeds Daily Limit
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_005_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: *   Error message: **"This deposit would exceed your self-imposed deposit limit. Check your current limit here."** is shown
        EXPECTED: *   User stays on 'My Payments' tab
        EXPECTED: *   User Balance is not changed
        EXPECTED: *   Entered amount is not cleared
        EXPECTED: *   All other fields are cleared
        """
        pass

    def test_006_verify_here_hyperlink(self):
        """
        DESCRIPTION: Verify '*here*' hyperlink
        EXPECTED: '*here*' is hyperlinked and takes user to the '**My Limits**' page
        """
        pass

    def test_007_repeat_steps_1_7_for_paypal(self):
        """
        DESCRIPTION: Repeat steps #1-7 for **PayPal **
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_7_for__neteller(self):
        """
        DESCRIPTION: Repeat steps #1-7 for  **NETELLER**
        EXPECTED: 
        """
        pass

    def test_009_deposit_via_any_payment_method_with_an_amount_that_does_not_exceed_daily_limit_and_tap_deposit_button(self):
        """
        DESCRIPTION: Deposit via any Payment Method with an amount that does NOT exceed Daily Limit and tap 'Deposit' button
        EXPECTED: *   Successful message is shown
        EXPECTED: *   User stays on the 'My Payments' tab
        EXPECTED: *   All fields are cleared
        """
        pass

    def test_010_deposit_via_other_payment_method_with_an_amount_that_in_sum_with_amount_from_previous_steps_exceeds_daily_limit(self):
        """
        DESCRIPTION: Deposit via other Payment Method with an amount that in sum with amount from previous steps exceeds Daily Limit
        EXPECTED: *   Error message: **"This deposit would exceed your self-imposed deposit limit. Check your current limit here."** is shown
        EXPECTED: *   User stays on the 'My Payments' tab
        EXPECTED: *   User Balance is not changed
        EXPECTED: *   Entered amount is not cleared
        EXPECTED: *   All other fields are cleared
        """
        pass
