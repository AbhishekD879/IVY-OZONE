import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.google_analytics
@pytest.mark.market_selector
@pytest.mark.competitions
@pytest.mark.markets
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.other
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-57172')  # Issue in coral only. todo : Need to remove this marker after given epic was closed
class Test_C360236_tracking_market_selector_competition(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C360236
    VOL_ID: C9698373
    NAME: Verify Market Selector Tracking on Competition page
    """
    keep_browser_open = True
    event_both_teams_to_score = None
    football_autotest_competition_league = tests.settings.football_autotest_competition_league.title()

    def test_000_add_event(self):
        """
        DESCRIPTION: Add football event with different markets
        """
        self.__class__.markets = {
            vec.siteserve.EXPECTED_MARKETS_NAMES.match_result if vec.siteserve.EXPECTED_MARKETS_NAMES.match_result == 'Match Result' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default: 'Match Result',
            vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify: 'To Qualify',
            vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_and_both_teams_to_score: 'Match Result & Both Teams To Score',
            vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5: 'Total Goals Over/Under 2.5',
            vec.siteserve.EXPECTED_MARKETS_NAMES.next_team_to_score: 'Next Team to Score',
            vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score: 'Both Teams to Score',
            vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet: 'Draw No Bet',
            vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result: '1st Half Result',
            vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result: 'Extra Time Result'}
        self.ob_config.add_autotest_premier_league_football_event(markets=[
            ('both_teams_to_score', {'cashout': True}),
            ('draw_no_bet', {'cashout': True}),
            ('first_half_result', {'cashout': True}),
            ('to_qualify', {'cashout': True}),
            ('next_team_to_score', {'cashout': True}),
            ('extra_time_result', {'cashout': True}),
            ('over_under_total_goals', {'cashout': True, 'over_under': 2.5}),
            ('match_result_and_both_teams_to_score', {'cashout': True})])

        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5] = 'Over/Under Total Goals 2.5'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_and_both_teams_to_score] = 'Match Result and Both Teams To Score'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result] = 'First-Half Result'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result] = 'Extra-Time Result'

    def test_001_tap_football(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.wait_content_state('Homepage')
        self.navigate_to_page(name='sport/football')
        self.site.wait_splash_to_hide(5)
        self.site.wait_content_state('Football')

    def test_002_tap_on_competitions(self):
        """
        DESCRIPTION: Tap on COMPETITIONS Module header
        """
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competitions tab is not active, active is "{active_tab}"')

    def test_003_verify_tracking(self):
        """
        DESCRIPTION: Verify "Market Selector" tracking for competition League
        """
        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')
        self.__class__.competition = tests.settings.football_autotest_competition.title() if \
            self.brand == 'ladbrokes' and self.device_type == self.device_type == 'desktop' else tests.settings.football_autotest_competition
        self.assertIn(self.competition, competitions.keys())
        competition = competitions[self.competition]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(self.football_autotest_competition_league, leagues)

        league = leagues[self.football_autotest_competition_league]
        league.click()
        self.site.wait_content_state_changed()
        self.site.wait_content_state(state_name='CompetitionLeaguePage')
        self.site.wait_splash_to_hide(5)
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections are present on page')
        section_name, section = list(sections.items())[0]
        self._logger.info(f'*** Verifying market selector tracking for section {section_name}')

        for market_name, market_name_in_response in self.markets.items():
            if self.device_type == 'desktop':
                self.site.competition_league.tab_content.dropdown_market_selector.select_value(value=market_name)
            else:
                market_selector = self.site.competition_league.tab_content.dropdown_market_selector
                market_selector.scroll_to()
                market_selector.value = market_name
            self.site.wait_content_state_changed()
            events = self.site.competition_league.tab_content.accordions_list
            wait_for_result(lambda: events.items_as_ordered_dict,
                            name='Events list is loaded',
                            timeout=5)
            if self.device_type == 'mobile':
                actual_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
                self.site.football.tab_content.dropdown_market_selector.scroll_to()
            else:
                actual_market = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
                self.site.competition_league.tab_content.dropdown_market_selector.scroll_to()
            self.assertEqual(actual_market.upper(), market_name.upper(),
                             msg=f'Actual market: "{actual_market.upper()}" is not same as '
                                 f'Expected market: "{market_name.upper()}"')
            self.expected_market_selector_response['categoryID'] = str(self.ob_config.backend.ti.football.category_id)
            self.expected_market_selector_response['eventLabel'] = market_name_in_response
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value='change market')
            self.compare_json_response(actual_response, self.expected_market_selector_response)
            sleep(5)  # need because of compare_json_response works faster than dropdown_market closed
