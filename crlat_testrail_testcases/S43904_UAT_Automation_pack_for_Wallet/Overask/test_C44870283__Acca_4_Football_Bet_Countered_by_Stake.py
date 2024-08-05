import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870283__Acca_4_Football_Bet_Countered_by_Stake(Common):
    """
    TR_ID: C44870283
    NAME: - Acca 4 Football Bet Countered by Stake
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_4_fold_oa_acca_bet(self):
        """
        DESCRIPTION: Place a 4-fold OA ACCA bet
        EXPECTED: The bet should have gone to the OA flow
        """
        pass

    def test_002_in_traders_interface_change_the_stake_of_the_bet_and_click_on_submit(self):
        """
        DESCRIPTION: In Trader's Interface, change the stake of the bet and click on Submit
        EXPECTED: The counter offer should show the bet with the new stake and it should be highlighted in yellow
        """
        pass

    def test_003_check_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the Potential Returns are correct
        EXPECTED: The Potential Returns should be correct
        """
        pass

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: You should see the bet receipt and it should show the new stake and the correct potential returns
        """
        pass

    def test_005_check_my_bets_open_bets_to_see_that_the_bet_has_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Check My Bets->Open Bets to see that the bet has the correct stake and Potential Returns
        EXPECTED: The bet should show the correct new stake and Potential Returns
        """
        pass
