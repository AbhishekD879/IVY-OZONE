import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C874246_Verify_Quick_Deposit_section_for_users_with_balance_lesser_bigger_than_100(Common):
    """
    TR_ID: C874246
    NAME: Verify Quick Deposit section for users with balance lesser/bigger than 100
    DESCRIPTION: This test case verifies Quick Deposit section for users with balance lesser/bigger than 100
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. Users have the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_that_has_balance_less_than_100_a_few_credit_cards_and_paypal_or_neteller_payment_method_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has balance less than 100, a few credit cards and Paypal or Neteller payment method added to his account
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - the currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * 'Quick Deposit' section is displayed within Quick Bet
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        """
        pass

    def test_005_verify_payment_methods_available(self):
        """
        DESCRIPTION: Verify Payment methods available
        EXPECTED: * All credit cards are displayed within Quick Deposit section
        EXPECTED: * Paypal and Neteller payments are NOT displayed event if one of them is default payment method
        """
        pass

    def test_006_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is logged out
        """
        pass

    def test_007_log_in_with_user_that_has_balance_bigger_than_100_a_few_credit_cards_and_paypal_or_neteller_payment_method_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has balance bigger than 100, a few credit cards and Paypal or Neteller payment method added to his account
        EXPECTED: User is logged in
        """
        pass

    def test_008_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_009_verify_payment_methods_available(self):
        """
        DESCRIPTION: Verify Payment methods available
        EXPECTED: * Only last added credit card is displayed Quick Deposit section
        EXPECTED: * Paypal and Neteller payments are NOT displayed event if one of them is default payment method
        """
        pass
