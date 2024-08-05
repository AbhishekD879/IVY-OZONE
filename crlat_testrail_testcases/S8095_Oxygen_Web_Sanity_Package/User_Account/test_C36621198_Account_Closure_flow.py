import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C36621198_Account_Closure_flow(Common):
    """
    TR_ID: C36621198
    NAME: Account Closure flow
    DESCRIPTION: This test case verifies Account Closure functionality
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to My Account menu -> select 'Gambling control' item
    PRECONDITIONS: * Select 'Account Closure & Reopening' section and click 'Choose'
    """
    keep_browser_open = True

    def test_001_select_i_want_to_close_my_account_or_section_of_itclick_continue(self):
        """
        DESCRIPTION: Select 'I want to close my Account or section of it'
        DESCRIPTION: Click 'Continue'
        EXPECTED: ![](index.php?/attachments/get/111269050)
        """
        pass

    def test_002_click_close_all(self):
        """
        DESCRIPTION: Click 'Close All'
        EXPECTED: * Option is selected and displayed within 'Please select a closure reason below' drop-down
        EXPECTED: * 'CONTINUE' button becomes enabled
        """
        pass

    def test_003_select_duration_indefinite_closureselect_reasonclick_continue(self):
        """
        DESCRIPTION: Select duration: indefinite closure
        DESCRIPTION: Select reason
        DESCRIPTION: Click 'Continue'
        EXPECTED: confirmation page is opened
        EXPECTED: ![](index.php?/attachments/get/111269051)
        """
        pass

    def test_004_clicktap_close_my_account(self):
        """
        DESCRIPTION: Click/tap 'Close my account'
        EXPECTED: Account is closed
        """
        pass

    def test_005_log_in_with_closed_account_and_try_to_make_deposit_place_a_bet_via_quick_betbetslipjackpot_and_so_on(self):
        """
        DESCRIPTION: Log in with closed account and try to make
        DESCRIPTION: * deposit
        DESCRIPTION: * place a bet (via Quick Bet/Betslip/Jackpot and so on)
        EXPECTED: * User is not able to deposit
        EXPECTED: * User is not able to place any bet
        """
        pass
