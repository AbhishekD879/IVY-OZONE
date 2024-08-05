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
class Test_C44870391_Verify_the_Bet_placement_Settlement_and_cash_out_for_available_selections_in_the_markets_Markets_Starman_Hotshot_BadBoys(Common):
    """
    TR_ID: C44870391
    NAME: "Verify the Bet placement & Settlement and cash out for available selections in the markets ( Markets: Starman/Hotshot/BadBoys"
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User navigates to football - #yourcall markets.
    """
    keep_browser_open = True

    def test_001_add_selection_to_bet_slip_from_starmanhotshotbadboys_markets(self):
        """
        DESCRIPTION: Add selection to bet slip from Starman/Hotshot/BadBoys markets
        EXPECTED: Selection should be added to bet slip
        """
        pass

    def test_002_enter_stake_and_click_on_place_button(self):
        """
        DESCRIPTION: Enter stake and click on place button
        EXPECTED: Bet should be placed.
        """
        pass

    def test_003_navigates_to_my_bets_area(self):
        """
        DESCRIPTION: Navigates to My Bets area
        EXPECTED: My bets area should be opened.
        """
        pass

    def test_004_click_on_cash_out_tab(self):
        """
        DESCRIPTION: Click on Cash out tab
        EXPECTED: Cash out tab should be opened.
        """
        pass

    def test_005_verify_cash_out_functionality_for_yourcall_markets(self):
        """
        DESCRIPTION: verify cash out functionality for #yourcall markets
        EXPECTED: cashout should be successful for #yourcall markets
        """
        pass

    def test_006_verify_settlebet_for_yourcall_markets(self):
        """
        DESCRIPTION: Verify settlebet for #yourcall markets
        EXPECTED: Bet should be displayed in settlebet tab(Win/lost/draw)
        """
        pass
