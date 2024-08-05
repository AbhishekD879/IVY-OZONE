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
class Test_C44870138_Verify_transaction_Banking_history_for_deposit_and_withdrawals(Common):
    """
    TR_ID: C44870138
    NAME: Verify transaction/Banking history for deposit and withdrawals
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has at least one registered card
    PRECONDITIONS: Balance of account is enough for withdraw from
    """
    keep_browser_open = True

    def test_001_go_to_my_account_tap_on_the_avatar___payment_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' (tap on the Avatar) -> 'Payment History' page
        EXPECTED: Payment History page is opened
        EXPECTED: 'Transactions Period' is set to Last 24 hrs by default  on 'Account History' page
        EXPECTED: Product Type is set to All by default
        EXPECTED: Transaction type is set to All by default
        """
        pass

    def test_002_select_the_product_type_from_the_drop_down_list(self):
        """
        DESCRIPTION: Select the product type from the drop down list
        EXPECTED: All the activities performed on the selected product type for the last 24 hrs should be displayed to the user
        """
        pass

    def test_003_choose_any_one__transaction_type_from_the_drop_down_list(self):
        """
        DESCRIPTION: Choose any one  Transaction Type from the drop down list
        EXPECTED: 
        """
        pass

    def test_004_verify__if_transaction_type____deposit_is_selected(self):
        """
        DESCRIPTION: Verify  if transaction Type -  '**Deposit**' is selected
        EXPECTED: The following information is displayed:
        EXPECTED: List of transactions (if it is available)
        EXPECTED: '**You have no transaction .**'  message is displayed (if there are no transactions)
        """
        pass

    def test_005_verify__if_transaction_type____withdraw_request_is_selected(self):
        """
        DESCRIPTION: Verify  if transaction Type -  '**Withdraw Request**' is selected
        EXPECTED: Page Contains the list of withdrawal requests with date,withdrawal request text and Amount
        EXPECTED: When each twistee is expanded user sees below info
        EXPECTED: - Time,Product,Balance,transaction Id,Request to Withdrawal funds msg
        """
        pass

    def test_006_verify__if_transaction_type____withdraw_declined_is_selected(self):
        """
        DESCRIPTION: Verify  if transaction Type -  '**Withdraw Declined**' is selected
        EXPECTED: Page Contains the list of  declined v with date,withdrawal request text and Amount
        EXPECTED: When each twistee is expanded user sees below info
        EXPECTED: - Time,Product,Balance,transaction Id,Cancelling a pending withdrawal request and returning funds to payable cash balance
        """
        pass
