import pytest
import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.lad_stg2
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.bet_placements
@pytest.mark.event_details
@pytest.mark.five_a_side_leaderboard
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@vtest
class Test_C65233214_Verify_MAXIMUM_ENTRIES_PER_USER_text_on_Leaderboard_is_not_displayed_if_Teams_entry_is_empty_in_CMS(BaseFiveASide):
    """
    TR_ID: C65233214
    NAME: Verify MAXIMUM ENTRIES PER USER text on Leaderboard is not displayed if Teams entry is empty in CMS
    DESCRIPTION: Verify MAXIMUM ENTRIES PER USER text on Leaderboard is not displayed if Teams entry is empty in CMS
    PRECONDITIONS: Contest name: Team1 vs Team2 (event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: event id
    PRECONDITIONS: Size: 5
    PRECONDITIONS: Teams: Blank
    PRECONDITIONS: User's Allowed: Test Account
    """
    keep_browser_open = True
    stake_value = 1
    proxy = None

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Assists',
            'Passes': 'Goals Outside The Box',
            'Assists': 'Goals',
            'Shots': 'Shots'
        },
        'Stats': {
            'To Concede': '1',
            'Assists': '1',
            'Goals Outside The Box': '1',
            'Goals': '1',
            'Shots': '6'
        }
    }

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Contest name: Team1 vs Team2 (event id)
        PRECONDITIONS: Stake: 1
        PRECONDITIONS: Event: event id
        PRECONDITIONS: Size: 5
        PRECONDITIONS: Teams: Blank
        PRECONDITIONS: User's Allowed: Test Account
        """
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        market_name = vec.yourcall.MARKETS.player_bets
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.home_team = event_resp[0]['event']['name'].split("|")[1]
        self.__class__.away_team = event_resp[0]['event']['name'].split("|")[5]
        event_start_time = event_resp[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=time_format,
            ss_data=True)
        self.__class__.full_event_name = f'{self.event_name} {self.event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{self.full_event_name}" with market name "{market_name}", '
            f'event id "{self.event_name}", event start time "{self.event_start_time_local}"')
        contest_name = f"Auto test " + self.event_name + " " + "(" + str(event_id) + ")"
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        self.cms_config.create_five_a_side_show_down(contest_name=contest_name,
                                                     entryStake="1", size="5", teams="",
                                                     event_id=event_id, display=True)
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.get_balance_by_page('all')
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.five_a_side),
                        msg=f'"{self.expected_market_tabs.five_a_side}" tab is not active')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')

        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get(self.Test['Combination']).click()

    def test_001_select_all_players_for_5_a_side_formation(self):
        """
        DESCRIPTION: On Betslip page (Before placing bet):
        EXPECTED: - Single contest should be available along with contest name
        """
        tab_content = self.site.sport_event_details.tab_content
        self.__class__.expected_players_list = []
        self.__class__.pitch_overlay = tab_content.pitch_overlay.content
        markets = self.pitch_overlay.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        used_players = []
        for market_name, market in list(markets.items()):
            if tab_content.pitch_overlay.has_journey_panel:
                tab_content.pitch_overlay.journey_panel.close_button.click()

            players = self.open_players_list(market=market, market_name=market_name)
            self.assertTrue(players, msg='Players are not displayed on the Players List')

            first_player_name = list(players.keys())[0]
            last_player_name = list(players.keys())[-1]
            for player_name, player in players.items():
                if player_name not in used_players:
                    try:
                        player.click()
                        self._logger.info(f'F*** Selecting player "{player_name}" for market "{market_name}"')
                        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                                        msg='Player Card is not shown')
                    except VoltronException:
                        # Handling <Player cannot Be Selected> dialog
                        five_a_side_dailog = self.site.wait_for_dialog(
                            vec.dialogs.DIALOG_MANAGER_5ASIDE_PLAYER_NOT_SELECTED,
                            timeout=5)
                        five_a_side_dailog.ok_thanks_btn.click()
                        continue
                    five_a_side_tab = self.site.sport_event_details.tab_content
                    self.assertTrue(five_a_side_tab, msg="5-A-Side tab content is not found")
                    player_card = five_a_side_tab.player_card
                    self.assertTrue(player_card.add_player_button.is_enabled(), msg='Add player button is not enabled')

                    # Selecting Market dropdown ..
                    market_dropDown = self.site.sport_event_details.tab_content.player_card.market_drop_down
                    self.assertTrue(market_dropDown,
                                    msg='Drop-down with the list of the markets is not present in player cards')
                    self.site.sport_event_details.tab_content.player_card.market_drop_down.click()
                    self.site.sport_event_details.tab_content.player_card.items_as_ordered_dict[
                        self.Test['Market'][market_name]].click()

                    # Updating stats ..
                    if self.Test['Market'][market_name] != 'To Be Carded':
                        try:
                            self.site.sport_event_details.tab_content.player_card.minus_button.click()
                            sleep(2)
                            stat = self.site.sport_event_details.tab_content.player_card.step_value
                            self._logger.info(
                                f'*** Decremented stat for player "{player_name}" & market "{market_name}", Stat: "{stat}"')
                        except ElementClickInterceptedException:
                            try:
                                self.site.sport_event_details.tab_content.player_card.plus_button.click()
                                sleep(2)
                                stat = self.site.sport_event_details.tab_content.player_card.step_value
                                self._logger.info(
                                    f'*** Incremented stat for player "{player_name}" & market "{market_name}", Stat: "{stat}"')
                            except ElementClickInterceptedException:
                                stat = self.site.sport_event_details.tab_content.player_card.step_value
                                self._logger.info(
                                    f'*** Cannot decrement/increment stat for player "{player_name}" & market "{market_name}", Stat: "{stat}"')
                    player_card.add_player_button.click()
                    sleep(5)
                    self.assertFalse(five_a_side_tab.wait_for_players_card_closed(timeout=10),
                                     msg='Players card has not been closed')
                    self.assertTrue(market.added_player_name,
                                    msg=f'Failed to display added Player\'s Name "{player_name}"')
                    used_players.append(player_name)
                    current_player_name = player_name
                    if self.pitch_overlay.wait_for_error_message(timeout=5):
                        market_index = 0
                        markets_count = 1
                        while self.pitch_overlay.wait_for_error_message(timeout=5) and (market_index < markets_count):
                            self._logger.info(
                                f'*** Encountered error "{self.pitch_overlay.error_message_text}", trying next player')
                            self.assertNotEqual(current_player_name, last_player_name,
                                                msg=f'No compatible players found for "{first_player_name}"')
                            market.icon.click()
                            sleep(2)
                            self.site.sport_event_details.tab_content.player_card.market_drop_down.click()
                            sleep(1)
                            markets_dropdown_list = list(
                                self.site.sport_event_details.tab_content.player_card.items_as_ordered_dict.keys())
                            markets_count = len(markets_dropdown_list)
                            self.site.sport_event_details.tab_content.player_card.items_as_ordered_dict[
                                markets_dropdown_list[market_index]].click()
                            market_index += 1
                            sleep(1)
                            update_player_btn = self.site.sport_event_details.tab_content.player_card.update_player_button
                            self.assertTrue(update_player_btn,
                                            msg='Update player button is not present in player cards')
                            self.site.sport_event_details.tab_content.player_card.update_player_button.click()
                            self.assertTrue(self.pitch_overlay, msg='Pitch View section is not displayed')
                        if markets_count == market_index:
                            self.assertFalse("Not able to resolve combination error even with different markets also")
                    if market_name in ('To Be Carded', 'To Concede'):
                        expected_market_name = (
                            f'{market.added_player_name} {market.name}').split(' - ')[0]
                    elif 'Shots' or 'Offsides' in market_name:  # Added Offsides
                        expected_market_name = f'{market.added_player_name} To Have {market.name}'
                    else:
                        expected_market_name = f'{market.added_player_name} To Make {market.name}'
                    self.expected_players_list.append(expected_market_name)
                    break
        self._logger.info('############### Data Set used in this test ###############')
        print(self.expected_players_list)

    def test_002_Enter_Stake_1_and_tap_place_bet_button(self):
        """
        DESCRIPTION: On Bet Receipt Page:
        EXPECTED: - "Bet Placed Successfully" text should be displayed
        EXPECTED: - "Your team has been entered into a 5-A-Side Leaderboard!" message should be displayed
        EXPECTED: - "VIEW ENTRY" button should be available
        """
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        if not self.is_safari:
            self.get_web_socket_response(self.response_50001)
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

        byb_betslip_panel = self.site.byb_betslip_panel
        self.__class__.betslip_odds = byb_betslip_panel.selection.content.odds
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.verify_user_balance(expected_user_balance=self.user_balance - self.stake_value)

    def test_003_Click_on_button_VIEW_ENTRY(self):
        """
        EXPECTED: - User should be on Leaderboard
        """
        bet_receipt_view_entry = self.site.byb_bet_receipt_panel.view_entry
        bet_receipt_view_entry.view_entry_button.click()
        sleep(5)
        wait_for_result(lambda: self.site.five_A_side_leaderboard.is_displayed(),
                        timeout=30,
                        name='five a side leaderboard is not displayed')

    def test_004_Click_on_button_VIEW_ENTRY(self):
        """
        EXPECTED: -Team1 name, Team2 name should be displayed. 5-A-Side logo is displayed.
        EXPECTED: -Header "5-A-SIDE LEADERBOARD" is displayed.
        EXPECTED: -<Maximum {Size} total entries (1/{Size})> should be available
        EXPECTED: -BUILD ANOTHER TEAM" Button should be enabled
        EXPECTED: -RETURN TO LOBBY" link should be available
        """
        self.assertEqual(self.site.five_A_side_leaderboard.home_team_name.text, self.home_team.upper(),
                         msg=f'"Home Team" name{self.site.five_A_side_leaderboard.home_team_name.text} '
                             f'is not same as expected {self.home_team}')
        self.assertEqual(self.site.five_A_side_leaderboard.away_team_name.text, self.away_team.upper(),
                         msg=f'"Away Team" name{self.site.five_A_side_leaderboard.away_team_name} '
                             f'is not same as expected {self.away_team}')
        self.assertTrue(self.site.five_A_side_leaderboard.total_entries,
                        msg='"Maximum {Size} total entries" text not displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.terms_rules_header.is_displayed(),
                        msg='"5-A-SIDE LEADERBOARD" header not displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.build_btn.is_displayed(),
                        msg='"BUILD ANOTHER TEAM" Button Not Displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.return_to_lobby.is_displayed(),
                        msg='"RETURN TO LOBBY" Link Not Displayed')

    def test_005_Verify_Maximum_Teams_entries_per_user_1_Teams_should_not_be_available(self):
        """
        EXPECTED: -<Maximum {Teams} entries per user (1/{Teams})> should not be available
        """
        self.assertFalse(self.site.five_A_side_leaderboard.entries_per_user,
                         msg='"Maximun entries per user" is not displayed')
