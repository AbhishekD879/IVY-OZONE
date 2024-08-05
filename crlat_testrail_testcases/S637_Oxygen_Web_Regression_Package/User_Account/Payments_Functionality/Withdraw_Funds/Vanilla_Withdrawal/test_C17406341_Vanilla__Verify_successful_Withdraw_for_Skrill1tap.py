import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C17406341_Vanilla__Verify_successful_Withdraw_for_Skrill1tap(Common):
    """
    TR_ID: C17406341
    NAME: [Vanilla] - Verify successful Withdraw for Skrill1tap
    DESCRIPTION: This test case verifies Withdraw of Funds for registered Payment Methods.
    PRECONDITIONS: 1. User should register at least 1 payment method - Skrill1tap;
    PRECONDITIONS: 2. User logged into the application;
    PRECONDITIONS: 3. User performed Deposit for registered payment Method;
    """
    keep_browser_open = True

    def test_001_click_on_user_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on User "Avatar" icon on the header.
        EXPECTED: User menu is opened;
        """
        pass

    def test_002_click_on_cashier_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Cashier" section in User menu;
        EXPECTED: Cashier Menu is opened and "Withdraw" section is present there;
        """
        pass

    def test_003_click_on_withdraw_section(self):
        """
        DESCRIPTION: Click On "Withdraw" section
        EXPECTED: "Withdraw" menu is opened with a list of all available payment methods for the User;
        """
        pass

    def test_004_select_skrill1tap_payment_method__skrill1tap_should_be_added_before_deposit(self):
        """
        DESCRIPTION: Select Skrill1tap payment method;
        DESCRIPTION: - Skrill1tap should be added before deposit.
        EXPECTED: Withdrawal page for Safecharge is opened;
        """
        pass

    def test_005_1_enter_amount_for_withdraw2_select_desired_cardaccount_id3_click_on_withdrawal_button(self):
        """
        DESCRIPTION: 1. Enter Amount for Withdraw;
        DESCRIPTION: 2. Select desired Card/Account ID;
        DESCRIPTION: 3. Click on 'Withdrawal' button;
        EXPECTED: Withdrawal is performed and Withdrawal ticket is displayed with the id of the transaction;
        """
        pass

    def test_006_verify_that_balance_is_changed(self):
        """
        DESCRIPTION: Verify that balance is changed;
        EXPECTED: Ballance changed and reduced equally to the amount of Withdrawal;
        """
        pass
