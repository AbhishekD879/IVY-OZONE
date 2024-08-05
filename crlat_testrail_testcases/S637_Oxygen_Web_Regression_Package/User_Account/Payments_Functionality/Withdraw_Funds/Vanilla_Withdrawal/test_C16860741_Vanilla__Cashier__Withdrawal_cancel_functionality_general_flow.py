import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C16860741_Vanilla__Cashier__Withdrawal_cancel_functionality_general_flow(Common):
    """
    TR_ID: C16860741
    NAME: [Vanilla] - Cashier - Withdrawal cancel functionality (general flow)
    DESCRIPTION: The purpose of this TC is verification of canceling Withdrawal by User from Menu;
    PRECONDITIONS: 1. User should register at least 1 payment method (e.g VISA);
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

    def test_003_click_on_the_withdraw_section_and_select_the_visa_payment_method__visa_should_be_added_before_deposit(self):
        """
        DESCRIPTION: Click On the "Withdraw" section and select the Visa payment method;
        DESCRIPTION: - Visa should be added before deposit.
        EXPECTED: Withdrawal page for Visa is opened;
        """
        pass

    def test_004_1_enter_amount_for_withdraw2_select_desired_cardaccount_id3_click_on_withdrawal_button(self):
        """
        DESCRIPTION: 1. Enter Amount for Withdraw;
        DESCRIPTION: 2. Select desired Card/Account ID;
        DESCRIPTION: 3. Click on 'Withdrawal' button;
        EXPECTED: Withdrawal is performed and Withdrawal ticket is displayed with id of the transaction;
        """
        pass

    def test_005_go_to_cashier_menu(self):
        """
        DESCRIPTION: Go to Cashier Menu
        EXPECTED: Cashier Menu is opened
        """
        pass

    def test_006_click_on_cancel_withdraw_selection(self):
        """
        DESCRIPTION: Click on "Cancel Withdraw" selection;
        EXPECTED: "Cancel Withdraw" menu is opened with a description of previously performed Withdraw;
        """
        pass

    def test_007_click_on_cancel_withdrawal(self):
        """
        DESCRIPTION: Click on "Cancel Withdrawal"
        EXPECTED: Withdrawal is canceled
        """
        pass

    def test_008_check_that_ballance_is_changed(self):
        """
        DESCRIPTION: Check that ballance is changed
        EXPECTED: Balance updated and rise on the sum of Withdrawal
        """
        pass
