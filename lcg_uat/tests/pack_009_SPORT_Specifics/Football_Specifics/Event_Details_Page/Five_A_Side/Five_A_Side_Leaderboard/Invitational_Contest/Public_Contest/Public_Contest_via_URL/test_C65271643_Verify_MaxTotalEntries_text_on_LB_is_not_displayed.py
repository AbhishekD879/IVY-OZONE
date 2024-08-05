import pytest
import tests
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
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
class Test_C65271643_Verify_Maximum_Total_Entries_text_on_Leaderboard_is_not_displayed_if_Size_entry_is_empty_in_CMS_public_Contest(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65271643
    NAME: Verify MAXIMUM TOTAL ENTRIES text on Leaderboard is not displayed if Size entry is empty in CMS - Public Contest
    DESCRIPTION: Verify MAXIMUM TOTAL ENTRIES text on Leaderboard is not displayed if Size entry is empty in CMS - Public Contest
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: {blank}
    PRECONDITIONS: Teams: 2
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Invitational Contest : True
    PRECONDITIONS: Invitational Contest Display : Public (True)
    PRECONDITIONS: Capture the Contest Id
    PRECONDITIONS: In Fronend:
    PRECONDITIONS: Navigate to public contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id})
    PRECONDITIONS: by using contest-id or take the URL from Contest URL field in CMS
    PRECONDITIONS: Click on Build Team
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Tackles',
            'Passes': 'Passes',
            'Assists': 'Assists',
            'Shots': 'Shots'
        },
        'Stats': {
            'To Concede': '1',
            'Tackles': '5',
            'Passes': '15',
            'Assists': '1',
            'Shots': '25'
        }
    }

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Below contest should be created in CMS:
        PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
        PRECONDITIONS: Stake: 1
        PRECONDITIONS: Event: {event id}
        PRECONDITIONS: Size: {blank}
        PRECONDITIONS: Teams: 2
        PRECONDITIONS: User's Allowed: Test Account
        PRECONDITIONS: invitational Contest : True
        PRECONDITIONS: Invitational Contest Display : Private (True)
        PRECONDITIONS: Capture the Contest Id
        PRECONDITIONS: In Fronend:
        PRECONDITIONS: Navigate to private contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id})
        PRECONDITIONS: by using contest-id or take the URL from Contest URL field in CMS
        PRECONDITIONS: Click on Build Team
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
        contest_name = f"INV_Auto test " + event_name + "_" + str(event_id) + "_" + 'C65269130'
        contest_response = self.cms_config.create_five_a_side_show_down(contest_name=contest_name,
                                                                        entryStake=self.stake_value,
                                                                        teams="2",
                                                                        event_id=event_id, display=True,
                                                                        isInvitationalContest=True)
        get_contest = self.cms_config.get_five_a_side_show_down_contest(contest_response['id'])
        contest_id = get_contest['contestURL'].split('/')[-1]
        contest_url = f'https://{tests.HOSTNAME}/' + '5-a-side/leaderboard/' + contest_id
        self.site.login()
        self.device.navigate_to(url=contest_url, testautomation=True)
        self.site.wait_content_state_changed(timeout=20)
        sleep(6)
        self.site.five_A_side_leaderboard.build_btn.click()
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get(self.Test['Combination']).click()

    def test_001_Select_less_than_5_players_for_the_5_A_Side_formation(self):
        """
        DESCRIPTION: Select less than 5 players for the 5-A-Side formation
        EXPECTED: - Players are selected on Pitch view
        EXPECTED: - 'Place Bet' button becomes active
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

    def test_002_Enter_Stake_1_Place_bet(self):
        """
        DESCRIPTION: Enter Stake: 1 & Place bet
        EXPECTED: On Bet Receipt Page: The message '✓Bet Placed Successfully'
        EXPECTED: Verify "Your team has been entered into a 5-A-Side Leaderboard!"
        EXPECTED: Verify button "VIEW ENTRY"
        """
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        sleep(2)
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        if not self.is_safari:
            self.get_web_socket_response(self.response_50001)
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

        byb_betslip_panel = self.site.byb_betslip_panel
        contest_header = byb_betslip_panel.select_your_leaderboard.contest_header.text
        self.assertTrue(contest_header, msg='"ContestHeader" is not available')
        contests = byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict
        self.assertTrue(contests, msg='"Contests" are not available')
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        wait_for_result(lambda: self.site.byb_bet_receipt_panel.view_entry.view_entry_button.is_displayed(), timeout=10,
                        name='leaderboard page is not displayed')
        sleep(2)

    def test_003_Click_on_button_VIEW_ENTRY_(self):
        """
        DESCRIPTION: Click on button "VIEW ENTRY"
        EXPECTED: - User should be on Leaderboard
        """
        self.site.byb_bet_receipt_panel.view_entry.view_entry_button.click()
        sleep(2)
        wait_for_result(lambda: self.site.five_A_side_leaderboard.is_displayed(),
                        timeout=10,
                        name='five a side leaderboard is displayed')

    def test_004_Verify_button_BUILD_ANOTHER_TEAM_and_is_enabled(self):
        """
        DESCRIPTION: Verify button BUILD ANOTHER TEAM" and is enabled
        EXPECTED: Verify Team1 name, Team2 name
        EXPECTED: Verify 5-A-Side logo
        EXPECTED: Verify header "5-A-SIDE LEADERBOARD"
        EXPECTED: Verify <Maximum {Teams} entries per user (1/{Teams})> should not be available
        EXPECTED: Verify button BUILD ANOTHER TEAM". Button should be enabled
        EXPECTED: Verify link ""RETURN TO LOBBY"" presence"
        """
        self.assertTrue(self.site.five_A_side_leaderboard.home_team_name.is_displayed(),
                        msg='"Home team" name is not displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.away_team_name.is_displayed(),
                        msg='"Away team" name is not displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.terms_rules_header.is_displayed(),
                        msg='"5-A-SIDE LEADERBOARD" header not displayed')
        self.assertFalse(self.site.five_A_side_leaderboard.total_entries.is_displayed(),
                         msg='Maximum {teams} total entries (1/{teams})" Link Displayed')
        build_another_team = self.site.five_A_side_leaderboard.build_btn.text
        self.assertEqual(build_another_team, 'BUILD ANOTHER TEAM',
                         msg=f'actual text {build_another_team} is not same as Expected text "BUILD ANOTHER TEAM"')
        self.assertTrue(self.site.five_A_side_leaderboard.return_to_lobby.is_displayed(),
                        msg='"RETURN TO LOBBY" Link Not Displayed')

    def test_005_verify_Maximum_Size_total_entries_1_Size(self):
        """
        DESCRIPTION: Verify <Maximum {size} total entries (1/{size}) should not be available
        EXPECTED: <Maximum {Size} total entries (1/{Size})> should not be available
        """
        self.assertFalse(self.site.five_A_side_leaderboard.total_entries.is_displayed(),
                         msg='Maximum {size} total entries (1/{Size})" Link Displayed')
