import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.waiters import wait_for_result
from urllib.parse import unquote


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.bet_placements
@pytest.mark.event_details
@pytest.mark.five_a_side_leaderboard_reg_tests
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@pytest.mark.reg156_fix
@vtest
class Test_C65248906_Verify_user_can_select_a_contest_out_of_many_place_bet_and_click_on_View_Entry(BaseFiveASide):
    """
    TR_ID: C65248906
    NAME: Verify user can select a contest out of many, place bet and click on View Entry
    DESCRIPTION: Verify user can select a contest out of many, place bet and click on View Entry
    PRECONDITIONS: Contest1:
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 5
    PRECONDITIONS: Teams: 2
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Contest2:
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)_1
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 5
    PRECONDITIONS: Teams: 2
    PRECONDITIONS: User's Allowed: Test Account
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Contest name1: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 5
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Contest name2: {Team1}vs{Team2}(event id)_1
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 5
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: User is logged in and on Football event details page:
        DESCRIPTION: - '5 A Side' sub tab (event type specified above):
        DESCRIPTION: - 'Build a team' button (pitch view)
        """
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        market_name = vec.yourcall.MARKETS.player_bets
        event_name = normalize_name(event_resp[0]['event']['name'])
        event_start_time = event_resp[0]['event']['startTime']
        event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=time_format,
            ss_data=True)
        full_event_name = f'{event_name} {event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{full_event_name}" with market name "{market_name}", '
            f'event id "{event_name}", event start time "{event_start_time_local}"')
        self.__class__.contest_name_1 = f"Auto test " + event_name + " " + "(" + str(event_id) + ")_8906"
        contest_name_2 = f"Auto test " + event_name + " " + "(" + str(event_id) + ")_8906_1"
        self.__class__.contest1 = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name_1,
                                                                               entryStake="1", size="5", teams="2",
                                                                               event_id=event_id, display=True)
        self.cms_config.create_five_a_side_show_down(contest_name=contest_name_2,
                                                     entryStake="1", size="5", teams="2",
                                                     event_id=event_id, display=True)
        self.site.login(username=tests.settings.betplacement_user)
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
        formation_carousel.get('BALANCED').click()

    def test_001_select_all_players_for_5_a_side_formation_and_click_on_place_bet(self):
        """
        DESCRIPTION: Select all players for 5-A-Side formation
        DESCRIPTION: Click on Place Bet
        EXPECTED: On Betslip page (Before placing bet):
        EXPECTED: Single contest should be available along with contest name and
        EXPECTED: should be same as in CMS
        """
        tab_content = self.site.sport_event_details.tab_content
        self.__class__.expected_players_list = []
        self.__class__.pitch_overlay = tab_content.pitch_overlay.content
        markets = self.pitch_overlay.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        self.__class__.used_players = []
        self.__class__.current_player_name = None
        for market_name, market in list(markets.items()):
            if tab_content.pitch_overlay.has_journey_panel:
                tab_content.pitch_overlay.journey_panel.close_button.click()
            players = self.open_players_list(market=market, market_name=market_name)
            self.assertTrue(players, msg='Players are not displayed on the Players List')
            first_player_name = list(players.keys())[0]
            last_player_name = list(players.keys())[-1]
            counter = 0
            for player_name, player in players.items():
                if player_name not in self.used_players:
                    # re-initializing player list because of StaleElement
                    if counter > 0:
                        players = self.open_players_list(market=market, market_name=market_name)
                        player = players.get(player_name)
                    try:
                        player.click()
                        self._logger.info(f'*** Selecting player "{player_name}" for market "{market_name}"')
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
                    player_card.add_player_button.click()
                    sleep(5)
                    self.assertFalse(five_a_side_tab.wait_for_players_card_closed(timeout=10),
                                     msg='Players card has not been closed')
                    self.assertTrue(market.added_player_name,
                                    msg=f'Failed to display added Player\'s Name "{player_name}"')
                    self.used_players.append(player_name)
                    self.__class__.current_player_name = player_name
                    if self.pitch_overlay.wait_for_error_message(timeout=5):
                        self._logger.info(
                            f'*** Encountered error "{self.pitch_overlay.error_message_text}", trying next player')
                        self.assertNotEqual(self.current_player_name, last_player_name,
                                            msg=f'No compatible players found for "{first_player_name}"')
                    else:
                        if market_name in ('To Be Carded', 'To Concede'):
                            expected_market_name = (
                                f'{market.added_player_name} {market.name}').split(' - ')[0]
                        elif 'Shots' in market_name:
                            expected_market_name = f'{market.added_player_name} To Have {market.name}'
                        else:
                            expected_market_name = f'{market.added_player_name} To Make {market.name}'
                        self.expected_players_list.append(expected_market_name)
                        break
                    counter += 1
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')

    def test_002_enter_stake_1_place_bet(self):
        """
        DESCRIPTION: Enter Stake: 1 & Place bet
        EXPECTED: On Bet Receipt Page:
        EXPECTED: Verify "Bet Placed Successfully" text
        EXPECTED: Verify "Your team has been entered into a 5-A-Side Leaderboard!"
        EXPECTED: Verify button "VIEW ENTRY"
        """
        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        wait_for_result(lambda: self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict is not None,
                        timeout=10)
        contest = self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(self.contest_name_1)
        if not contest.has_active_contest():
            contest.click()
        self.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(self.byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        self.byb_betslip_panel.place_bet.click()
        result = self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25)
        self.assertTrue(result, msg='5-A-Side Bet Receipt is not displayed')
        self.assertTrue(self.byb_betslip_panel.has_view_entry(timeout=10), msg='View Entry panel is displayed')
        wait_for_result(lambda: self.byb_betslip_panel.view_entry.view_entry_title is not None, timeout=10)
        self.assertEqual(self.byb_betslip_panel.view_entry.view_entry_title, vec.betslip.VIEW_ENTRY_TITLE,
                         msg=f'Actual title "{self.byb_betslip_panel.view_entry.view_entry_title}" is '
                             f'not same as Expected "{vec.betslip.VIEW_ENTRY_TITLE}"')
        successful_message = self.site.quick_bet_panel.bet_receipt.header.bet_placed_text
        self.assertEqual(successful_message, vec.betslip.SUCCESS_BET, msg=f'Actual message "{successful_message}" is not '
                                                                          f'same as Expected "{vec.betslip.SUCCESS_BET}"')

    def test_003_click_on_button_view_entry(self):
        """
        DESCRIPTION: Click on button "VIEW ENTRY"
        EXPECTED: User should be on Leaderboard
        """
        self.byb_betslip_panel.view_entry.view_entry_button.click()
        sleep(3)
        result = wait_for_result(lambda: self.site.five_A_side_leaderboard.is_displayed(),
                                 timeout=15,
                                 name='five a side leaderboard is displayed')
        self.assertTrue(result, msg='five a side leaderboard is not displayed')

    def test_004_verify_contest_id_in_the_url(self):
        """
        DESCRIPTION: Verify Contest id in the URL
        EXPECTED: Contest id in the URL should be the same as in CMS
        """
        actual_contest_id = unquote(self.device.get_current_url())
        contest_id = self.contest1['id']
        self.assertIn(contest_id, actual_contest_id, msg=f'Actual contest id "{actual_contest_id}" '
                                                         f'is not same as Expected "{contest_id}"')

    def test_005_verify_leaderboard_ui_elements(self):
        """
        DESCRIPTION: Verify Leaderboard UI elements
        EXPECTED: Verify Team1 name, Team2 name
        EXPECTED: Verify 5-A-Side logo
        EXPECTED: Verify header "5-A-SIDE LEADERBOARD"
        EXPECTED: Verify <Maximum {Teams} entries per user (1/{Teams})>
        EXPECTED: Verify <Maximum {Size} total entries (1/{Size})>
        """
        leaderboard = self.site.five_A_side_leaderboard
        self.assertTrue(leaderboard.home_team_name.is_displayed(),
                        msg='"Home team" name is not displayed')
        self.assertTrue(leaderboard.away_team_name.is_displayed(),
                        msg='"Away team" name is not displayed')
        self.assertTrue(leaderboard.terms_rules_header.is_displayed(),
                        msg='"5-A-Leaderboard" header is not displayed')
        self.assertTrue(leaderboard.entries_per_user.is_displayed(),
                        msg='"Maximun entries per user" is not displayed')
        self.assertTrue(leaderboard.total_entries.is_displayed(),
                        msg='"Total entries" is not displayed')
