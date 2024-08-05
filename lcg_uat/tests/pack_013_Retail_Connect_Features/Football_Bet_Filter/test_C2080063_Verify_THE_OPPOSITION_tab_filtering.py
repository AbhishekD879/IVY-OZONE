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
class Test_C2080063_Verify_THE_OPPOSITION_tab_filtering(BaseFootballBetFilter):
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
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('footballFilter'):
            raise CmsClientException('"Football Bet Filter" is disabled')
        self.__class__.coupon_name = self.open_bet_filter_via_coupon()
        self.__class__.bet_filter = self.site.football_bet_filter
        result = self.bet_filter.tab_menu.open_tab(vec.retail.THE_OPPOSITION_TAB)
        self.assertTrue(result, msg=f'"{vec.retail.THE_OPPOSITION_TAB}" tab is not active')
        self.__class__.filter_sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(self.filter_sections, msg='Can not find any sections')
        for section_name, section in self.filter_sections.items():
            section_filters = section.items_as_ordered_dict
            self.assertTrue(section_filters, msg=f'There are no any filters under "{section_name}" section')
            for filter_name, filter_ in section_filters.items():
                self.assertFalse(filter_.is_selected(expected_result=False), msg=f'"{filter_name}" filter is selected')

    def test_002_verify_filtering_by_last_game(self):
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
        self.assertIn(vec.bet_finder.FB_BET_FILTER_LAST_GAME, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAME}" filter section is not shown')
        last_game_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_LAST_GAME)
        last_game_filters = last_game_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_WIN, last_game_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_WIN}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAME}" section')
        win_filter = last_game_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_WIN)
        win_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opp_last_game=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_WIN.lower()])))
        win_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_DRAW, last_game_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_DRAW}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAME}" section')
        draw_filter = last_game_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_DRAW)
        draw_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opp_last_game=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_DRAW.lower()])))
        draw_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LOSE, last_game_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LOSE}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_LAST_GAME}" section')
        self.__class__.lose_filter = last_game_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LOSE)
        self.lose_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opp_last_game=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_LOSE.lower()])))

    def test_003_verify_filtering_by_last_6_games_point_total(self):
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
        self.lose_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT}" filter section is not shown')
        last_six_games_points_total_section = \
            self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT)
        last_six_games_points_total_filters = last_six_games_points_total_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS, last_six_games_points_total_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT}" section')
        self.__class__.zero_six_points_filter = last_six_games_points_total_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS)
        self.zero_six_points_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opp_last_6_games=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS.lower()])))
        self.zero_six_points_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_SEVEN_TWELVE_POINTS, last_six_games_points_total_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_SEVEN_TWELVE_POINTS}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT}" section')
        self.__class__.seven_twelve_points_filter = \
            last_six_games_points_total_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_SEVEN_TWELVE_POINTS)
        self.seven_twelve_points_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opp_last_6_games=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_SEVEN_TWELVE_POINTS.lower()])))
        self.seven_twelve_points_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_THIRTEEN_EIGHTEEN_POINTS, last_six_games_points_total_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_THIRTEEN_EIGHTEEN_POINTS}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT}" section')
        self.__class__.thirteen_eighteen_points_filter = \
            last_six_games_points_total_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_THIRTEEN_EIGHTEEN_POINTS)
        self.thirteen_eighteen_points_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opp_last_6_games=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_THIRTEEN_EIGHTEEN_POINTS.lower()])))

    def test_004_verify_filtering_by_key_trends(self):
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
        self.thirteen_eighteen_points_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT}" filter section is not shown')
        key_trends_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT)
        key_trends_filters = key_trends_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_HIGH_SCORING, key_trends_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_HIGH_SCORING}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT}" section')
        high_scoring_filter = key_trends_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_HIGH_SCORING)
        high_scoring_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opposition_filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_HIGH_SCORING.lower()])))
        high_scoring_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE, key_trends_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT}" section')
        leaky_defence_filter = key_trends_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE)
        leaky_defence_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opposition_filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE.lower()])))
        leaky_defence_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_CONCEDED_LAST_GAMES, key_trends_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_CONCEDED_LAST_GAMES}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT}" section')
        self.__class__.conceded_two_plus_last_games_filter = \
            key_trends_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_CONCEDED_LAST_GAMES)
        self.conceded_two_plus_last_games_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            opposition_filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_CONCEDED_LAST_GAMES.lower()])))

    def test_005_verify_filtering_by_league_positions(self):
        """
        DESCRIPTION: Verify filtering by LEAGUE POSITIONS
        DESCRIPTION: * TOP HALF
        DESCRIPTION: * BOTTOM HALF
        DESCRIPTION: * ABOVE OPPOSITION
        DESCRIPTION: * Check off 'TOP HALF' > tap 'Find Bets'.
        DESCRIPTION: * Check off 'BOTTOM HALF' > tap 'Find Bets'
        DESCRIPTION: * Check off 'ABOVE OPPOSITION' > tap 'Find Bets'
        EXPECTED: 1. Results should show data from API CALL params
        EXPECTED: * compare THE OPPOSITE TEAM for
        EXPECTED: "leaguePosition": "No" vs "teamsInLeague": "No"
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        self.conceded_two_plus_last_games_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT, self.filter_sections,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT}" filter section is not shown')
        league_positions_section = self.filter_sections.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT)
        league_positions_filters = league_positions_section.items_as_ordered_dict
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_TOP_HALF, league_positions_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_TOP_HALF}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT}" section')
        top_half_filter = league_positions_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_TOP_HALF)
        top_half_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_TOP_HALF.lower()])))
        top_half_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_BOTTOM_HALF, league_positions_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_BOTTOM_HALF}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT}" section')
        bottom_half_filter = league_positions_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_BOTTOM_HALF)
        bottom_half_filter.click()
        self.verify_number_of_bets(
            expected_number_of_bets=len(self.get_selections(coupon_name=self.coupon_name,
                                                            filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_BOTTOM_HALF.lower()])))
        bottom_half_filter.click()
        self.assertIn(vec.bet_finder.FB_BET_FILTER_OPPOSITION_BELOW_OPPOSITION, league_positions_filters,
                      msg=f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_BELOW_OPPOSITION}" filter is not shown under '
                          f'"{vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT}" section')
        below_opposition_filter = league_positions_filters.get(vec.bet_finder.FB_BET_FILTER_OPPOSITION_BELOW_OPPOSITION)
        below_opposition_filter.click()
        expected_bets = self.site.football_bet_filter.read_number_of_bets()
        self.verify_number_of_bets(
            expected_number_of_bets=expected_bets)

    def test_006_select_a_couple_of_different_filters(self):
        """
        DESCRIPTION: Select a couple of different filters
        EXPECTED: Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        self.zero_six_points_filter.click()
        self.__class__.expected_selections = self.get_selections(
            coupon_name=self.coupon_name, opposition_filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_BELOW_OPPOSITION.lower()],
            opp_last_6_games=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS.lower()])
        self.verify_number_of_bets(expected_number_of_bets=len(self.expected_selections))

    def test_007_click_find_bets_button(self):
        """
        DESCRIPTION: Click Find Bets button
        EXPECTED: Football Filter Results page is opened.
        EXPECTED: Verify that:
        EXPECTED: - Results number is correct
        EXPECTED: - List of selections is correct
        """
        if self.site.football_bet_filter.find_bets_button.is_enabled():
            self.site.football_bet_filter.find_bets_button.click()
            self.site.wait_content_state_changed(timeout=5)
            bet_filter_results_page = self.site.football_bet_filter_results_page
            results = bet_filter_results_page.coupon_results if self.device_type == "mobile" else bet_filter_results_page.number_of_results
            self.assertEqual(results, len(self.expected_selections),
                             msg=f'Results number "{results}" is not the same '
                                 f'as expected "{len(self.expected_selections)}"')
            expected_selection_names = [selection['selectionName'] for selection in self.expected_selections]
            bet_filter_results = [result.name for result in bet_filter_results_page.items]
            self.assertEqual(len(bet_filter_results), len(expected_selection_names),
                             msg=f'List of selections: \n"{bet_filter_results}" \nis not the same as '
                                 f'expected \n"{expected_selection_names}"')
        else:
            self._logger.info('There is no bets that fits selected filter')
