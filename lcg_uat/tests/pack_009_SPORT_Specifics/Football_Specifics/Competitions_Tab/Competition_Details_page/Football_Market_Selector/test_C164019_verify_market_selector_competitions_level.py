import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.market_selector
@pytest.mark.competitions
@pytest.mark.cms
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C164019_Verify_Market_Selector_Competition(BaseSportTest):
    """
    TR_ID: C164019
    NAME: Verify Market selector drop down on Competition page
    DESCRIPTION: This test case verifies displaying of market with 'Next Team To Score Goal' market template name and market name in the format "First Team to Score" etc.
    """
    keep_browser_open = True
    events = {}
    markets = {vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5: 'over_under_total_goals',
               vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score: 'both_teams_to_score',
               vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_and_both_teams_to_score: 'match_result_and_both_teams_to_score',
               vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet: 'draw_no_bet',
               vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result: 'first_half_result',
               vec.siteserve.EXPECTED_MARKETS_NAMES.next_team_to_score: 'next_team_to_score',
               vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result: 'extra_time_result',
               vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify: 'to_qualify'
               }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football events with different markets
        """
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
        if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                'A-ZClassIDs').split(','):
            raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                     f'is not configured on Competitions tab')

        event = self.ob_config.add_autotest_premier_league_football_event()
        event_name = f'{event.team1} v {event.team2}'
        self._logger.info(f'*** Created Footaball event "{event_name}"')
        self.__class__.events.update({'Match Result': event_name})

        for market_name, market_short_name in self.markets.items():
            market_properties = {'cashout': True}
            if market_short_name == 'over_under_total_goals':
                market_properties.update({'over_under': 2.5})
            event = self.ob_config.add_autotest_premier_league_football_event(
                markets=[(market_short_name, market_properties)], wait_for_event=False)
            event_name = f'{event.team1} v {event.team2}'
            self._logger.info(f'*** Created Football event "{event_name}" (ID: {event.event_id}) with market "{market_name}"')
            self.__class__.events.update({market_name: event_name})

    def test_001_tap_football(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_tap_competition(self):
        """
        DESCRIPTION: Tap on Competition Module header
        """
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

    def test_003_verify_filtered_events(self):
        """
        DESCRIPTION: Verify "Market Selector" filter for competition League
        """
        markets = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default, vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result,
                   vec.siteserve.EXPECTED_MARKETS_NAMES.next_team_to_score, vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5,
                   vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score,
                   vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet, vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result,
                   vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify]
        section_name = vec.sb.TABS_NAME_TODAY if self.device_type != 'desktop' else vec.sb.TABS_NAME_TODAY.title()
        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            football_autotest_competition = tests.settings.football_autotest_competition.title()
        else:
            football_autotest_competition = tests.settings.football_autotest_competition

        self.assertIn(football_autotest_competition, competitions,
                      msg=f'"{football_autotest_competition}" is not found in the '
                          f'list of leagues "{list(competitions.keys())}"')
        competition = competitions[football_autotest_competition]

        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        self.assertTrue(leagues, msg='No leagues are present on page')
        competition_league = tests.settings.football_autotest_competition_league.title()
        self.assertIn(competition_league, leagues.keys(),
                      msg=f'League "{competition_league}" is not found in "{list(leagues.keys())}"')
        league = leagues[competition_league]
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        for market in markets:
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector
            market_dropdown.click_item(market)
            event_name = self.events[market]
            sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on page')
            section = sections.get(section_name)
            self.assertTrue(section, msg=f'Section "{section_name}" is not found in "{", ".join(sections.keys())}')
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg='No event groups found on page')
            event = events[event_name]
            self.assertTrue(section, msg=f'Event "{event_name}" is not found in "{", ".join(events.keys())}')

            self.assertTrue(event, msg=f'Incorrect filtering by "{market}" market. Event with '
                                       f'"{self.events[market]}" is not present')
            # problem occurs only with using loop
            import time
            time.sleep(5)
