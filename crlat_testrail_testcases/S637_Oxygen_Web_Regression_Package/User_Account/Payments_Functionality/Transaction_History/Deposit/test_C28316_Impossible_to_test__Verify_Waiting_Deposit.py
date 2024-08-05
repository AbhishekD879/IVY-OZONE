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
class Test_C28316_Impossible_to_test__Verify_Waiting_Deposit(Common):
    """
    TR_ID: C28316
    NAME: Impossible to test - Verify Waiting Deposit
    DESCRIPTION: This test case verifies Waiting Withdrawal.
    DESCRIPTION: SHOULD BE EDITED OR DELETED.
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has at least one registered card
    PRECONDITIONS: *   Balance of account is enough for withdraw from
    PRECONDITIONS: Note: UAT team support is needed.
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
        EXPECTED: *   Drop-down list with existing reqistered cards is shown
        EXPECTED: *   Drop-down is expanded by default
        """
        pass

    def test_003_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_004_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Successfull message: **"Your withdrawal request has been successful. Reference: #XXXXXXX"** is shown
        EXPECTED: *   User stays on the 'Withdraw Funds' page (refreshed with clear form)
        """
        pass

    def test_005_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is decremented on amount set on step №4
        """
        pass
