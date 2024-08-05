import pytest
from json import JSONDecodeError
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import do_request
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C145822_Verify_SiteServer_call_for_the_Football_Market_Selector_on_Landing_page(BaseSportTest):
    """
    TR_ID: C145822
    NAME: Verify SiteServer call for the Football Market Selector on Landing page
    DESCRIPTION: This test case verifies that SiteServer call "simpleFilter=market.templateMarketName" is using instead of the "simpleFilter=market.name".
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event and navigate to football/matches
        EXPECTED: Navigate to Football Matches tab
        """
        markets = [('to_qualify',),
                   ('over_under_total_goals', {'over_under': 2.5}),
                   ('both_teams_to_score',),
                   ('draw_no_bet',),
                   ('first_half_result',),
                   ('match_result_and_both_teams_to_score',), ]

        event = self.ob_config.add_autotest_premier_league_football_event(markets=markets)
        self.__class__.eventID = event.event_id

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL', timeout=60)
        result = wait_for_result(
            lambda: self.site.sports_page.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Sport landing page is not loaded completely')

        current_tab_name = self.site.football.tabs_menu.current
        matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                   self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, matches_tab_name,
                         msg=f'Current active tab: "{current_tab_name}", instead of "{matches_tab_name}"')

    def test_001_go_to_network___all___headers_and_find_simplefiltermarkettemplatemarketname_in_ss_request(self):
        """
        DESCRIPTION: Go to Network -> All -> **Headers** and find 'simpleFilter=market.templateMarketName' in SS request
        EXPECTED: The following values are displayed in the SS request to get the list of particular markets:
        EXPECTED: * Match Betting
        EXPECTED: * To Qualify
        EXPECTED: * Over/Under Total Goals
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * First-Half Result
        """
        request_data = self.template_market_name_SS_request()

        actual_markets = \
            request_data.replace("%20", " ").split("simpleFilter=market.templateMarketName:intersects:")[1].split("&translationLang=")[0]

        expected_markets = "|Match Betting|,|Over/Under Total Goals|,|Both Teams to Score|,|To Qualify|,|Draw No Bet|,|First-Half Result|,|Match Result and Both Teams To Score|"

        self.assertIn(expected_markets, actual_markets,
                      msg=f'Actual market data in SS request "{actual_markets}" is not matching with expected market "{expected_markets}"')

    def test_002_go_to_network___all___preview_and_find_templatemarketname_attribute_for_different_markets_in_ss_response(
            self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName attribute' for different markets in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * Match Betting
        EXPECTED: * To Qualify
        EXPECTED: * Over/Under Total Goals
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * First-Half Result
        """
        self.__class__.expected_market_list = [
            vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default if self.site.brand == 'ladbrokes' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting,
            vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify,
            'Match Result and Both Teams To Score',
            vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5.split(" 2.5")[0] if self.site.brand == 'bma' else "Over/Under Total Goals",
            vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score,
            vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet,
            'First-Half Result']

        response = do_request(url=self.final_request_url, method='GET')

        actual_SS_market_list = []
        for event in response['SSResponse']['children']:
            if "".join(list(event.keys())) == "event":
                for market in event['event']['children']:
                    if event['event']['id'] == self.eventID:
                        actual_SS_market_list.append(market['market']['templateMarketName'])

        self.assertEqual(sorted(actual_SS_market_list), sorted(self.expected_market_list),
                         msg=f'Actual market list from UI "{sorted(actual_SS_market_list)}" is not matching with expected market list "{sorted(self.expected_market_list)}"')

    def test_003_verify_options_available_for_football_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify options available for Football in the 'Market selector' dropdown list
        EXPECTED: The following options are displayed in the Market selector dropdown list:
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        """
        actual_markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        self.expected_market_list[0] = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result if self.site.brand == 'bma' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.expected_market_list[2] = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_and_both_teams_to_score
        self.expected_market_list[3] = vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5
        self.expected_market_list[6] = vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result

        self.assertEqual(sorted(actual_markets_list), sorted(self.expected_market_list),
                         msg=f'Actual market list from UI "{sorted(actual_markets_list)}" is not matching with expected market list "{sorted(self.expected_market_list)}"')
