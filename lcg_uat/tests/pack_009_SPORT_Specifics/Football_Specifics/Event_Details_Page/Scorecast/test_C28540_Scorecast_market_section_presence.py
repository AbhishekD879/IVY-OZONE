import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.scorecast
@pytest.mark.correct_score
@pytest.mark.ob_smoke
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28540_Scorecast_market_section_presence(BaseSportTest):
    """
    TR_ID: C28540
    VOL_ID: C9697677
    NAME: Scorecast market section presence
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Scorecast market
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event_params.event_id
        self.__class__.event_name_on_sports_page = event_params.team1 + ' v ' + event_params.team2

    def test_001_open_test_event_page(self):
        """
        DESCRIPTION: Open tested Event Details page
        EXPECTED: Football Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, timeout=15)

    def test_002_event_details(self):
        """
        DESCRIPTION: Verify event name is the same as on Main <Sport> Page
        """
        event_name_details_page = self.site.sport_event_details.event_title_bar.event_name

        self._logger.debug(f'*** Event name on event details page: {event_name_details_page}')
        self.assertEqual(event_name_details_page, self.event_name_on_sports_page,
                         msg=f'Event name "{event_name_details_page}" on details '
                             f'page doesn\'t match with event name "{self.event_name_on_sports_page}" on <Sport> page')

    def test_003_market_tabs(self):
        """
        DESCRIPTION: Verify market tabs:
        EXPECTED: 'MAIN MARKETS' tab is selected by default
        EXPECTED: Order of tabs is the same as configured in CMS
        """
        markets_tabs = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        self.verify_edp_market_tabs_order(edp_market_tabs=markets_tabs.keys())

        current_tab = self.site.sport_event_details.markets_tabs_list.current
        expected_market_tab = self.get_default_tab_name_on_sports_edp(self.eventID)
        self.assertEqual(current_tab, expected_market_tab,
                         msg=f'{expected_market_tab} is not active tab, active tab is "{current_tab}"')

        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}" is not active tab after click, '
                             f'active tab is "{current_tab}"')

    def test_004_verify_scorecast_market_section(self):
        """
        DESCRIPTION: Verify Scorecast market section
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        self.assertIn(self.expected_market_sections.scorecast, markets, msg=f'SCORECAST market was not found in "{markets}"')
        scorecast = markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(scorecast, msg='SCORECAST section is not found')
        scorecast.expand()
        is_market_section_expanded = scorecast.is_expanded()
        self.assertTrue(is_market_section_expanded, msg=f'The section "{scorecast.name}" is not expanded')
        team_names = scorecast.team_names
        self._logger.debug('*** Team names: "%s"' % team_names)
        self.assertTrue(team_names, msg='Team Names field is empty')

        scorecast.first_scorer_tab.click()
        self.assertTrue(scorecast.first_scorer_tab.is_selected(timeout=3), msg=f'First scorer tab is not selected')

        scorecast.last_scorer_tab.click()
        self.assertTrue(scorecast.last_scorer_tab.is_selected(timeout=3), msg=f'Last scorer tab is not selected')
        scorecast.first_goalscorer_team_button.click()

        first_goalscorer_team_selected = scorecast.first_goalscorer_team_button.is_selected(timeout=3)
        self.assertTrue(first_goalscorer_team_selected, msg='First goal scorer team button is not selected')

        scorecast.last_goalscorer_team_button.click()

        last_goalscorer_team_selected = scorecast.last_goalscorer_team_button.is_selected(timeout=3)
        self.assertTrue(last_goalscorer_team_selected, msg='Last goal scorer team button is not selected')

        selected_player = scorecast.player_scorers_list.selected_item
        self._logger.debug('*** Selected player name is: "%s"' % selected_player)
        scorecast.player_scorers_list.select_player_by_index(index=2)

        correct_score_teams = scorecast.correct_score_teams.items_as_ordered_dict
        for score_team_name, score_team in correct_score_teams:
            self._logger.debug('*** Correct score team is: "%s"' % score_team_name)
            score_team.click()
            button_is_selected = score_team.is_selected()
            self.assertTrue(button_is_selected, msg=f'Score team: "{score_team_name}" button is not selected')
        scorecast.home_team_results_dropdown.select_value('1')
        scorecast.away_team_results_dropdown.select_value('1')
        scorecast.player_scorers_list.select_player_by_index(index=2)
        result = wait_for_result(lambda: scorecast.add_to_betslip.output_price != 'N/A',
                                 name=f'output price "{scorecast.add_to_betslip.output_price}" for selection 1-1 to appear',
                                 timeout=10)
        self.assertTrue(result, msg=f'Output price "{scorecast.add_to_betslip.output_price}" for selection 1-1 is not found')
        self.assertTrue(scorecast.add_to_betslip.is_enabled(timeout=2), msg='Bet button is not enabled')
        scorecast.add_to_betslip.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=1)
