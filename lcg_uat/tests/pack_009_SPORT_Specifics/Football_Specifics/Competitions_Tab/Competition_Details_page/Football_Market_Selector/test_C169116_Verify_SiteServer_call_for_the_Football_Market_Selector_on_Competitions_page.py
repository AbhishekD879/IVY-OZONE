import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import do_request
from json import JSONDecodeError


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create event in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C169116_Verify_SiteServer_call_for_the_Football_Market_Selector_on_Competitions_page(BaseBetSlipTest):
    """
    TR_ID: C169116
    NAME: Verify SiteServer call for the Football Market Selector on Competitions page
    DESCRIPTION: This test case verifies SiteServer call for the Football Market Selector on Competitions page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |Total Goals Over/Under| (rawHandicapValue="2.5") - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: * |Next Team to Score| - "Next Team to Score"
    PRECONDITIONS: * |Extra-Time Result| - Extra Time Result
    """
    keep_browser_open = True
    markets = [('to_qualify', ),
               ('over_under_total_goals', {'over_under': 2.5}),
               ('both_teams_to_score', ),
               ('draw_no_bet', ),
               ('first_half_result', ),
               ('match_result_and_both_teams_to_score', ),
               ('next_team_to_score', ),
               ('extra_time_result', )]

    def navigate_to_league(self, league_category, league_name):
        if self.device_type == 'mobile':
            category = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict.get(
                league_category)
        else:
            category = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(league_category)
        self.assertTrue(category, msg='category is not displayed')
        if not category.is_expanded():
            category.expand()
        league = category.items_as_ordered_dict.get(league_name)
        league.click()
        self.assertTrue(self.site.football.tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed for Football')

    def template_market_name_SS_request(self):

        url = 'market.templateMarketName'
        perflog = self.device.get_performance_log()

        for log in list(perflog[::-1]):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    self.__class__.final_request_url = request_url
                    return self.final_request_url

            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. Load Oxygen application
        PRECONDITIONS: 2. Go to Football Landing page
        PRECONDITIONS: 3. Click/Tap on Competition Module header
        PRECONDITIONS: 4. Click/Tap on sub-category (Class ID) with Type ID's
        PRECONDITIONS: 5. Choose Competition (Type ID)
        """
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='football', status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for football sport')

            event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
            self.__class__.eventID = event.event_id

        self.site.wait_content_state('homepage')
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state('football')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            league = 'Auto Test'
            self.navigate_to_league(league_category=league,
                                    league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
        else:
            league = 'AUTO TEST'
            self.navigate_to_league(league_category=league, league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)

    def test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_different_markets_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName attribute' for different markets in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * Match Betting
        EXPECTED: * To Qualify
        EXPECTED: * Both Teams to Score
        EXPECTED: * Over/Under Total Goals (rawHandicapValue="2.5")
        EXPECTED: * Draw No Bet
        EXPECTED: * Match Result and Both Teams To Score
        EXPECTED: * First-Half Result
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra-Time Result
        """
        request_data = self.template_market_name_SS_request()
        markets = \
            request_data.replace("%20", " ").split("simpleFilter=market.templateMarketName:intersects:")[1].split("&translationLang=")[0]
        self.assertTrue(markets, msg=f'Market data in SS request "{markets}" is not displayed')

        self.__class__.expected_market_list = [
            vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default if self.site.brand == 'ladbrokes' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting,
            vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify,
            'Match Result and Both Teams To Score',
            vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5.split(" 2.5")[0] if self.site.brand == 'bma' else "Over/Under Total Goals",
            vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score,
            vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet,
            vec.siteserve.EXPECTED_MARKETS_NAMES.next_team_to_score,
            'First-Half Result',
            'Extra-Time Result']

        response = do_request(url=self.final_request_url, method='GET')

        actual_SS_market_list = []
        for event in response['SSResponse']['children']:
            if "".join(list(event.keys())) == "event":
                for market in event['event']['children']:
                    if event['event']['id'] == self.eventID:
                        actual_SS_market_list.append(market['market']['templateMarketName'])

        for market in self.expected_market_list:
            self.assertIn(market, actual_SS_market_list,
                          msg=f'Expected market: "{market} is not in'
                              f'Actual market List: "{actual_SS_market_list}"')

    def test_002_verify_options_available_for_football_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify options available for Football in the 'Market Selector' dropdown list
        EXPECTED: The following options are displayed in the Market selector dropdown list:
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra Time Result
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * Match Result and Both Teams To Score
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        """
        actual_markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        self.expected_market_list[0] = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result if self.site.brand == 'bma' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.expected_market_list[2] = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_and_both_teams_to_score
        self.expected_market_list[3] = vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5
        self.expected_market_list[6] = vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result
        self.expected_market_list[7] = '1st Half Result'
        self.expected_market_list[8] = vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result

        for market in self.expected_market_list:
            self.assertIn(market, actual_markets_list,
                          msg=f'Expected market: "{market} is not in'
                              f'Actual market List: "{actual_markets_list}"')
