import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28297_Verify_Currency_on_the_Withdraw_Funds_page(Common):
    """
    TR_ID: C28297
    NAME: Verify Currency on the Withdraw Funds page
    DESCRIPTION: This test case verifies Verify Currency on the Withdraw Funds page
    PRECONDITIONS: *   Each user has at least one registered Payment Method
    PRECONDITIONS: *   Make sure you have 4 registered users with different currency settings: GBP, EUR, USD, SEK
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = **£**;
    PRECONDITIONS: *   'USD': symbol = **$**;
    PRECONDITIONS: *   'EUR': symbol = **€'**;
    PRECONDITIONS: *   'SEK': symbol = **Kr**
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_003_tap_withdraw_menu_item(self):
        """
        DESCRIPTION: Tap 'Withdraw' menu item
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Last used Payment Method is selected by default
        """
        pass

    def test_004_verify_currency_symbol_next_to_the_quick_deposit_buttons1__52__103__204__505__100(self):
        """
        DESCRIPTION: Verify currency symbol next to the quick deposit buttons:
        DESCRIPTION: 1.  5
        DESCRIPTION: 2.  10
        DESCRIPTION: 3.  20
        DESCRIPTION: 4.  50
        DESCRIPTION: 5.  100
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_005_enter_invalid_amount_into_amount_edit_field_tap_withdraw_funds_button_and_verify_currency_symbol(self):
        """
        DESCRIPTION: Enter invalid amount into amount edit field, tap 'Withdraw Funds' button and verify currency symbol
        EXPECTED: *   Error message  "**The minimum withdraw amount is **<currency symbol> **5**" is shown
        EXPECTED: *   Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_006_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        pass

    def test_007_log_in_user_witheurcurrency(self):
        """
        DESCRIPTION: Log in user with **EUR **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_008_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps №2-5
        EXPECTED: The same as on the steps №2-9
        """
        pass

    def test_009_log_in_user_with_usdcurrency(self):
        """
        DESCRIPTION: Log in user with **USD **currency
        EXPECTED: User is logged out successfully
        """
        pass

    def test_010_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps №2-5
        EXPECTED: The same as on the steps №2-9
        """
        pass

    def test_011_log_in_user_withsekcurrency(self):
        """
        DESCRIPTION: Log in user with **SEK **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_012_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps №2-5
        EXPECTED: In step #4 currency symbol IS NOT shown near the quick deposit buttons.
        EXPECTED: The currency symbol is displayed near the 'Quick Amount' label. It is shown in brackets
        EXPECTED: Also the quick amount values are: 50, 100. 200, 500, 1000
        """
        pass
