import pytest
import tests
from time import sleep
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
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
class Test_C65233210_Verify_bet_placement_without_selecting_contest_on_Betslip_for_a_single_contest_created_in_CMS(BaseFiveASide):
    """
    TR_ID: C65233210
    NAME: Verify bet placement without selecting contest on Betslip for a single contest created in CMS
    DESCRIPTION: Verify bet placement without selecting contest on Betslip for a single contest created in CMS
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 2
    PRECONDITIONS: Teams: 1
    PRECONDITIONS: User's Allowed: Test Account
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 2
        DESCRIPTION: Teams: 1
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
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        self.__class__.contest_name = f"Auto test " + event_name + " " + "(" + str(event_id) + ")_3210"
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                     entryStake="0.10", size="2", teams="1",
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
        expected_players_list = []
        self.__class__.pitch_overlay = tab_content.pitch_overlay.content
        markets = self.pitch_overlay.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        used_players = []
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
                if player_name not in used_players:
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
                    used_players.append(player_name)
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
                        expected_players_list.append(expected_market_name)
                        break
                    counter += 1
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')

    def test_002_dont_select_any_contest_on_betslip_add_stake_1_and_place_bet(self):
        """
        DESCRIPTION: Don't select any contest on betslip, add stake 1 and place bet
        EXPECTED: Bet should be placed and it should be normal 5-A-Side bet. Bet will
        EXPECTED: not be added to leaderboard
        """
        contest = list(self.site.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.values())[0]
        self.assertEqual(self.contest_name, contest.name, msg=f'Actual contest name "{contest.name}" is '
                                                              f'not same as Expected "{self.contest_name}"')
        contest.click()
        byb_betslip_panel = self.site.byb_betslip_panel
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.assertFalse(byb_betslip_panel.has_view_entry(expected_result=False), msg='View Entry panel is displayed')
