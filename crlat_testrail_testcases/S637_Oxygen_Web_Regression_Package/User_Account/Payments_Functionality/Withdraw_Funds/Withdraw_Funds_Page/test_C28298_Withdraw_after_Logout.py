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
class Test_C28298_Withdraw_after_Logout(Common):
    """
    TR_ID: C28298
    NAME: Withdraw after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by the server automatically when his/her session is over on the server.
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Invictus in one browser tab and open 'Withdraw Funds' page
    PRECONDITIONS: *   Login to Invictus in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_select_debitcredit_card_and_enter_amount(self):
        """
        DESCRIPTION: Select Debit/Credit card and enter amount
        EXPECTED: 
        """
        pass

    def test_002_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_003_verify_withdraw_funds_page(self):
        """
        DESCRIPTION: Verify 'Withdraw Funds' page
        EXPECTED: * Popup message about logging out appears.
        EXPECTED: * User is logged out from the application automatically without performing any action
        EXPECTED: * User is not able to see **Withdraw Funds** page and to perform Withdraw operations
        EXPECTED: * User is redirected to the Homepage
        """
        pass

    def test_004_select_paypal_method_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Select PayPal method and repeat steps 2-3
        EXPECTED: 
        """
        pass

    def test_005_select_neteller_account_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Select NETELLER account and repeat steps 2-3
        EXPECTED: 
        """
        pass
