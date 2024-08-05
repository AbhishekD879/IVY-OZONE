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
class Test_C44870132_Add_multiple_payment_methods_to_users_account_and_Deposit_money_Paypal_Paysafe_card_Add_Skrill_Neteller_(Common):
    """
    TR_ID: C44870132
    NAME: Add multiple payment methods to user's account and Deposit money ( Paypal ,Paysafe card  ,Add Skrill , Neteller )
    DESCRIPTION: 
    PRECONDITIONS: User has a valid accounts from which his/her can deposit funds
    PRECONDITIONS: Balance is enough for depositing
    PRECONDITIONS: Note: For test accounts only Master card, Visa & Maestro are available.
    """
    keep_browser_open = True

    def test_001_log_into_an_app(self):
        """
        DESCRIPTION: Log into an app
        EXPECTED: 
        """
        pass

    def test_002_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_003_tap_add_a_new_payment_method_and_select_required_payment_method_tab(self):
        """
        DESCRIPTION: Tap 'Add A New Payment Method' and select required payment method tab
        EXPECTED: 
        """
        pass

    def test_004_select_paypal_payment_method(self):
        """
        DESCRIPTION: Select PayPal payment method
        EXPECTED: 
        """
        pass

    def test_005_quick_deposit_buttons_are_displayed_below_the_amount_limit_labelthe_following_values_are_shown51525(self):
        """
        DESCRIPTION: Quick deposit buttons are displayed below the '**Amount Limit':** label
        DESCRIPTION: The following values are shown:
        DESCRIPTION: £5
        DESCRIPTION: £15
        DESCRIPTION: £25
        EXPECTED: 
        """
        pass

    def test_006_verify_amount_edit_field(self):
        """
        DESCRIPTION: Verify Amount edit field
        EXPECTED: 'Amount:' label and edit field are present below the quick deposit buttons
        EXPECTED: Amount field is £5 by default
        """
        pass

    def test_007_verify_deposit_button(self):
        """
        DESCRIPTION: Verify 'Deposit' button
        EXPECTED: Deposit' button is enabled by default
        """
        pass

    def test_008_verify_checkbox_skip_paypal_payment_confirmation_page_for_your_future_payments_by_accepting_paypal_agreement(self):
        """
        DESCRIPTION: Verify checkbox "Skip PayPal payment confirmation page for your future payments, by accepting PayPal agreement"."
        EXPECTED: Select the check box
        """
        pass

    def test_009_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on Deposit button
        EXPECTED: User is taken to Paypal Login page
        """
        pass

    def test_010_enter_valid_credential_and_login(self):
        """
        DESCRIPTION: Enter valid credential and login
        EXPECTED: User is loggen in to paypal account
        """
        pass

    def test_011_submit_paypal_form__tap_pay_now_button(self):
        """
        DESCRIPTION: Submit PayPal form > Tap 'Pay Now' button
        EXPECTED: User is redirected to 'My Payments' tab
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.**
        """
        pass

    def test_012_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is increased with amount set in step #5
        """
        pass

    def test_013_verify_paypal_account_on_my_payments_tab(self):
        """
        DESCRIPTION: Verify PayPal account on 'My Payments' tab
        EXPECTED: PayPal payment method is shown first in 'Select Payment Method' drop-down list in format:
        EXPECTED: "PayPal (email@address.com)"
        EXPECTED: Text is available below 'Select Payment Method' drop down: "Your Registered PayPal Account: email@address.com In order to change your PayPal account, please contact customer support."
        """
        pass

    def test_014_tap_add_neteller_tab(self):
        """
        DESCRIPTION: Tap 'Add NETELLER' tab
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps 5-7
        EXPECTED: 
        """
        pass

    def test_016_enter_valid_account_or_email_into_account_idemail_field(self):
        """
        DESCRIPTION: Enter valid Account or Email into 'Account ID/Email:' field
        EXPECTED: Account/Email is displayed
        """
        pass

    def test_017_enter_valid_security_id_into_secure_id_or_authentication_code_fiels(self):
        """
        DESCRIPTION: Enter valid Security ID into 'Secure ID or Authentication Code:' fiels
        EXPECTED: Secure ID or Authentication Code is displayed
        """
        pass

    def test_018_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_019_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: User is redirected to 'My Payments' tab
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"**
        EXPECTED: All fields are cleared
        EXPECTED: 'Deposit' button is enabled
        """
        pass

    def test_020_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is increased on amount set on step №18
        """
        pass

    def test_021_verify_drop_down_list(self):
        """
        DESCRIPTION: Verify drop-down list
        EXPECTED: NETELLER payment method is shown at the top of the registered payments drop down list in format:
        EXPECTED: "NETELLER (Account ID **or **Email **form their Neteller account)"**
        """
        pass

    def test_022_tap_add_paysafecard_tab(self):
        """
        DESCRIPTION: Tap Add Paysafecard tab
        EXPECTED: Add Paysafecard tab is selected
        """
        pass

    def test_023_enter_valid_amount_manually_or_via_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or via quick deposit buttons
        EXPECTED: Amount value is displayed in Amount edit field
        """
        pass

    def test_024_tap_deposit_button(self):
        """
        DESCRIPTION: Tap Deposit button
        EXPECTED: Paysafecard iframe page is opened where user is able to submit Paysafecard form
        """
        pass

    def test_025_submit_paysafecard_form(self):
        """
        DESCRIPTION: Submit Paysafecard form
        EXPECTED: User is redirected to My Payments tab
        EXPECTED: Successful message: Your deposit of <currency symbol> XX.XX was successful. appears
        EXPECTED: All fields are cleared off
        EXPECTED: Deposit button is active
        """
        pass

    def test_026_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is increased on amount set on step №23
        """
        pass

    def test_027_verify_dropdown_list(self):
        """
        DESCRIPTION: Verify dropdown list
        EXPECTED: Paysafecard payment method is shown at the top of the registered payments dropdown list in the format: PaySafeCard
        """
        pass

    def test_028_tap_add_skrill_tab(self):
        """
        DESCRIPTION: Tap Add Skrill tab
        EXPECTED: Add Skrill tab is selected
        """
        pass

    def test_029_enter_valid_amount_manually_or_via_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or via quick deposit buttons
        EXPECTED: Amount value is displayed in Amount edit field
        EXPECTED: Deposit button is active
        """
        pass

    def test_030_tap_deposit_button(self):
        """
        DESCRIPTION: Tap Deposit button
        EXPECTED: Skrill iframe page is opened where user is able to submit Skrill form
        """
        pass

    def test_031_submit_skrill_form(self):
        """
        DESCRIPTION: Submit Skrill form
        EXPECTED: User is redirected to My Payments tab
        EXPECTED: Successful message: Your deposit of <currency symbol> XX.XX was successful. appears
        EXPECTED: All fields are cleared off
        EXPECTED: Deposit button is active
        """
        pass

    def test_032_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is increased on amount set on step №29
        """
        pass

    def test_033_verify_dropdown_list(self):
        """
        DESCRIPTION: Verify dropdown list
        EXPECTED: Skrill payment method is shown at the top of the registered payments dropdown list in the format: Skrill (Account ID)
        """
        pass
