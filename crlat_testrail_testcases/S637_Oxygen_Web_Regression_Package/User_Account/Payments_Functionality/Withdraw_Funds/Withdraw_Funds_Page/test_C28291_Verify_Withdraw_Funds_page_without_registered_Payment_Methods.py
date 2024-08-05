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
class Test_C28291_Verify_Withdraw_Funds_page_without_registered_Payment_Methods(Common):
    """
    TR_ID: C28291
    NAME: Verify Withdraw Funds page without registered Payment Methods
    DESCRIPTION: This test case verifies view of the Withdraw Funds page without registered Payment Methods.
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has NO registered Credit/Debit Cards
    PRECONDITIONS: *   User has NO registered PayPal account
    PRECONDITIONS: *   User has NO registered NETELLER account
    PRECONDITIONS: NOTE: in case server returns unexpected response: only error code (no “message”, “errorMessage”…)/empty response/ other data structure default error message should be displyed: "**There has been an error with your transaction. Please contact our Customer Services team.**"
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_menu_item(self):
        """
        DESCRIPTION: Tap 'Withdraw' menu item
        EXPECTED: 'Withdraw Funds' page is opened
        """
        pass

    def test_003_verify_withdraw_funds_page_view(self):
        """
        DESCRIPTION: Verify 'Withdraw Funds' page view
        EXPECTED: *   Text message **'Please set up a deposit method first.' **is shown
        EXPECTED: *   Button **'Deposit Now'** is shown below the message and is enabled
        """
        pass

    def test_004_tap_deposit_now_button(self):
        """
        DESCRIPTION: Tap **'Deposit Now'** button
        EXPECTED: *   **'Deposit'** page is opened
        EXPECTED: *   **'Add Debit/Credit Cards**' tab is selected
        """
        pass
