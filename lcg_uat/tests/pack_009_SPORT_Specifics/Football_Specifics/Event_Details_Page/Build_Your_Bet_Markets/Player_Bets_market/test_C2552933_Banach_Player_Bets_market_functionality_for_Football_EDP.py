import re
import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.player_bets
@pytest.mark.markets
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C2552933_Banach_Player_Bets_market_functionality_for_Football_EDP(BaseBanachTest):
    """
    TR_ID: C2552933
    NAME: Banach Player Bets market functionality for Football EDP
    DESCRIPTION: This test case verifies 'Player Bets' market functionality for Football EDP
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
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet' tab is available
    """
    keep_browser_open = True
    player_bets_market = None
    ui_statistics = None
    byb_average_value = None
    byb_statistics_values_params = None
    byb_statistics_values = None

    def handle_player_cannot_be_selected_popup(self):
        sleep(3)
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
        if tests.settings.backend_env == 'prod':
            self.__class__.proxy = None
            self.__class__.eventID = self.get_ob_event_with_byb_market(
                market_name=self.expected_market_sections.player_bets.title())
        else:
            self.__class__.eventID = self.create_ob_event_for_mock(team1='Test team 1', team2='Test team 2')
        self.navigate_to_edp(event_id=self.eventID)

    def test_001_clicktap_on_build_your_bet_tab_where_player_bets_market_is_available(self):
        """
        DESCRIPTION: Click/Tap on 'Build Your Bet' tab where 'Player Bets' market is available
        EXPECTED: * 'Player Bets' accordion is present and contains 'Players' dropdown
        EXPECTED: * Banach **players** response is received
        """
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.handle_player_cannot_be_selected_popup()
        player_bets = self.expected_market_sections.player_bets.title() if self.brand == 'bma' else self.expected_market_sections.player_bets
        self.site.sport_event_details.tabs_menu_byb.open_tab(player_bets)
        self.__class__.player_bets_market = self.get_market(
            market_name=self.expected_market_sections.player_total_passes)
        self.assertTrue(self.get_players_for_event(event_id=self.eventID).as_list_of_names,
                        msg="Players are received in the response")

    def test_002_clicktap_players_dropdown_and_verifies_the_list_of_player_names_inside(self):
        """
        DESCRIPTION: Click/Tap 'Players' dropdown and verifies the list of player names inside
        EXPECTED: List of players corresponds to **name** attributes received in **players** response
        """
        self.device.driver.implicitly_wait(3)
        self.assertTrue(self.player_bets_market.has_show_more_players_button())
        self.player_bets_market.show_more_players_button.click()
        self.device.driver.implicitly_wait(1)
        self.__class__.players_list = self.player_bets_market.display_players.items_as_ordered_dict
        self.assertGreaterEqual(list(self.players_list.keys()), sorted(list(self.players_list.keys())))

    def test_003_select_some_player_name(self):
        """
        DESCRIPTION: Select some player name
        EXPECTED: * Banach **player-statistics** response is received
        EXPECTED: * 'Statistic' dropdown appears in the row below
        """
        byb_statistics_all = self.get_statistics(event_id=self.eventID)
        byb_statistics = sorted(byb_statistics_all.as_list_of_names)
        byb_statistics.remove('Cards') if 'Cards' in byb_statistics else None
        self.assertTrue(byb_statistics, msg="Statistics response is received")
        self.__class__.player = next(iter((self.players_list.items())))[1]
        self.assertTrue(self.player.team_stat_values.selected_item,
                        msg="Stats values is not displayed")
        self.assertTrue(self.player.team_stat_values.stat_value_decrease.is_displayed(),
                        msg="Stats values decrease button is not displayed")
        self.assertTrue(self.player.team_stat_values.stat_value_increase.is_displayed(),
                        msg="Stats values increase button is not displayed")

    def test_004_clicktap_statistic_dropdown_and_verifies_statistics_data_inside(self):
        """
        DESCRIPTION: Click/Tap 'Statistic' dropdown and verifies statistics data inside
        EXPECTED: List of statistics corresponds to **title** attributes received in Banach **player-statistics** response
        """
        self.__class__.byb_player_id = self.get_players_for_event(event_id=self.eventID).as_json_resp['data'][00]['id']
        byb_statistics_all = self.get_statistics(event_id=self.eventID, byb_player_id=self.byb_player_id)
        byb_statistics = sorted(byb_statistics_all.as_list_of_names)
        byb_statistics.remove('Cards') if 'Cards' in byb_statistics else None
        self.assertIn("Passes", byb_statistics, msg="Passed is not found in **player-statistics** response")
        self.assertTrue(self.player.show_stats_link.is_displayed(), msg="Show Stats link is not displayed")
        self.player.show_stats_link.click()
        self.__class__.player_name = self.site.player_bets_stats_popup.player_name.text
        self.assertIn(self.player_name, next(iter((self.players_list.items())))[0],
                      msg="Player Name is not equal with stats dialog")
        self.site.player_bets_stats_popup.back_button.click()

    def test_005_select_some_statistic(self):
        """
        DESCRIPTION: Select some statistic
        EXPECTED: * Banach **statistic-value-range** response is received
        EXPECTED: * 'Stats Value' dropdown is prepopulated with value
        """
        byb_statistics_values_params = self.get_statistic_values(event_id=self.eventID,
                                                                 byb_player_id=self.byb_player_id, byb_statistic_id=1)
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

    def test_006_verify_prepopulated_value(self):
        """
        DESCRIPTION: Verify prepopulated value
        EXPECTED: * Integer number is displayed that corresponds to **average** attribute in **statistic-value-range** response
        EXPECTED: * In case NOT integer is received it should be rounded (i.e. 2.4 -> 2 and 2.5 -> 3)
        EXPECTED: * In case average is below minimum value, minimum value is displayed that corresponds to 'minValue'  in **statistic-value-range** response
        EXPECTED: * In case average is above maximum value, maximum value is displayed  that corresponds to 'maxValue'  in **statistic-value-range** response
        """
        byb_statistics_values_params = self.get_statistic_values(event_id=self.eventID,
                                                                 byb_player_id=self.byb_player_id, byb_statistic_id=1)
        byb_statistic_value_range_resp = byb_statistics_values_params.as_json_resp
        self.assertTrue(self.player.team_stat_values.selected_item, msg="Stat Value is prepopulated")
        byb_average_value = byb_statistic_value_range_resp.get('average', '')
        self.assertTrue([byb_average_value],
                        msg=f'Statistic **average** value from **statistic-value-range** response is "{[byb_average_value]}"')

    def test_007_clicktap_stats_value_dropdown(self):
        """
        DESCRIPTION: Click/Tap 'Stats Value' dropdown
        EXPECTED: List of values is displayed
        EXPECTED: * Values are displayed in increments of 1, e.g.:
        EXPECTED: if minValue:1 and maxValue:6, then dropdown will contain 1+,2+,3+,4+,5+,6+ values
        """
        self.__class__.byb_statistics_values_params = self.get_statistic_values(event_id=self.eventID,
                                                                                byb_player_id=self.byb_player_id,
                                                                                byb_statistic_id=1)
        byb_statistic_value_range_resp = self.byb_statistics_values_params.as_json_resp
        stat_selected = self.player.team_stat_values.selected_item
        byb_min_value = byb_statistic_value_range_resp.get('minValue', '')
        stat_default = re.findall(r'\d+', stat_selected)
        stat_default_value = [int(i) for i in stat_default]
        self.assertGreaterEqual(stat_default_value, [byb_min_value], msg="SelectedItem is less than minValue")
        if self.player.team_stat_values.stat_value_increase.is_enabled():
            self.player.team_stat_values.stat_value_increase.click()
            sleep(1)
        stat_selected = self.player.team_stat_values.selected_item
        stat_default = re.findall(r'\d+', stat_selected)
        stat_default_value = [int(i) for i in stat_default]
        byb_max_value = byb_statistic_value_range_resp.get('maxValue', '')
        self.assertLessEqual(stat_default_value, [byb_max_value], msg="SelectedItem is less than minValue")

    def test_008_select_value_other_then_prepopulated(self):
        """
        DESCRIPTION: Select value other then prepopulated
        EXPECTED: Selected value is displayed within 'Stats Value' dropdown box
        """
        stat_selected = self.player.team_stat_values.selected_item
        if self.player.team_stat_values.stat_value_increase.is_enabled():
            self.player.team_stat_values.stat_value_increase.click()
            sleep(1)
            new_stat_selected_after_increment = self.player.team_stat_values.selected_item
            self.assertNotEqual(new_stat_selected_after_increment, stat_selected,
                                msg="the new stat is not getting updated")
        if self.player.team_stat_values.stat_value_decrease.is_enabled():
            self.player.team_stat_values.stat_value_decrease.click()
            sleep(1)
            new_stat_selected_after_decrement = self.player.team_stat_values.selected_item
            self.assertTrue(new_stat_selected_after_decrement,
                            msg="the new stat is not getting updated")

    def test_009_click_add_to_bet_button(self):
        """
        DESCRIPTION: Click 'ADD TO BET' button
        EXPECTED: * '1. SELECT A PLAYER' label with one dropdown below is shown
        EXPECTED: * No player is selected by default
        EXPECTED: * 'Select Player' message is displayed within dropdown box
        EXPECTED: * Selection is added to Dashboard
        """
        self.assertTrue(self.player.add_to_betslip_button.is_displayed(),
                        msg='ADD TO BET button has not appeared')
        self.player.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB dashboard is not available')
        selection_names = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.summary_description.dashboard_market_text
        self.assertTrue(selection_names, msg=f'List of BYB selections is empty"')
        self.assertIn(self.player_name.upper(), selection_names,
                      msg=f'Selected player "{self.player_name}" is not found among BYB dashboard selections '
                          f'"{selection_names}"')
