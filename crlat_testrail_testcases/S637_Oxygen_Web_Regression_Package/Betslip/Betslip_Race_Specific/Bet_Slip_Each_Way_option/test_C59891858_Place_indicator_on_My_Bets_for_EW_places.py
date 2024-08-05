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
class Test_C59891858_Place_indicator_on_My_Bets_for_EW_places(Common):
    """
    TR_ID: C59891858
    NAME: Place indicator on My Bets for EW places
    DESCRIPTION: Test case verifies place indicator on Settle Bets tab on single and multiple bets
    PRECONDITIONS: How to result market on TI https://confluence.egalacoral.com/pages/viewpage.action?pageId=96150627
    PRECONDITIONS: - User is logged in and has positive balance to place bet
    PRECONDITIONS: - User has placed few e/w bets on Horse/Greyhound Races
    """
    keep_browser_open = True

    def test_001_open_win_or_each_way_market_on_ti(self):
        """
        DESCRIPTION: Open 'Win or Each Way' market on TI
        EXPECTED: 
        """
        pass

    def test_002_set_results_to_have_different_outcomes_win_lose_void_place_in_result_column_and_places_place_column(self):
        """
        DESCRIPTION: Set results to have different outcomes ('win', 'lose', 'void', 'place' in 'Result' column) and places ('Place' column)
        EXPECTED: Results are set ('Yes' is displayed in 'Confirmed' and 'Settled' columns)
        """
        pass

    def test_003_open_my_bets___settled_bets_tab(self):
        """
        DESCRIPTION: Open 'My Bets' -> 'Settled bets' tab
        EXPECTED: 'Settled bets' tab is opened
        """
        pass

    def test_004_verify_position_is_displayed_for_resulted_bets(self):
        """
        DESCRIPTION: Verify position is displayed for resulted bets
        EXPECTED: Place indicator is shown
        EXPECTED: ![](index.php?/attachments/get/118934771)
        """
        pass
