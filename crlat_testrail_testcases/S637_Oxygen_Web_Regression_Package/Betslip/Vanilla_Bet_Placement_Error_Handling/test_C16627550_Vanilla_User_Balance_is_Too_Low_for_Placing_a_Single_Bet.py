import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C16627550_Vanilla_User_Balance_is_Too_Low_for_Placing_a_Single_Bet(Common):
    """
    TR_ID: C16627550
    NAME: [Vanilla] User Balance is Too Low for Placing a Single Bet
    DESCRIPTION: This test case verifies bet slip error handling in case when user balance is too low.
    PRECONDITIONS: 1.  The user account is NOT sufficient to cover any stake
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> sport it is possible to place a bet from:
    PRECONDITIONS: - 'Next races' module
    PRECONDITIONS: - event landing page
    PRECONDITIONS: NOTE: in order to check Max Allowed Bet enter extremely large stake value in 'Stake' field and tap 'Bet Now' button to see what is Max allowed bet for selection.
    """
    keep_browser_open = True

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_003_go_to_betslip_and_enter_a_stake_which_will_not_exceed_users_balance_and_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Go to 'Betslip' and enter a stake which will not exceed user's balance and won't exceed a max bet allowed
        EXPECTED: 'PLACE BET' button is available
        """
        pass

    def test_004_enter_a_stake_which_will_exceed_users_balance_but_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Enter a stake which will exceed user's balance but won't exceed a max bet allowed
        EXPECTED: * 'PLACE BET' button is not available
        EXPECTED: * 'MAKE A DEPOSIT' button is available
        """
        pass

    def test_005_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT'
        EXPECTED: 'Quick Deposit' module is displayed in Betslip
        """
        pass
