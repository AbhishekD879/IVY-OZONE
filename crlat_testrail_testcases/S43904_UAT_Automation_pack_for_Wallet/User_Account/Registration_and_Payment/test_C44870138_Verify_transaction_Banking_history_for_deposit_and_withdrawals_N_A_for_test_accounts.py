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
class Test_C44870138_Verify_transaction_Banking_history_for_deposit_and_withdrawals_N_A_for_test_accounts(Common):
    """
    TR_ID: C44870138
    NAME: Verify transaction/Banking history for deposit and withdrawals  (N/A for test accounts)
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has at least one registered card
    PRECONDITIONS: Balance of account is enough for withdraw from
    """
    keep_browser_open = True

    def test_001_go_to_my_account_tap_on_the_avatar___history____payment_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' (tap on the Avatar) -> 'History' --> 'Payment History' page
        EXPECTED: Payment History page is opened with the 'ALL/DEPOSIT/WITHDRAWAL'
        EXPECTED: Product Type is set to All by default
        EXPECTED: Transaction type is set to All by default
        EXPECTED: Option of Payment method with a drop down to choose the cards is available.
        """
        pass

    def test_002_select_the_product_alldepositwithdrawal_type_from_the_list(self):
        """
        DESCRIPTION: Select the product (ALL/DEPOSIT/WITHDRAWAL) type from the list
        EXPECTED: All the activities performed on the selected product type for the last 24 hrs should be displayed to the user
        """
        pass

    def test_003_choose_any_one__transaction_type_from_the_drop_down_list(self):
        """
        DESCRIPTION: Choose any one  Transaction Type from the drop down list
        EXPECTED: 
        """
        pass

    def test_004_verify__if_transaction_type____deposit_is_selected_and_click_on_go_tab(self):
        """
        DESCRIPTION: Verify  if transaction Type -  '**Deposit**' is selected and click on 'GO' tab
        EXPECTED: The following information is displayed:
        EXPECTED: List of transactions (if it is available)
        EXPECTED: '**No transactions to display .**'  message is displayed (if there are no transactions)
        """
        pass

    def test_005_verify__if_transaction_type____withdrawal_is_selected_and_click_on_go_tab(self):
        """
        DESCRIPTION: Verify  if transaction Type -  '**Withdrawal**' is selected and click on 'GO' tab
        EXPECTED: Page Contains the list of withdrawal information is displayed.
        EXPECTED: Note: Withdrawals are not allowed for test accounts.
        """
        pass
