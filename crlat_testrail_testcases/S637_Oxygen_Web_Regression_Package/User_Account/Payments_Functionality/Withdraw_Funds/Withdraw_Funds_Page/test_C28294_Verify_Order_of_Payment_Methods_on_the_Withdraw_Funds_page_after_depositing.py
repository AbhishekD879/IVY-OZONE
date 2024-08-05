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
class Test_C28294_Verify_Order_of_Payment_Methods_on_the_Withdraw_Funds_page_after_depositing(Common):
    """
    TR_ID: C28294
    NAME: Verify Order of Payment Methods on the Withdraw Funds page after depositing
    DESCRIPTION: This test case verifies Order of Payment Methods on the Withdraw Funds page after depositing
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has more than one registered cards with positive balance
    PRECONDITIONS: *   User has registered PayPal account with positive balance
    PRECONDITIONS: *   User has NETELLER account registered with positive balance
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_menu_item(self):
        """
        DESCRIPTION: Tap 'Withdraw' menu item
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_003_verify_payment_methodsorder_in_the_drop_down_list(self):
        """
        DESCRIPTION: Verify Payment Methods order in the drop-down list
        EXPECTED: *   The Payment Method that was last added is listed at the top of the drop-down list
        EXPECTED: *   This Payment Method is selected by default
        """
        pass

    def test_004_go_to_deposit_page__select_creditdebit_card_from_the_bottom_of_the_drop_down(self):
        """
        DESCRIPTION: Go to 'Deposit' page => Select **Credit/Debit card** from the bottom of the drop-down
        EXPECTED: 
        """
        pass

    def test_005_make_successful_deposit_from_this_creditdebit_card(self):
        """
        DESCRIPTION: Make successful deposit from this Credit/Debit card
        EXPECTED: 
        """
        pass

    def test_006_go_to_withdraw_funds_page__verify_payment_methods_order_in_the_drop_down_list(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page => Verify Payment Methods order in the drop-down list
        EXPECTED: Card selected on step №4 is selected as default and displayed on the top of drop-down list
        """
        pass

    def test_007_go_to_deposit_page__selectpaypalaccountfrom_the_drop_down(self):
        """
        DESCRIPTION: Go to 'Deposit' page => Select **PayPal **account from the drop-down
        EXPECTED: 
        """
        pass

    def test_008_make_successful_deposit_from_this_paypal_account(self):
        """
        DESCRIPTION: Make successful deposit from this PayPal account
        EXPECTED: 
        """
        pass

    def test_009_go_to_withdraw_funds_page__verify_payment_methods_order_in_the_drop_down_list(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page => Verify Payment Methods order in the drop-down list
        EXPECTED: PayPal account selected on step №7 is selected as default and displayed on the top of drop-down list
        """
        pass

    def test_010_go_to_deposit_page__select_neteller_accountfrom_the_drop_down(self):
        """
        DESCRIPTION: Go to 'Deposit' page => Select **NETELLER **account from the drop-down
        EXPECTED: 
        """
        pass

    def test_011_make_successful_deposit_from_this_neteller_account(self):
        """
        DESCRIPTION: Make successful deposit from this NETELLER account
        EXPECTED: 
        """
        pass

    def test_012_go_to_withdraw_funds_page__verify_payment_methods_order_in_the_drop_down_list(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page => Verify Payment Methods order in the drop-down list
        EXPECTED: NETELLER account selected on step №10  is selected as default and displayed on the top of drop-down list
        """
        pass

    def test_013_go_to_deposit_page__add_new_debitcredit_card(self):
        """
        DESCRIPTION: Go to 'Deposit' page => Add new debit/credit card
        EXPECTED: *   'Deposit Methods' tab is opened
        EXPECTED: *   Success message **'Your card was added successfully.'** is displayed
        """
        pass

    def test_014_go_to_withdraw_funds_page__verify_cards_order(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page => Verify cards order
        EXPECTED: Card added on the previous step is displayed at the top of the list
        """
        pass
