import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17723915_Vanilla_Verify_Banking_right_menu_option(Common):
    """
    TR_ID: C17723915
    NAME: [Vanilla] Verify 'Banking' right menu option
    DESCRIPTION: This test case is to verify all option menus under Banking right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in, 'My Account' button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap 'My Account' button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_banking__balances_ladbrokesbankingcoral_menu_option(self):
        """
        DESCRIPTION: Click/tap 'Banking & Balances' (Ladbrokes)/'Banking'(Coral) menu option
        EXPECTED: 'Banking & Balances'/'Banking' menu is displayed with the following options:
        EXPECTED: - My Balance
        EXPECTED: - Deposit
        EXPECTED: - Transfer (Ladbrokes only)
        EXPECTED: - Withdraw
        EXPECTED: - Payment History (Ladbrokes only)
        """
        pass

    def test_004_clicktap_my_balance_option(self):
        """
        DESCRIPTION: Click/tap 'My Balance' option
        EXPECTED: 'My Balance' is displayed with the following information:
        EXPECTED: - Withdrawable - Online
        EXPECTED: - Restricted (Coral only)
        EXPECTED: - Available balance
        EXPECTED: - Total balance
        EXPECTED: At the bottom there is a 'Deposit' button and 'Available to use on' section
        """
        pass

    def test_005_navigate_back_and_clicktap_deposit_option(self):
        """
        DESCRIPTION: Navigate back and click/tap 'Deposit' option
        EXPECTED: User is taken to 'Deposit/payment methods' page
        """
        pass

    def test_006_navigate_back_and_clicktap_withdraw_option(self):
        """
        DESCRIPTION: Navigate back and click/tap 'Withdraw' option
        EXPECTED: User is taken to 'Withdraw' page
        """
        pass

    def test_007_ladbrokes_onlynavigate_back_and_clicktap_transfer_option(self):
        """
        DESCRIPTION: **Ladbrokes only:**
        DESCRIPTION: Navigate back and click/tap 'Transfer' option
        EXPECTED: User is taken to 'Transfer' page
        """
        pass

    def test_008_ladbrokes_onlynavigate_back_and_clicktap_payment_history_option(self):
        """
        DESCRIPTION: **Ladbrokes only:**
        DESCRIPTION: Navigate back and click/tap 'Payment History' option
        EXPECTED: User is taken to 'Payment History' page
        """
        pass
