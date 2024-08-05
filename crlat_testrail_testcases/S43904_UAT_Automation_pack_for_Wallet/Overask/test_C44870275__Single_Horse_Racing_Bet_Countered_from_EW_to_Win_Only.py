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
class Test_C44870275__Single_Horse_Racing_Bet_Countered_from_EW_to_Win_Only(Common):
    """
    TR_ID: C44870275
    NAME: - Single Horse Racing Bet Countered from EW to Win Only
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_an_overask_each_way_horse_race(self):
        """
        DESCRIPTION: Place an overask Each Way horse race
        EXPECTED: You should have placed a bet
        """
        pass

    def test_002_in_the_ti_change_the_type_of_the_bet_from_each_way_to_win_only(self):
        """
        DESCRIPTION: In the TI, change the type of the bet from Each Way to Win Only
        EXPECTED: You should have changed EW to Win Only
        """
        pass

    def test_003_check_that_the_counter_offer_shows_that1_your_stake_is_highlighted2_you_see_the_win_only_signposting3_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the counter offer shows that:
        DESCRIPTION: 1. Your stake is highlighted
        DESCRIPTION: 2. You see the Win Only signposting
        DESCRIPTION: 3. The potential returns are correct
        EXPECTED: You should see that
        EXPECTED: 1. The stake is highlighted
        EXPECTED: 2. The Win Only signposting
        EXPECTED: 3. The correct potential returns
        """
        pass

    def test_004_place_the_bet_and_check_that_the_bet_receipt_shows_the_correct_stake_and_potential_returns_and_does_not_show_any_each_way_terms_and_places_eg_12_1_2_3(self):
        """
        DESCRIPTION: Place the bet and check that the bet receipt shows the correct stake and potential returns AND does not show any Each Way terms and places e.g. 1/2, 1-2-3
        EXPECTED: The receipt should show the correct stake and potential returns and no Each Way terms should be seen
        """
        pass

    def test_005_check_that_bet_shows_the_correct_stake_and_potential_returns_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Check that bet shows the correct stake and potential returns in My Bets->Open Bets
        EXPECTED: The correct stake and potential returns should be shown for this bet in My Bets->Open Bets
        """
        pass
