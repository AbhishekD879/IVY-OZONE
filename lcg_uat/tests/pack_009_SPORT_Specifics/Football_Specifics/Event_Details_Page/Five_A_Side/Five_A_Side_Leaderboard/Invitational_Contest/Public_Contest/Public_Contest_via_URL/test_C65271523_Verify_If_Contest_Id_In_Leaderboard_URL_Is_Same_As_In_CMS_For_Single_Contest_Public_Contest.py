import pytest
import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep, time
from voltron.utils.waiters import wait_for_result


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
class Test_C65271523_Verify_If_Contest_Id_In_Leaderboard_URL_Is_Same_As_In_CMS_For_Single_Contest_Public_Contest(BaseFiveASide):
    """
    TR_ID: C65271523
    NAME: Verify if Contest Id in Leaderboard URL is same as in CMS for Single Contest - Public Contest
    DESCRIPTION: Test case Verify if Contest Id in Leaderboard URL is same as in CMS for Single Contest - Public Contest
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 2
    PRECONDITIONS: Teams: 1
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Invitational Contest : True
    PRECONDITIONS: Invitational Contest Display : Public (True)
    PRECONDITIONS: Capture the Contest Id
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Assists',
            'Passes': 'Goals',
            'Assists': 'Goals Inside The Box',
            'Shots': 'Passes'
        },
        'Stats': {
            'To Concede': '1',
            'Tackles': '1',
            'Passes': '2',
            'Assists': '1',
            'Shots': '25'
        }
    }

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
        self.__class__.contest_name = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(round(time()))
        self.__class__.response_id = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                                                  entryStake=self.stake_value, size="2",
                                                                                  teams="1",
                                                                                  event_id=event_id, display=True,isInvitationalContest=True)['id']
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
        formation_carousel.get(self.Test['Combination']).click()

    def test_001_select_all_players_for_5_a_side_formation(self):
        """
        DESCRIPTION: Select all players for 5-A-Side formation
        EXPECTED: - Players are selected on Pitch view
        EXPECTED: - 'Place Bet' button becomes active
        """
        tab_content = self.site.sport_event_details.tab_content
        expected_players_list = []
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
                    expected_players_list.append(expected_market_name)
                    break
        self._logger.info('############### Data Set used in this test ###############')
        print(expected_players_list)

    def test_002_click_tap_place_bet_button(self):
        """
        DESCRIPTION: Click/Tap 'Place Bet' button
        EXPECTED: - Title of the Banach Betslip is '5-A-Side Betslip'
        """
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')

    def test_003_enter_any_value_into_the_stake_field_and_click_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter any value into the 'Stake' field and click/tap 'Place bet' button
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - Verify "Your team has been entered into a 5-A-Side Leaderboard!"
        EXPECTED: - Verify button "VIEW ENTRY"
        """
        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(self.byb_betslip_panel.select_your_leaderboard.contest_header.is_displayed(),
                        msg='leaderboard is not displayed')
        self.assertIn(self.contest_name,
                      self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.keys(),
                      msg=f'{self.contest_name} is not in leaderboard keys {self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.keys()} ')
        if not self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
                self.contest_name).has_active_contest:
            self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict[self.contest_name].click()
        self.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(self.byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        self.byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.assertTrue(self.byb_betslip_panel.view_entry.is_displayed(), msg='View Entry panel is not displayed')

    def test_004_click_on_view_entry_button_and_verify_leaderboard_url(self):
        """
        DESCRIPTION: Click on button "VIEW ENTRY"  and  Verify Contest Id in the URL
        EXPECTED: - User should be on Leaderboard
        EXPECTED: - Contest Id in the URL should be the same as in CMS
        """
        wait_for_result(lambda: self.byb_betslip_panel.view_entry.view_entry_button.is_displayed(),
                        timeout=5,
                        name='VIEW ENTRY button text to appear')
        self.byb_betslip_panel.view_entry.view_entry_button.click()
        sleep(2)
        wait_for_result(lambda: self.site.five_A_side_leaderboard.is_displayed(),
                        timeout=5,
                        name='five a side leaderboard is displayed')
        self.assertIn(self.response_id, self.device.get_current_url(),
                      msg=f'{self.response_id} contest id not in leaderboard url {self.device.get_current_url()}')
