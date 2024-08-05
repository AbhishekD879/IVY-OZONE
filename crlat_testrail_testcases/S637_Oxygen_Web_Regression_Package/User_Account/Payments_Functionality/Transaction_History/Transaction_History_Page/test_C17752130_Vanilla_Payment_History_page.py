import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C17752130_Vanilla_Payment_History_page(Common):
    """
    TR_ID: C17752130
    NAME: [Vanilla] Payment History page
    DESCRIPTION: This test case verifies Payment History page.
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has at least one registered card
    PRECONDITIONS: *   Balance of account is enough for withdraw from
    """
    keep_browser_open = True

    def test_001_go_to_menu___history__payment_history_page(self):
        """
        DESCRIPTION: Go to 'Menu' -> 'History' ->'Payment History' page
        EXPECTED: *   'Payment History' page is opened
        EXPECTED: *   Three buttons are visible: ' **All** ', ' **Deposit** ' and ' **Withdraw** '
        EXPECTED: *   ' **All** ' button is selected by default
        EXPECTED: *   A list box with available payments is displayed, 'Payment method' is selected by default
        EXPECTED: *   "From" date picker is populated with one month back from today's date by default
        EXPECTED: *   "To" date picker with user's current date selected by default
        EXPECTED: *   A green 'GO' button is present
        EXPECTED: *   The list of all Deposit and Withdrawals is displayed below
        """
        pass

    def test_002_tap_deposit_button_and_tap_go(self):
        """
        DESCRIPTION: Tap 'Deposit' button and tap 'GO'
        EXPECTED: *  All deposits within selected time frame are displayed
        EXPECTED: *  If there is no actions to display then a message is displayed instead: 'No transactions to display'
        EXPECTED: *  'All' button gets highlighted with this action
        """
        pass

    def test_003_verify_list_format_for_deposits(self):
        """
        DESCRIPTION: Verify list format for 'Deposits'
        EXPECTED: Each tab should contain:
        EXPECTED: * Green checkbox image - reference of a correct deposit
        EXPECTED: * In the same line: 'Deposit' text and the +'value' deposited
        EXPECTED: * In the line below: 'ID' number and 'Credited' text
        """
        pass

    def test_004_tap_withdraw_button_and_tap_go(self):
        """
        DESCRIPTION: Tap 'Withdraw' button and tap 'GO'
        EXPECTED: *  All withdrawals within selected time frame are displayed
        EXPECTED: *  If there is no actions to display then a message is displayed instead: 'No transactions to display'
        EXPECTED: *  'All' button gets highlighted with this action
        """
        pass

    def test_005_verify_list_format_for_withdrawals(self):
        """
        DESCRIPTION: Verify list format for 'Withdrawals'
        EXPECTED: Each tab for completed withdrawals should contain:
        EXPECTED: * Green checkbox image
        EXPECTED: * In the same line: 'Deposit' text and the +'value' deposited
        EXPECTED: * In the line below: 'ID' number and 'Completed' text
        EXPECTED: Each tab for 'pending withdrawals' should contain:
        EXPECTED: * Green checkbox image
        EXPECTED: * In the same line: 'Deposit' text and the +'value' deposited
        EXPECTED: * In the line below: 'ID' number and 'Pending' text
        EXPECTED: * A 'REVERSE' box
        """
        pass

    def test_006_tap_in_a_reverse_box_and_verify_page_layout(self):
        """
        DESCRIPTION: Tap in a 'REVERSE' box and verify page layout
        EXPECTED: * Reserve Withdrawals page is opened
        EXPECTED: * A checkable box is displayed and ticked by default, 'All Pending Withdrawals' text and at the right side of tab the account currency and the sum of all pending withdrawals is shown
        EXPECTED: * A list of each pending withdawal is displayed, verify:
        EXPECTED: - A checkable box
        EXPECTED: - Payment method image and the last 4 digits of card
        EXPECTED: - The ID of the withdrawal and the date
        EXPECTED: - At the right side, the 'Amount' of the withdrawal
        EXPECTED: * 'Reverse' button with value of requested withdrawal(s)
        EXPECTED: * 'Deposit' button
        EXPECTED: ![](index.php?/attachments/get/35733)
        """
        pass
