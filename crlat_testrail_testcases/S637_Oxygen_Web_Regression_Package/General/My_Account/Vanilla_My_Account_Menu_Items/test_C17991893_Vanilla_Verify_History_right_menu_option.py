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
class Test_C17991893_Vanilla_Verify_History_right_menu_option(Common):
    """
    TR_ID: C17991893
    NAME: [Vanilla] Verify History right menu option
    DESCRIPTION: This test case is to verify all option menus under History right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_history_menu_option(self):
        """
        DESCRIPTION: Click/tap HISTORY menu option
        EXPECTED: History menu is displayed with the following options:
        EXPECTED: - Transaction History
        EXPECTED: - Payment History
        EXPECTED: - Betting History
        """
        pass

    def test_004_clicktap_transaction_history_option(self):
        """
        DESCRIPTION: Click/tap Transaction History option
        EXPECTED: My Transactions page is displayed
        """
        pass

    def test_005_reopen_right_menu__history_and_clicktap_payment_history_option(self):
        """
        DESCRIPTION: Reopen right menu-> History and click/tap Payment History option
        EXPECTED: User is taken to Payment History page
        """
        pass

    def test_006_reopen_right_menu__history_and_clicktap_betting_history_option(self):
        """
        DESCRIPTION: Reopen right menu-> History and click/tap Betting History option
        EXPECTED: User is taken to My Bets -> Settled bets tab.
        EXPECTED: Sports section is selected by default
        """
        pass
