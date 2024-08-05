import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C58215580_Banach_Verify_settle_results_of_Build_Your_Bet_combination_bet(Common):
    """
    TR_ID: C58215580
    NAME: Banach. Verify settle results of Build Your Bet combination bet
    DESCRIPTION: Test case verifies Build Your Bet/Bet Builder bet on 'Settled bets' tab of Bet History
    PRECONDITIONS: * Environment has Banach mapped football events with Bet Placement available
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has at least 4 BYB combination bets placed in Open Bets (different selections are used for each bet)
    PRECONDITIONS: To place BYB bet:
    PRECONDITIONS: * Find mapped BYB event
    PRECONDITIONS: * Navigate to 'Build Your Bet'/'Bet Builder' tab on EDP
    PRECONDITIONS: * Add at least two selection which could combine
    PRECONDITIONS: * Place a bet
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_of_bet_history(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab of Bet History
        EXPECTED: BYB/BB bets are present among the others
        """
        pass

    def test_002_in_ti_settle_banach_market_selections_of_the_bet_to_get1_bet_with_all_selections_won2_bet_with_all_selections_won_and_one_void3_bet_with_all_selections_lost_and_one_void4_bet_with_all_selections_won_and_one_lost(self):
        """
        DESCRIPTION: In TI settle Banach market selections of the bet to get:
        DESCRIPTION: 1) Bet with all selections 'Won'
        DESCRIPTION: 2) Bet with all selections 'Won' and one 'Void'
        DESCRIPTION: 3) Bet with all selections 'Lost' and one 'Void'
        DESCRIPTION: 4) Bet with all selections 'Won' and one 'Lost'
        EXPECTED: Settled results are saved in TI
        """
        pass

    def test_003_refresh_the_open_bets_tab(self):
        """
        DESCRIPTION: Refresh the 'Open Bets' tab
        EXPECTED: Settled combination bets are not displayed on 'Open Bets'
        """
        pass

    def test_004_navigate_to_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab
        EXPECTED: * Banach combination bets are settled
        EXPECTED: * Settled bets have 'Build Your Bet' header for Coral or 'Bet Builder' header for Ladbrokes
        """
        pass

    def test_005_observe_status_of_settled_banach_bets(self):
        """
        DESCRIPTION: Observe status of settled Banach bets
        EXPECTED: 1) Bet with all selections 'Won' has result status **Won** and **green tick** sign near the selection
        EXPECTED: 2) Bet with all selections 'Won' and one 'Void' has result status **Void** and **Void** label near the selection.
        EXPECTED: 3) Bet with all selections 'Lost' and one 'Void' has result status **Lost** and **red cross** sign near the selection
        EXPECTED: 4) Bet with all selections 'Won' and one 'Lost' has result status **Lost** and **red cross** sign near the selection
        """
        pass
