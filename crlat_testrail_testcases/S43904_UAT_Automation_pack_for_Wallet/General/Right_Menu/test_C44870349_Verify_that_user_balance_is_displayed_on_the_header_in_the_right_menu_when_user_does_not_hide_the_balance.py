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
class Test_C44870349_Verify_that_user_balance_is_displayed_on_the_header_in_the_right_menu_when_user_does_not_hide_the_balance(Common):
    """
    TR_ID: C44870349
    NAME: Verify that user balance is displayed on the header in the right menu when user does not hide the balance.
    DESCRIPTION: Not applicable for Desktop
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_click_on_betslip__balance__xxxxx_(self):
        """
        DESCRIPTION: Click on Betslip > Balance (£ XXX.XX) >
        EXPECTED: Hide Balance / Deposit
        EXPECTED: options are available
        """
        pass

    def test_002_click_on_hide_balance_and_verify(self):
        """
        DESCRIPTION: Click on Hide balance and verify.
        EXPECTED: The user's account balance is not displayed in the header area. Thus, the user's balance is hidden displayed as BALANCE
        """
        pass

    def test_003_close_the_betslip_and_againclick_on_betslip__balance__xxxxx(self):
        """
        DESCRIPTION: Close the 'Betslip' and again
        DESCRIPTION: Click on Betslip > Balance (£ XXX.XX)
        EXPECTED: Show Balance / Deposit
        EXPECTED: options are available
        """
        pass

    def test_004_click_on_show_balance_and_verify(self):
        """
        DESCRIPTION: Click on Show balance and verify.
        EXPECTED: The user's account balance is displayed in the header area along with the corresponding currency symbol.
        """
        pass
