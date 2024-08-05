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
class Test_C28312_Verify_Pending_Withdrawal(Common):
    """
    TR_ID: C28312
    NAME: Verify Pending Withdrawal
    DESCRIPTION: This test case verifies Pending Withdrawal.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered Debit/Credit Card, PayPal and NETELLER methods
    PRECONDITIONS: *   Balance of account is enough for withdraw from
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_button(self):
        """
        DESCRIPTION: Tap 'Withdraw' button
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        """
        pass

    def test_003_select_debitcredit_card(self):
        """
        DESCRIPTION: Select Debit/Credit Card
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_005_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Successfull message: **"Your withdrawal request has been successful.Reference: #XXXXXXX"** *(ID of successful response )** is shown
        EXPECTED: *   User stays on the 'Withdraw Funds' page (refreshed with clear form)
        """
        pass

    def test_006_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is decreased by amount set in step №4
        """
        pass

    def test_007_go_to_my_account___transaction_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Transaction History' page
        EXPECTED: *   'Transactions' tab on 'Account History' page is opened
        EXPECTED: *   'Deposit' button is selected by default
        """
        pass

    def test_008_tap_withdraw_button(self):
        """
        DESCRIPTION: Tap 'Withdraw' button
        EXPECTED: 
        """
        pass

    def test_009_tap_pending_tab(self):
        """
        DESCRIPTION: Tap 'Pending' tab
        EXPECTED: *   'Pending' tab is selected
        EXPECTED: *   Previously made withdrawals are displayed
        """
        pass

    def test_010_verify_that_the_transaction_info_is_correct(self):
        """
        DESCRIPTION: Verify that the transaction info is correct
        EXPECTED: 4 columns are displayed:
        EXPECTED: *   **Type of payment method**
        EXPECTED: *   **'Date/Time:' **label, date of withdrawal in format: DD-MM-YYYY  HH:MM (24-hour clock) and card number in format: '\**\*|\* <**the last 4 digits of the **used** card**>'
        EXPECTED: *   **'Amount:'** label and value of withdrawal with **<currency symbol>**
        EXPECTED: *   '**Cancel**' button
        EXPECTED: * All information regarding the card (last 4 digits, label) corresponds to the card, from which the withdrawal was made
        """
        pass

    def test_011_tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button
        EXPECTED: *   **'Cancel Withdrawal'** pop-up is shown
        EXPECTED: *   Message **'Are you sure you wish to cancel the withdrawal?'**
        EXPECTED: *   Two buttons: '**Close**' and **'Yes, cancel it!'**
        """
        pass

    def test_012_tap_close_button(self):
        """
        DESCRIPTION: Tap 'Close' button
        EXPECTED: **'Cancel Withdrawal'**  pop-up is closed
        """
        pass

    def test_013_repeat_step_9(self):
        """
        DESCRIPTION: Repeat step №9
        EXPECTED: 
        """
        pass

    def test_014_tap_yes_cancel_it_button(self):
        """
        DESCRIPTION: Tap 'Yes cancel it!' button
        EXPECTED: *   **'Your withdrawal has been successfully canceled!'** message is shown
        EXPECTED: *   Withdrawal transaction record disappears from 'Pending' tab
        EXPECTED: *   User Balance is incremented on amount set on step №4
        """
        pass

    def test_015_make_sure_to_repeat_steps_1_14_with_mastercard_and_visa_cards(self):
        """
        DESCRIPTION: Make sure to repeat steps 1-14 with Mastercard and VISA cards
        EXPECTED: 
        """
        pass

    def test_016_go_to_withdraw_funds_page(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page
        EXPECTED: 
        """
        pass

    def test_017_select_paypal_method(self):
        """
        DESCRIPTION: Select PayPal method
        EXPECTED: 
        """
        pass

    def test_018_repeat_steps_4_14(self):
        """
        DESCRIPTION: Repeat steps №4-14
        EXPECTED: 
        """
        pass

    def test_019_go_to_withdraw_funds_page(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page
        EXPECTED: 
        """
        pass

    def test_020_select_neteller_method(self):
        """
        DESCRIPTION: Select NETELLER method
        EXPECTED: 
        """
        pass

    def test_021_repeat_steps_4_14(self):
        """
        DESCRIPTION: Repeat steps №4-14
        EXPECTED: 
        """
        pass
