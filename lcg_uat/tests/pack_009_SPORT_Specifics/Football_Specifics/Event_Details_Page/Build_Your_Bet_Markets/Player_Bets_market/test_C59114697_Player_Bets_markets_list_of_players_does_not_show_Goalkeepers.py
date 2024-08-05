import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.helpers import do_request


# @pytest.mark.tst2  # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C59114697_Player_Bets_markets_list_of_players_does_not_show_Goalkeepers(BaseBanachTest):
    """
     TR_ID: C59114697
     NAME: 'Player Bets' market's list of players does not show Goalkeepers
     DESCRIPTION: This test case verifies that Goalkeepers are not listed in the 'Player Bets' market
     PRECONDITIONS: Event with BYB mapping is available
     """
    keep_browser_open = True
    goal_keepers = []

    def get_market(self, market_name):
        markets = self.site.sport_event_details.tab_content.accordions_list.get_items(name=market_name)
        self.assertTrue(markets, msg=f'Cannot find markets on page')
        market = markets.get(market_name)
        self.assertTrue(market, msg=f'Cannot find market "{market_name}"')
        market.expand()
        return market

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with player bets markets, open its EDP
        """
        self.__class__.proxy = None
        self.__class__.eventID = self.get_ob_event_with_byb_market(
            market_name=self.expected_market_sections.player_bets.title())
        self.navigate_to_edp(event_id=self.eventID)

    def test_001___navigate_to_the_event_details_page_where_build_your_betcoralbet_builderladbrokes_tab_is_available__open_byb_tab(self):
        """
         DESCRIPTION: - Navigate to the Event Details page where 'Build Your Bet'(Coral)/'Bet Builder'(Ladbrokes) tab is available
         DESCRIPTION: - Open BYB tab
         EXPECTED: BYB tab is opened, Player Bets market is present
         """
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.site.sport_event_details.tabs_menu_byb.open_tab(self.expected_market_sections.player_bets if self.brand == "ladbrokes" else self.expected_market_sections.player_bets.title())
        self.__class__.player_bets_market = self.get_market(
            market_name=self.expected_market_sections.player_total_passes)
        self.assertTrue(self.get_players_for_event(event_id=self.eventID).as_list_of_names,
                        msg="Players are received in the response")

        self.device.driver.implicitly_wait(5)
        self.assertTrue(self.player_bets_market.has_show_more_players_button())
        self.player_bets_market.show_more_players_button.click()
        self.__class__.players_list = self.player_bets_market.display_players.items_as_ordered_dict
        self.assertGreaterEqual(list(self.players_list.keys()), sorted(list(self.players_list.keys())))

    def test_002___open_devtools_find_xhr_request_to_apiv1playersexample_httpsbuildyourbet_tst0coralcoukapiv1playersobeventid10294369__right_click_in_preview_tab_store_as_global_variable(
            self):
        """
         DESCRIPTION: - Open DevTools, find XHR request to /api/v1/players
         DESCRIPTION: (example: https://buildyourbet-tst0.coral.co.uk/api/v1/players?obEventId=10294369)
         DESCRIPTION: - Right click in Preview tab, Store as global variable
         EXPECTED: response is saved and shown as temp1 variable in console
         EXPECTED: ![](index.php?/attachments/get/113441616)
         """
        url = '%s%s' % (self.byb_hostname, self.banach_players_endpoint)
        params = (
            ('obEventId', self.eventID),
        )
        self.__class__.req = do_request(method='GET', url=url, params=params)['data']

    def test_003___execute_following_expression_in_console_to_get_list_of_goalkeeperstemp1datafilterplayer__playerpositiontitle__goalkeeper__verify_that_goalkeepers_are_not_present_in_select_a_player_dropdown_in_player_bets_marketor__check_response_manually_and_verify_that_players_who_has__positiontitle_goalkeeper__are_not_shown_in_player_bets_market(self):
        """
         DESCRIPTION: - execute following expression in console to get list of Goalkeepers:
         DESCRIPTION: temp1.data.filter(player => player.position.title === 'Goalkeeper')
         DESCRIPTION: - verify that Goalkeepers are NOT present in 'SELECT A PLAYER' dropdown in 'Player Bets' market
         DESCRIPTION: OR
         DESCRIPTION: - check response manually and verify that Players who has _position.title: "Goalkeeper"_ are not shown in 'Player Bets' market
         EXPECTED: Goalkeepers are not available for selection in 'Player Bets' market
         EXPECTED: ![](index.php?/attachments/get/113441666)
         """
        for i in self.req:
            if i['position']['title'] == 'Goalkeeper':
                self.goal_keepers.append(i['name'])
        for player in self.goal_keepers:
            self.assertNotIn(player, list(self.players_list.keys()), msg=f'player "{player}" is found in the list "{list(self.players_list.keys())}"')
