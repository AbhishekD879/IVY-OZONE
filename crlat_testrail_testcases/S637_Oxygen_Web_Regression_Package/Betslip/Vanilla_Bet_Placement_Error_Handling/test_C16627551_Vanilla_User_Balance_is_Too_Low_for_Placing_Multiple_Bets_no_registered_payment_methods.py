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
class Test_C16627551_Vanilla_User_Balance_is_Too_Low_for_Placing_Multiple_Bets_no_registered_payment_methods(Common):
    """
    TR_ID: C16627551
    NAME: [Vanilla] User Balance is Too Low for Placing Multiple Bets  (no registered payment methods)
    DESCRIPTION: This test case verifies Error Handling When User Balance is Too Low for Placing Multiple Bets
    PRECONDITIONS: 1.  The user account is NOT sufficient to cover multiple stakes (no registered payment methods)
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

    def test_002_add_multiple_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add multiple selection to the Betslip
        EXPECTED: Betslip counter is increased with number of selections
        """
        pass

    def test_003_go_to_betslip_and_enter_multiples_stake_which_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Go to 'Betslip' and enter Multiples stake which won't exceed a max bet allowed
        EXPECTED: 'PLACE BET' button is changed to 'MAKE A DEPOSIT'
        """
        pass

    def test_004_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT'
        EXPECTED: User is redirected to 'Deposit' page
        """
        pass
