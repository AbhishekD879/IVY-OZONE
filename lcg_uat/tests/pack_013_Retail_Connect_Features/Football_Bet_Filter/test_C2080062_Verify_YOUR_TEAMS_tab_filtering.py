from time import sleep

import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.tst2  # football filter has endpoints just for prod
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.bet_filter
@pytest.mark.football_bet_filter
@pytest.mark.retail
@pytest.mark.connect
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C2080062_Verify_YOUR_TEAMS_tab_filtering(BaseFootballBetFilter):
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
    filter_sections = None

    def test_001_load_football_filter_page(self):
        """
        DESCRIPTION: Load Football filter page
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('footballFilter'):
            raise CmsClientException('"Football Bet Filter" is disabled')
        self.__class__.coupon_name = self.open_bet_filter_via_coupon()
        bet_filter = self.site.football_bet_filter
        result = bet_filter.tab_menu.open_tab(vec.retail.YOUR_TEAMS_TAB)
        self.assertTrue(result, msg=f'"{vec.retail.YOUR_TEAMS_TAB}" tab is not active')

    def test_002_verify_filters_default_value(self):
        """
        DESCRIPTION: Verify filters default value
        EXPECTED: * None of the filters is selected
        """
        self.__class__.filter_sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(self.filter_sections, msg='Can not find any sections')

        for section_name, section in self.filter_sections.items():
            section_filters = section.items_as_ordered_dict
            self.assertTrue(section_filters, msg=f'There are no any filters under "{section_name}" section')
            for filter_name, filter_ in section_filters.items():
                self.assertFalse(filter_.is_selected(expected_result=False), msg=f'"{filter_name}" filter is selected')

    def test_003_verify_filtering_by_playing_at_home_away_check_off_home_tap_find_bets_check_off_away_tap_find_bets(self):
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
        self.assertIn(vec.bet_finder.FB_BET_FILTER_PLAYING_AT_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_PLAYING_AT_TEXT}" filter section is not shown')
        playing_at_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_PLAYING_AT_TEXT)
        playing_at_filters = playing_at_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_HOME, playing_at_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_HOME}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_PLAYING_AT_TEXT}" section')
        home_filter = playing_at_filters.get(vec.bet_finder.FB_BET_FILTER_HOME)
        home_filter.click()
        sleep(2)
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_HOME.lower()])))
        home_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_AWAY, playing_at_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_AWAY}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_PLAYING_AT_TEXT}" section')
        self.__class__.away_filter = playing_at_filters.get(vec.bet_finder.FB_BET_FILTER_AWAY)
        self.away_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_AWAY.lower()])))

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
        self.away_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT}" filter section is not shown')
        last_game_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT)
        last_game_filters = last_game_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_WIN, last_game_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_WIN}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT}" section')
        win_filter = last_game_filters.get(vec.bet_finder.FB_BET_FILTER_WIN)
        win_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, last_game=[vec.bet_finder.FB_BET_FILTER_WIN.lower()])))
        win_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_DRAW, last_game_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_DRAW}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT}" section')
        draw_filter = last_game_filters.get(vec.bet_finder.FB_BET_FILTER_DRAW)
        draw_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, last_game=[vec.bet_finder.FB_BET_FILTER_DRAW.lower()])))
        draw_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_LOSE, last_game_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_LOSE}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT}" section')
        self.__class__.lose_filter = last_game_filters.get(vec.bet_finder.FB_BET_FILTER_LOSE)
        self.lose_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, last_game=[vec.bet_finder.FB_BET_FILTER_LOSE.lower()])))

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
        self.lose_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT}" filter section is not shown')
        last_six_games_points_total_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT)
        last_six_games_points_total_filters = last_six_games_points_total_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_ZERO_SIX_POINTS, last_six_games_points_total_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_ZERO_SIX_POINTS}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT}" section')
        zero_six_points_filter = last_six_games_points_total_filters.get(vec.bet_finder.FB_BET_FILTER_ZERO_SIX_POINTS)
        zero_six_points_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, last_6_games=[vec.bet_finder.FB_BET_FILTER_ZERO_SIX_POINTS.lower()])))
        zero_six_points_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_SEVEN_TWELVE_POINTS, last_six_games_points_total_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_SEVEN_TWELVE_POINTS}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT}" section')
        seven_twelve_points_filter = last_six_games_points_total_filters.get(vec.bet_finder.FB_BET_FILTER_SEVEN_TWELVE_POINTS)
        seven_twelve_points_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, last_6_games=[vec.bet_finder.FB_BET_FILTER_SEVEN_TWELVE_POINTS.lower()])))
        seven_twelve_points_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_THIRTEEN_EIGHTEEN_POINTS, last_six_games_points_total_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_THIRTEEN_EIGHTEEN_POINTS}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT}" section')
        self.__class__.thirteen_eighteen_points_filter = last_six_games_points_total_filters.get(
            vec.bet_finder.FB_BET_FILTER_THIRTEEN_EIGHTEEN_POINTS)
        self.thirteen_eighteen_points_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, last_6_games=[vec.bet_finder.FB_BET_FILTER_THIRTEEN_EIGHTEEN_POINTS.lower()])))

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
        self.thirteen_eighteen_points_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT}" filter section is not shown')
        key_tends_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT)
        key_tends_filters = key_tends_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_HIGH_SCORING, key_tends_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_HIGH_SCORING}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT}" section')
        high_scoring_filter = key_tends_filters.get(vec.bet_finder.FB_BET_FILTER_HIGH_SCORING)
        high_scoring_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_HIGH_SCORING.lower()])))
        high_scoring_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_MEAN_DEFENCE, key_tends_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_MEAN_DEFENCE}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT}" section')
        mean_defence_filter = key_tends_filters.get(vec.bet_finder.FB_BET_FILTER_MEAN_DEFENCE)
        mean_defence_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_MEAN_DEFENCE.lower()])))
        mean_defence_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME, key_tends_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT}" section')
        self.__class__.clean_sheet_last_game_filter = key_tends_filters.get(vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME)
        self.clean_sheet_last_game_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME.lower()])))

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
        self.clean_sheet_last_game_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_LEAGUE_POSITIONS_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_LEAGUE_POSITIONS_TEXT}" filter section is not shown')
        league_positions_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_LEAGUE_POSITIONS_TEXT)
        league_positions_filters = league_positions_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_TOP_HALF, league_positions_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_TOP_HALF}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LEAGUE_POSITIONS_TEXT}" section')
        top_half_filter = league_positions_filters.get(vec.bet_finder.FB_BET_FILTER_TOP_HALF)
        top_half_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_TOP_HALF.lower()])))
        top_half_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_BOTTOM_HALF, league_positions_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_BOTTOM_HALF}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LEAGUE_POSITIONS_TEXT}" section')
        bottom_half_filter = league_positions_filters.get(vec.bet_finder.FB_BET_FILTER_BOTTOM_HALF)
        bottom_half_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_BOTTOM_HALF.lower()])))
        bottom_half_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_ABOVE_OPPOSITION, league_positions_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_ABOVE_OPPOSITION}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LEAGUE_POSITIONS_TEXT}" section')
        self.__class__.above_opposition_filter = league_positions_filters.get(vec.bet_finder.FB_BET_FILTER_ABOVE_OPPOSITION)
        self.above_opposition_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_ABOVE_OPPOSITION.lower()])))

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
        self.above_opposition_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_ODDS_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_ODDS_TEXT}" filter section is not shown')
        odds_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_ODDS_TEXT)
        odds_filters = odds_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_FAVOURITE, odds_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_FAVOURITE}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_ODDS_TEXT}" section')
        favorite_filter = odds_filters.get(vec.bet_finder.FB_BET_FILTER_FAVOURITE)
        favorite_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_FAVOURITE.lower()])))
        favorite_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OUTSIDER, odds_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OUTSIDER}" filter is not shown under "{vec.bet_finder.FB_BET_FILTER_ODDS_TEXT}" section')
        self.__class__.outsider_filter = odds_filters.get(vec.bet_finder.FB_BET_FILTER_OUTSIDER)
        self.outsider_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name, filters=[vec.bet_finder.FB_BET_FILTER_OUTSIDER.lower()])))

    def test_009_select_a_couple_of_different_filters(self):
        """
        DESCRIPTION: Select a couple of different filters
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        self.outsider_filter.click()
        self.away_filter.click()
        self.lose_filter.click()
        self.above_opposition_filter.click()
        self.__class__.expected_selections = self.get_selections(coupon_name=self.coupon_name,
                                                                 filters=[vec.bet_finder.FB_BET_FILTER_AWAY.lower(),
                                                                          vec.bet_finder.FB_BET_FILTER_ABOVE_OPPOSITION.lower()],
                                                                 last_game=[vec.bet_finder.FB_BET_FILTER_LOSE.lower()])
        self.verify_number_of_bets(expected_number_of_bets=len(self.expected_selections))

    def test_010_click_find_bets_button(self):
        """
        DESCRIPTION: Click Find Bets button
        EXPECTED: Football Filter Results page is opened.
        EXPECTED: Verify that:
        EXPECTED: - Results number is correct
        EXPECTED: - List of selections is correct
        """
        if self.site.football_bet_filter.find_bets_button.is_enabled():
            self.site.football_bet_filter.find_bets_button.click()
            bet_filter_results_page = self.site.football_bet_filter_results_page
            self.assertEqual(bet_filter_results_page.number_of_results, len(self.expected_selections),
                             msg=f'Results number "{bet_filter_results_page.number_of_results}" is not the same '
                                 f'as expected "{len(self.expected_selections)}"')
            expected_selection_names = [selection['selectionName'] for selection in self.expected_selections]
            bet_filter_results = [result.name.split(' @')[0] for result in bet_filter_results_page.items]
            self.assertListEqual(sorted(bet_filter_results), sorted(expected_selection_names),
                                 msg=f'List of selections: \n"{bet_filter_results}" \nis not the same as '
                                     f'expected \n"{expected_selection_names}"')
        else:
            self._logger.info('There is no bets that fits selected filter')
