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
class Test_C28292_Verify_Withdraw_Funds_page_with_registered_Payment_Methods(Common):
    """
    TR_ID: C28292
    NAME: Verify Withdraw Funds page with registered Payment Methods
    DESCRIPTION: This test case verifies view of the Withdraw Funds page with registered Payment Methods.
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has more than one registered cards/PayPal account/NETELLER account
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
        EXPECTED: 'Withdraw Funds' page is opened
        """
        pass

    def test_003_verify_withdraw_funds_page(self):
        """
        DESCRIPTION: Verify 'Withdraw Funds' page
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_004_verify_drop_down_items(self):
        """
        DESCRIPTION: Verify drop-down items
        EXPECTED: *   Drop-down consists of Names of the added Payment Methods
        EXPECTED: *   Name of card in format:** <The card type name> (\**\*|\\* \*\*|\\*\* \*|\\***| <the last 4 digits of the added card>). **Card type name can be: Visa, Visa Electron, MasterCard, Maestro
        EXPECTED: *   Name of NETELLER account in format: **NETELLER (Account ID** or **Email****)**
        EXPECTED: *   Name of PayPal account in format: **PayPal (email@address.com)**
        """
        pass

    def test_005_verify_account_balance(self):
        """
        DESCRIPTION: Verify Account Balance
        EXPECTED: 'Account Balance:' label is shown with current user balance in format '<currency>XXX,XXX.XX'
        """
        pass

    def test_006_verify_quick_withdraw_buttons(self):
        """
        DESCRIPTION: Verify quick withdraw buttons
        EXPECTED: 1.  Quick withdraw buttons are displayed below the 'Withdraw Amount:' label
        EXPECTED: 2.  The following values are shown:
        EXPECTED: *   5
        EXPECTED: *   10
        EXPECTED: *   20
        EXPECTED: *   50
        EXPECTED: *   100
        """
        pass

    def test_007_verify_amount_edit_field(self):
        """
        DESCRIPTION: Verify amount edit field
        EXPECTED: 'Enter Amount Manually...' text is displayed by default in amount field
        """
        pass

    def test_008_verify_withdraw_funds_button(self):
        """
        DESCRIPTION: Verify 'Withdraw Funds' button
        EXPECTED: 'Withdraw Funds' button is enabled by default
        """
        pass
