import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2069265_Verify_displaying_when_Football_selection_is_winning_lousing(Common):
    """
    TR_ID: C2069265
    NAME: Verify displaying when Football selection is winning/ lousing
    DESCRIPTION: This test case verifies Indication That Bet Is Winning/Losing (it's developed for 5 markets: Match Result; Both Teams to Score; Goal in Both Halves; to Win and Both Teams to Score (to Win Not to Nil);
    PRECONDITIONS: Request coupons codes placed on all outcomes of following markets:
    PRECONDITIONS: Match Result
    PRECONDITIONS: Both Teams to Score
    PRECONDITIONS: Goal in Both Halves
    PRECONDITIONS: to Win and Both Teams to Score (to Win Not to Nil)
    PRECONDITIONS: to Win to Nil
    PRECONDITIONS: **Verify displaying when Football selection is winning/ lousing simultaneously on both 'Shop Bet Tracker' and  'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_team_a_selection_of_market_match_result(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'Team A'** selection of market **'Match Result'**
        EXPECTED: 
        """
        pass

    def test_003__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * If score of team  **'Team A'** is higher then **'Team B'** -> Ball icon is green
        EXPECTED: * If score of team  **'Team B'** is higher then **'Team A'** -> Ball icon is red
        EXPECTED: * If score of team  **'Team B'** is equal to **'Team A'** -> Ball icon is red
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass

    def test_004_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_draw_selection_of_market_match_result(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'Draw'** selection of market **'Match Result'**
        EXPECTED: 
        """
        pass

    def test_005__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * If score of team  **'Team A'** is equal to **'Team B'** -> Ball icon is green
        EXPECTED: * In all other cases ball icon is red
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass

    def test_006_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_yes_selection_of_market_both_teams_to_score(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'YES'** selection of market **'Both Teams to Score'**
        EXPECTED: 
        """
        pass

    def test_007__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * If score of team  **'Team A'** is equal to '0' and  **'Team B'** is '0' -> Ball icon is red
        EXPECTED: * If score of one of the team is equal to '0' -> Ball icon is red
        EXPECTED: * If Score of **'Team A'** and **'Team B'** is higher that 0 ->
        EXPECTED: Ball icon is green
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass

    def test_008_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_no_selection_of_market_both_teams_to_score(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'NO'** selection of market **'Both Teams to Score'**
        EXPECTED: * If both teams score is equal to '0' -> ball icon is green
        EXPECTED: * If one team score is equal to '0' -> ball icon is green
        EXPECTED: * If both teams score is higher than '0' -> ball icon is red
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass

    def test_009_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_yes_selection_of_market_goal_in_both_halves(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'YES'** selection of market **'Goal in Both Halves'**
        EXPECTED: 
        """
        pass

    def test_010__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * During first half ball icon is red
        EXPECTED: * If first half is finished with score 0:0 -> ball icons remains red
        EXPECTED: * If first half has some score but second half is finished with 0:0 -> ball icons is red
        EXPECTED: * If first half and second half have some score  -> ball icons is green
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass

    def test_011_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_no_selection_of_market_goal_in_both_halves(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'NO'** selection of market **'Goal in Both Halves'**
        EXPECTED: 
        """
        pass

    def test_012__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * During first half ball icon is green
        EXPECTED: * If first half is finished with score 0:0 -> ball icons remains green
        EXPECTED: * If first half has has some score but second half is finished with 0:0 -> ball icons remains green
        EXPECTED: * If first half and second half have has some score  -> ball icons is red
        """
        pass

    def test_013_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_team_a_selection_of_market_to_win_and_both_teams_to_score_to_win_not_to_nil(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'Team A'** selection of market **'to Win and Both Teams to Score (to Win Not to Nil)'**
        EXPECTED: 
        """
        pass

    def test_014__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * If score is added for both teams and score of **'Team A'** is greater of score of  **'Team B'** - ball icon is green
        EXPECTED: * * If score of **'Team A'** is greater of score of  **'Team B'** but score of **'Team B'** is '0' - ball icon is red
        EXPECTED: * If score of **'Team B'** if greater of equal to score of **'Team 'A** - ball icon is red
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass

    def test_015_submit_valid_cash_out_code_which_contains_event_team_a_vs_team_b_with_bet_on_team_a_selection_of_market_to_win_to_nil(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains event ('Team A' vs 'Team B') with bet on **'Team A'** selection of market **'to Win to Nil'**
        EXPECTED: 
        """
        pass

    def test_016__trigger_score_changing_verify_result_on_both_shop_bet_tracker_page_and__my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger score changing
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and  'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: * If score is added for both teams and score of **'Team A'** is greater of score of  **'Team B'** - ball icon is red
        EXPECTED: * * If score of **'Team A'** is greater of score of  **'Team B'** and score of **'Team B'** is '0' - ball icon is green
        EXPECTED: * If score of **'Team B'** if greater of equal to score of **'Team 'A** - ball icon is red
        EXPECTED: * After match is finished icon color proceeds showing correct winning/ lousing status
        """
        pass
