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
class Test_C28293_Verify_Initial_Payment_Methods_Order_on_the_Withdraw_Funds_page(Common):
    """
    TR_ID: C28293
    NAME: Verify Initial Payment Methods Order on the Withdraw Funds page
    DESCRIPTION: This test case verifies Initial Payment Methods Order on the Withdraw Funds page
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has more than one registered cards
    PRECONDITIONS: *   User has registered PayPal account
    PRECONDITIONS: *   User has NETELLER account registered
    PRECONDITIONS: *   User has never deposited before
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

    def test_003_verify_payment_methods_order_in_the_drop_down_list(self):
        """
        DESCRIPTION: Verify Payment Methods order in the drop-down list
        EXPECTED: The Payment Method that was last added is listed at the top of the drop-down list
        """
        pass

    def test_004_add_new_debitcredit_card_successfully_go_to_withdraw_funds_page__verify_payment_methods_order(self):
        """
        DESCRIPTION: Add new Debit/Credit card successfully => Go to 'Withdraw Funds' page => Verify Payment Methods order
        EXPECTED: Card added last is displayed at the top of the list
        """
        pass

    def test_005_add_new_paypal_account__go_to_withdraw_funds_page__verify_payment_methods_order(self):
        """
        DESCRIPTION: Add new PayPal account => Go to 'Withdraw Funds' page => Verify Payment Methods order
        EXPECTED: PayPal account added last is displayed at the top of the list
        """
        pass

    def test_006_add_new_neteller_account__go_to_withdraw_funds_page__verify_payment_methods_order(self):
        """
        DESCRIPTION: Add new NETELLER account => Go to 'Withdraw Funds' page => Verify Payment Methods order
        EXPECTED: NETELLER account added last is displayed at the top of the list
        """
        pass
