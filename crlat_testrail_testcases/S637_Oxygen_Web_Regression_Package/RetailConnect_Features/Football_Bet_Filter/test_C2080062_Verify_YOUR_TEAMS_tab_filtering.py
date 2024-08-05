import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2080062_Verify_YOUR_TEAMS_tab_filtering(Common):
    """
    TR_ID: C2080062
    NAME: Verify 'YOUR TEAMS' tab filtering
    DESCRIPTION: AUTOTEST [C9859220]
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Select 'Connect' from header ribbon
    PRECONDITIONS: 3. Select 'Football Bet Filter' item
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
    """
    keep_browser_open = True

    def test_001_load_football_filter_page(self):
        """
        DESCRIPTION: Load Football filter page
        EXPECTED: 
        """
        pass

    def test_002_verify_filters_default_value(self):
        """
        DESCRIPTION: Verify filters default value
        EXPECTED: * None of the filters is selected
        """
        pass

    def test_003_verify_filtering_by_playing_at_home_awaycheck_off_home__tap_find_betscheck_off_away__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by PLAYING AT
        DESCRIPTION: * HOME
        DESCRIPTION: * AWAY
        DESCRIPTION: Check off 'HOME' > tap 'Find Bets'.
        DESCRIPTION: Check off 'AWAY' > tap 'Find Bets'
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * {"type": "home"}
        EXPECTED: * {"type": "away"}
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_004_verify_filtering_by_last_game_win_draw_lose(self):
        """
        DESCRIPTION: Verify filtering by LAST GAME
        DESCRIPTION: * WIN
        DESCRIPTION: * DRAW
        DESCRIPTION: * LOSE
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * {"lastGame": "win"}
        EXPECTED: * {"lastGame": "draw"}
        EXPECTED: * {"lastGame": "lose"}
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_005_verify_filtering_by_last_6_games_point_total_0_6_points_7_12_points_13_18_points(self):
        """
        DESCRIPTION: Verify filtering by LAST 6 GAMES POINT TOTAL
        DESCRIPTION: * 0-6 POINTS
        DESCRIPTION: * 7-12 POINTS
        DESCRIPTION: * 13-18 POINTS
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * {"last6Games": "0"} [0, 1, 2, 3, 4, 5, 6]
        EXPECTED: * {"last6Games": "7"} [7...12]
        EXPECTED: * {"last6Games": "13"} [13...18]
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_006_verify_filtering_by_key_trends_high_scoring_mean_defence_clean_sheet_last_game(self):
        """
        DESCRIPTION: Verify filtering by KEY TRENDS
        DESCRIPTION: * HIGH SCORING
        DESCRIPTION: * MEAN DEFENCE
        DESCRIPTION: * CLEAN SHEET LAST GAME
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * {"keyTrendsScoring": "highScoring"}
        EXPECTED: * {"keyTrendsDefence": "meanDefence"}
        EXPECTED: * {"keyTrendsLastGame": "cleanSheet"}
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_007_verify_filtering_by_league_positions_top_half_bottom_half_above_opposition(self):
        """
        DESCRIPTION: Verify filtering by LEAGUE POSITIONS
        DESCRIPTION: * TOP HALF
        DESCRIPTION: * BOTTOM HALF
        DESCRIPTION: * ABOVE OPPOSITION
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * compare
        EXPECTED: "leaguePosition": "No" vs "teamsInLeague": "No"
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_008_verify_filtering_by_odds_favourite_outsider(self):
        """
        DESCRIPTION: Verify filtering by ODDS
        DESCRIPTION: * FAVOURITE
        DESCRIPTION: * OUTSIDER
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * compare the odds for the teams in rEsults page with their opposition in match
        EXPECTED: "odds": "11/8" vs "odds": "2/1"
        EXPECTED: (selection with smaller 'odds' is FAVOURITE; selection with bigger 'odds' is OUTSIDER)
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_009_select_a_couple_of_different_filters(self):
        """
        DESCRIPTION: Select a couple of different filters
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_010_click_find_bets_button(self):
        """
        DESCRIPTION: Click Find Bets button
        EXPECTED: Football Filter Results page is opened.
        EXPECTED: Verify that:
        EXPECTED: - Results number is correct
        EXPECTED: - List of selections is correct
        """
        pass
