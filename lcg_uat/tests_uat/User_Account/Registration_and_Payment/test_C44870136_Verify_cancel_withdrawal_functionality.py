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
class Test_C44870136_Verify_cancel_withdrawal_functionality(Common):
    """
    TR_ID: C44870136
    NAME: Verify cancel withdrawal functionality
    DESCRIPTION: 
    PRECONDITIONS: User logged into the application;
    PRECONDITIONS: User performed Withdrawal
    """
    keep_browser_open = True

    def test_001_click__right_menu(self):
        """
        DESCRIPTION: Click  Right menu
        EXPECTED: User menu is opened;
        """
        pass

    def test_002_click_on_banking(self):
        """
        DESCRIPTION: Click on Banking
        EXPECTED: Banking page with following fields are displayed
        EXPECTED: Deposit
        EXPECTED: Deposit Limits
        EXPECTED: Transfer
        EXPECTED: Withdraw
        EXPECTED: View balances
        EXPECTED: banking History
        """
        pass

    def test_003_select__withdraw_from_banking_page(self):
        """
        DESCRIPTION: Select  Withdraw from banking page
        EXPECTED: Withdrawal page is opened
        """
        pass

    def test_004_tap_on_withdrawal_twistee(self):
        """
        DESCRIPTION: Tap on Withdrawal twistee
        EXPECTED: Banking section is expanded with the following elemnts
        EXPECTED: Deposit
        EXPECTED: Deposit Limits
        EXPECTED: Transfer
        EXPECTED: Withdrawal
        EXPECTED: Pending Withdrawal
        EXPECTED: View balances
        """
        pass

    def test_005_select_pending_withdrawals(self):
        """
        DESCRIPTION: Select pending withdrawals
        EXPECTED: User is taken to pending withdrawals page
        EXPECTED: User sees the all the relevant info as below
        EXPECTED: - Date of withdrawal
        EXPECTED: - Amount
        EXPECTED: - Cancel Button
        """
        pass

    def test_006_expand_the_twistee_present_beside_cancel_button(self):
        """
        DESCRIPTION: Expand the twistee present beside cancel button
        EXPECTED: User should see all the info about withdrawal
        EXPECTED: - Time,Account,Method,Wallet,Transaction Id
        """
        pass

    def test_007_click_on_cancel_withdraw_selection(self):
        """
        DESCRIPTION: Click on "Cancel Withdraw" selection;
        EXPECTED: "Cancel Withdraw Successful" popup is shown with Done and X options
        """
        pass

    def test_008_check_that_balance_is_updated(self):
        """
        DESCRIPTION: Check that balance is updated
        EXPECTED: 
        """
        pass
