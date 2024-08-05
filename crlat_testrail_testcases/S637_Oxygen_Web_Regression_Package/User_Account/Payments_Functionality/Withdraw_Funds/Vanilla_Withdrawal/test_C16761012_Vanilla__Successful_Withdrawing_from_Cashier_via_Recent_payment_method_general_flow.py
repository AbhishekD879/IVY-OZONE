import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.other
@vtest
class Test_C16761012_Vanilla__Successful_Withdrawing_from_Cashier_via_Recent_payment_method_general_flow(Common):
    """
    TR_ID: C16761012
    NAME: [Vanilla] - Successful Withdrawing from Cashier via Recent payment method  (general flow)
    DESCRIPTION: This test case verifies Withdraw of Funds for registered Payment Methods.
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

    def test_003_click_on_withdraw_section(self):
        """
        DESCRIPTION: Click On "Withdraw" section
        EXPECTED: "Withdraw" menu is opened with a list of all available payment methods for the User;
        EXPECTED: 1. VISA
        EXPECTED: 2. MasterCard
        EXPECTED: 3. Netteller
        EXPECTED: 4. PayPal
        """
        pass

    def test_004_select_visa_payment_method__visa_should_be_added_before_deposit(self):
        """
        DESCRIPTION: Select Visa payment method;
        DESCRIPTION: - Visa should be added before deposit.
        EXPECTED: Withdrawal page for Visa is opened;
        """
        pass

    def test_005_1_enter_amount_for_withdraw2_select_desired_cardaccount_id3_enter_security_codeid4_click_on_withdrawal_button(self):
        """
        DESCRIPTION: 1. Enter Amount for Withdraw;
        DESCRIPTION: 2. Select desired Card/Account ID;
        DESCRIPTION: 3. Enter Security code/id
        DESCRIPTION: 4. Click on 'Withdrawal' button;
        EXPECTED: Withdrawal is performed and Withdrawal ticket is displayed with id of the transaction;
        """
        pass

    def test_006_verify_that_balance_is_changed(self):
        """
        DESCRIPTION: Verify that balance is changed;
        EXPECTED: Ballance changed and reduced equally to the amount of Withdrawal;
        """
        pass
