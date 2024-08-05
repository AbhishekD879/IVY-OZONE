import re
import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.build_your_bet
@vtest
class Test_C2552934_Banach_Ordering_in_Player_Bets_market_for_Football_EDP(BaseBanachTest):
    """
    TR_ID: C2552934
    NAME: Banach. Ordering in 'Player Bets' market for Football EDP
    DESCRIPTION: This test case verifies ordering in 'Player Bets' market for Football EDP
    PRECONDITIONS: **Config:**
    PRECONDITIONS: 1. 'Build Your Bet' tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: 2. Banach leagues are added and enabled in CMS -> Your Call -> YourCall Leagues
    PRECONDITIONS: 3. Event belonging to Banach league is mapped (on the Banach side) and created in OpenBet (T.I)
    PRECONDITIONS: 4. BYB markets are added in CMS (in particular case 'Player Bets' market)-> BYB -> BYB Markets
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Request for Banach players: https://coral-test2.banachtechnology.com/api/buildabet/players?obEventId=<ob_event_id>
    PRECONDITIONS: Request for Banach players statistic: https://coral-test2.banachtechnology.com/api/buildabet/playerStatistics?obEventId=<ob_event_id>&id=<player_id>
    PRECONDITIONS: Request for Banach players statistic value range: https://coral-test2.banachtechnology.com/api/buildabet/statisticValueRange?obEventId=<ob_event_id>&playerId=<player_id>&statId=<stats_id>
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet'(Coral)/'Bet Builder'(Ladbrokes) tab is available
    PRECONDITIONS: 4. Click/Tap on 'Build Your Bet/Bet Builder' tab
    """
    keep_browser_open = True
    player_bets_market = None
    byb_statistics_values_params = None

    def handle_player_cannot_be_selected_popup(self):
        sleep(6)
        try:
            self.assertFalse(self.site.wait_for_dialog(
                vec.dialogs.DIALOG_MANAGER_PLAYER_NOT_SELECTED,
                timeout=5))
        except VoltronException:
            # Handling <Player cannot Be Selected> dialog
            playerbet_dailog = self.site.wait_for_dialog(
                vec.dialogs.DIALOG_MANAGER_PLAYER_NOT_SELECTED,
                timeout=5)
            playerbet_dailog.ok_thanks_btn.click()

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

    def test_001_clicktap_players_dropdown_and_verify_ordering_of_player_names(self):
        """
        DESCRIPTION: Click/Tap 'Players' dropdown and verify ordering of player names
        EXPECTED: Player names are ordered in the following way: **Home Team first (list shown alphabetically by surname A-Z) - Away Team last (list shown alphabetically by surname A-Z)** Goalkeepers are not shown
        """
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.handle_player_cannot_be_selected_popup()
        player_bets = self.expected_market_sections.player_bets.title() if self.brand == 'bma' else self.expected_market_sections.player_bets
        self.assertTrue(
            self.site.sport_event_details.tabs_menu_byb.open_tab(player_bets),
            msg=f'"{player_bets}" tab is not active')
        self.handle_player_cannot_be_selected_popup()
        self.__class__.player_bets_market = self.get_market(market_name=self.expected_market_sections.player_total_passes)
        self.assertTrue(self.player_bets_market.is_expanded(),
                        msg=f'Market "{self.expected_market_sections.player_total_passes}" is not expanded')
        self.assertTrue(self.get_players_for_event(event_id=self.eventID).as_list_of_names,
                        msg="Players are received in the response")
        self.device.driver.implicitly_wait(3)
        if self.player_bets_market.has_show_more_players_button():
            self.assertTrue(self.player_bets_market.has_show_more_players_button())
            self.player_bets_market.show_more_players_button.click()
        sleep(2)
        self.__class__.players_list = self.player_bets_market.display_players.items_as_ordered_dict
        self.assertGreaterEqual(list(self.players_list.keys()), sorted(list(self.players_list.keys())))

    def test_002_select_some_player_name(self):
        """
        DESCRIPTION: Select some player name
        EXPECTED: * Selected player name is displayed within 'Players' dropdown
        EXPECTED: * 'Statistic' dropdown appears below with 'Stats Value' dropdown in the same row
        """
        self.__class__.byb_player_id = self.get_players_for_event(event_id=self.eventID).as_json_resp['data'][00]['id']
        byb_statistics_all = self.get_statistics(event_id=self.eventID, byb_player_id=self.byb_player_id)
        byb_statistics = sorted(byb_statistics_all.as_list_of_names)
        byb_statistics.remove('Cards') if 'Cards' in byb_statistics else None
        self.assertTrue(byb_statistics, msg="Statistics response is received")
        self.assertIn("Passes", byb_statistics, msg="Passed is not found in **player-statistics** response")
        self.__class__.player = next(iter((self.players_list.items())))[1]
        self.assertTrue(self.player.team_stat_values.selected_item,
                        msg="Stats values is not displayed")
        self.assertTrue(self.player.team_stat_values.stat_value_decrease.is_displayed(),
                        msg="Stats values decrease button is not displayed")
        self.assertTrue(self.player.team_stat_values.stat_value_increase.is_displayed(),
                        msg="Stats values increase button is not displayed")

    def test_003_clicktap_statistic_dropdown_and_verify_ordering_of_stats(self):
        """
        DESCRIPTION: Click/Tap 'Statistic' dropdown and verify ordering of stats
        EXPECTED: Statistics are sorted by alphabetical order
        """
        byb_statistics_all = self.get_statistics(event_id=self.eventID, byb_player_id=self.byb_player_id)
        byb_statistics = sorted(byb_statistics_all.as_list_of_names)
        byb_statistics.remove('Cards') if 'Cards' in byb_statistics else None
        self.assertIn("Passes", byb_statistics, msg="Passed is not found in **player-statistics** response")
        self.assertTrue(self.player.show_stats_link.is_displayed(), msg="Show Stats link is not displayed")
        self.player.show_stats_link.click()
        self.__class__.player_name = self.site.player_bets_stats_popup.player_name.text
        self.assertEqual(self.player_name, next(iter((self.players_list.items())))[0],
                         msg="Player Name is not equal with stats dialog")
        self.site.player_bets_stats_popup.back_button.click()

    def test_004_select_some_statistic(self):
        """
        DESCRIPTION: Select some statistic
        EXPECTED: * Selected statistic name is displayed within 'Statistic' dropdown
        EXPECTED: * 'Stats Value' dropdown is prepopulated with corresponding statistic average value
        """
        byb_statistics_values_params = self.get_statistic_values(event_id=self.eventID, byb_player_id=self.byb_player_id,
                                                                 byb_statistic_id=1)
        byb_statistic_value_range_resp = byb_statistics_values_params.as_json_resp
        self.assertTrue(byb_statistic_value_range_resp, msg="**statistic-value-range** response is not received")
        self.assertTrue(self.player.team_stat_values.selected_item, msg="Stat value is prepopulated")
        if self.player.team_stat_values.stat_value_decrease.is_enabled():
            self.player.team_stat_values.stat_value_decrease.click()
            sleep(1)
        if self.player.team_stat_values.stat_value_increase.is_enabled():
            self.player.team_stat_values.stat_value_increase.click()
            sleep(1)
        self.assertTrue(self.player.team_stat_values.selected_item, msg="Stat value is not empty")

    def test_005_clicktap_stats_value_dropdown_and_verify_ordering_of_values(self):
        """
        DESCRIPTION: Click/Tap 'Stats Value' dropdown and verify ordering of values
        EXPECTED: * Stats values are sorted from lowest to highest numerical order
        EXPECTED: * Stats values have **+** sign near each value
        """
        byb_statistics_values_params = self.get_statistic_values(event_id=self.eventID, byb_player_id=self.byb_player_id,
                                                                 byb_statistic_id=1)
        byb_statistic_value_range_resp = byb_statistics_values_params.as_json_resp
        stat_selected = self.player.team_stat_values.selected_item
        byb_average_value = byb_statistic_value_range_resp.get('average', '')
        stat_default = re.findall(r'\d+', stat_selected)
        stat_default_value = [int(i) for i in stat_default]
        self.assertLessEqual(stat_default_value, [byb_average_value],
                             msg=f'Statistic value "{stat_default_value}" is not the same as **average** value '
                                 f'from **statistic-value-range** response "{[byb_average_value]}"')
