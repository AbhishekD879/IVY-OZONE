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
class Test_C2080063_Verify_THE_OPPOSITION_tab_filtering(Common):
    """
    TR_ID: C2080063
    NAME: Verify 'THE OPPOSITION' tab filtering
    DESCRIPTION: AUTOTEST [C9864907]
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Select 'Connect' from header ribbon
    PRECONDITIONS: 3. Select 'Football Bet Filter' item
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
    """
    keep_browser_open = True

    def test_001_load_football_filter_page_switch_to_the_opposition_tab(self):
        """
        DESCRIPTION: Load Football filter page. Switch to 'THE OPPOSITION' tab
        EXPECTED: * Non of the filters is selected by default
        """
        pass

    def test_002_verify_filtering_by_last_game_win_draw_lose_check_off_win__tap_find_bets_check_off_draw__tap_find_bets_check_off_lose__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by LAST GAME
        DESCRIPTION: * WIN
        DESCRIPTION: * DRAW
        DESCRIPTION: * LOSE
        DESCRIPTION: * Check off 'WIN' > tap 'Find Bets'.
        DESCRIPTION: * Check off 'DRAW' > tap 'Find Bets'
        DESCRIPTION: * Check off 'LOSE' > tap 'Find Bets'
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: (COMPARE FOR THE OPPOSITION at Results page)
        EXPECTED: * {"lastGame": "win"}
        EXPECTED: * {"lastGame": "draw"}
        EXPECTED: * {"lastGame": "lose"}
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_003_verify_filtering_by_last_6_games_point_total_0_6_points_7_12_points_13_18_points_check_off_0_6_points__tap_find_bets_check_off_7_12_points__tap_find_bets_check_off_13_18_points__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by LAST 6 GAMES POINT TOTAL
        DESCRIPTION: * 0-6 POINTS
        DESCRIPTION: * 7-12 POINTS
        DESCRIPTION: * 13-18 POINTS
        DESCRIPTION: * Check off '0-6 POINTS' > tap 'Find Bets'.
        DESCRIPTION: * Check off '7-12 POINTS' > tap 'Find Bets'
        DESCRIPTION: * Check off '13-18 POINTS' > tap 'Find Bets'
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: (COMPARE FOR THE OPPOSITION at Results page)
        EXPECTED: * {"last6Games": "0"} [0, 1, 2, 3, 4, 5, 6]
        EXPECTED: * {"last6Games": "7"} [7...12]
        EXPECTED: * {"last6Games": "13"} [13...18]
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_004_verify_filtering_by_key_trends_high_scoring_leaky_defence_conceded_2plus_last_game_check_off_high_scoring__tap_find_bets_check_off_leaky_defence__tap_find_bets_check_off_conceded_2plus_last_game__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by KEY TRENDS
        DESCRIPTION: * HIGH SCORING
        DESCRIPTION: * LEAKY DEFENCE
        DESCRIPTION: * CONCEDED 2+ LAST GAME
        DESCRIPTION: * Check off 'HIGH SCORING' > tap 'Find Bets'.
        DESCRIPTION: * Check off 'LEAKY DEFENCE' > tap 'Find Bets'
        DESCRIPTION: * Check off 'CONCEDED 2+ LAST GAME' > tap 'Find Bets'
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: (COMPARE FOR THE OPPOSITION at Results page)
        EXPECTED: * {"keyTrendsScoring": "highScoring"}
        EXPECTED: * {"keyTrendsDefence": "weakDefence"}
        EXPECTED: * {"keyTrendsLastGame": "conceded2+"}
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_005_verify_filtering_by_league_positions_top_half_bottom_half_below_opposition_check_off_top_half__tap_find_bets_check_off_bottom_half__tap_find_bets_check_off_below_opposition__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by LEAGUE POSITIONS
        DESCRIPTION: * TOP HALF
        DESCRIPTION: * BOTTOM HALF
        DESCRIPTION: * BELOW OPPOSITION
        DESCRIPTION: * Check off 'TOP HALF' > tap 'Find Bets'.
        DESCRIPTION: * Check off 'BOTTOM HALF' > tap 'Find Bets'
        DESCRIPTION: * Check off 'BELOW OPPOSITION' > tap 'Find Bets'
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * compare THE OPPOSITE TEAM for
        EXPECTED: "leaguePosition": "No" vs "teamsInLeague": "No"
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_006_select_a_couple_of_different_filters(self):
        """
        DESCRIPTION: Select a couple of different filters
        EXPECTED: Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_007_click_find_bets_button(self):
        """
        DESCRIPTION: Click Find Bets button
        EXPECTED: Football Filter Results page is opened.
        EXPECTED: Verify that:
        EXPECTED: - Results number is correct
        EXPECTED: - List of selections is correct
        """
        pass
