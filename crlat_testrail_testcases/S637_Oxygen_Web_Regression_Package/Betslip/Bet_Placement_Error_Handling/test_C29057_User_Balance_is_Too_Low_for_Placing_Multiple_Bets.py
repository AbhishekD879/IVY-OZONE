import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29057_User_Balance_is_Too_Low_for_Placing_Multiple_Bets(Common):
    """
    TR_ID: C29057
    NAME: User Balance is Too Low for Placing Multiple Bets
    DESCRIPTION: This test case verifies Error Handling When User Balance is Too Low for Placing Multiple Bets
    DESCRIPTION: AUTOTEST C2491007
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User's balance is not sufficient to cover any stake, no registered payment methods
    """
    keep_browser_open = True

    def test_001_add_few_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add few selections to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_enter_multiples_stake_which_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Enter Multiples stake which won't exceed a max bet allowed
        EXPECTED: 'Bet Now' (from OX 99 'Place Bet') button is enabled
        """
        pass

    def test_003_tap_on_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: Betslip is closed
        EXPECTED: User is navigated to 'Deposit' page, 'Add Credit/Debit Cards' tab for Coral brand
        EXPECTED: User is navigated to Account One system for Ladbrokes brand
        """
        pass
