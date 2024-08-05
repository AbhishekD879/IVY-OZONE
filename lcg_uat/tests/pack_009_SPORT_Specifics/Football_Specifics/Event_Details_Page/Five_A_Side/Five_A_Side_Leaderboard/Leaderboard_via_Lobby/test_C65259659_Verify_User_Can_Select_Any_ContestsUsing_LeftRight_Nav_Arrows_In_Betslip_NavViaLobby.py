import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep, time
from crlat_ob_client.utils.date_time import get_date_time_as_string


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
@vtest
class Test_C65259659_Verify_User_Can_Select_Any_ContestsUsing_LeftRight_Nav_Arrows_In_Betslip_NavViaLobby(BaseFiveASide,
                                                                                                          BaseFeaturedTest):
    """
     TR_ID: C65259659
     NAME: 	Verify user can select any of the contests using left and right navigation arrows in betslip - navigation via lobby
     DESCRIPTION: This testcase verifies user can select any of the contests using left and right navigation arrows in betslip - navigation via lobby
     PRECONDITIONS: In CMS, quick link should be configured for Lobby, Homepage> Quick Links > Create Sports Quick Link.
     PRECONDITIONS: Title: {title} e.g.: Beta2 Lobby, Destination: https://beta2-sports.ladbrokes.com/5-a-side/lobby
     PRECONDITIONS: Below contest should be created in CMS:
     PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
     PRECONDITIONS: Stake: 1
     PRECONDITIONS: Event: {event id}
     PRECONDITIONS: Size: 5
     PRECONDITIONS: Teams: 2
     PRECONDITIONS: User's Allowed: Test Account
     PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
     PRECONDITIONS: Stake: 1
     PRECONDITIONS: Event: {event id}
     PRECONDITIONS: Size: 7
     PRECONDITIONS: Teams: 3
     PRECONDITIONS: User's Allowed: Test Account
     PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
     PRECONDITIONS: Stake: 1
     PRECONDITIONS: Event: {event id}
     PRECONDITIONS: Size: 10
     PRECONDITIONS: Teams: 2
     PRECONDITIONS: User's Allowed: Test Account
     PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
     PRECONDITIONS: Stake: 1
     PRECONDITIONS: Event: {event id}
     PRECONDITIONS: Size: 6
     PRECONDITIONS: Teams: 3
     PRECONDITIONS: User's Allowed: Test Account
    """
    keep_browser_open = True
    proxy = None
    device_name = tests.desktop_default
    maximized_browser = True
    stake_value = 1
    sport_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/5-a-side/lobby'

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
            'To Concede': '0',
            'Tackles': '1',
            'Passes': '25',
            'Assists': '1',
            'Shots': '1'
        }
    }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 5
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 7
        DESCRIPTION: Teams: 3
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 10
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 6
        DESCRIPTION: Teams: 3
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: User is logged in and on Football event details page:
        DESCRIPTION: - '5 A Side' sub tab (event type specified above):
        DESCRIPTION: - 'Build a team' button (pitch view)
        """
        self.__class__.quick_link_name = "Autotest_" + str(round(time()))
        if self.device_type != 'desktop':
            if not self.is_quick_links_enabled():
                raise CmsClientException('"Quick links" module is disabled')
            if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
                raise CmsClientException('"Quick links" module is disabled for homepage')
            now = datetime.now()
            time_format = '%Y-%m-%dT%H:%M:%S.%f'
            date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                days=-1,
                                                minutes=-1)[:-3] + 'Z'
            date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                              days=3)[:-3] + 'Z'
            self.cms_config.create_quick_link(title=self.quick_link_name,
                                              sport_id=self.sport_id.get('homepage'),
                                              destination=self.destination_url,
                                              date_from=date_from, date_to=date_to)
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
        self.__class__.contest_name1 = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(round(time()))
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name1,
                                                     entryStake=self.stake_value, size="5",
                                                     teams="2",
                                                     event_id=event_id, display=True)
        self.__class__.contest_name2 = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(round(time()))
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name2,
                                                     entryStake=self.stake_value, size="7",
                                                     teams="3",
                                                     event_id=event_id, display=True)
        self.__class__.contest_name3 = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(round(time()))
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name3,
                                                     entryStake=self.stake_value, size="10",
                                                     teams="2",
                                                     event_id=event_id, display=True)
        self.__class__.contest_name4 = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(round(time()))
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name4,
                                                     entryStake=self.stake_value, size="6",
                                                     teams="3",
                                                     event_id=event_id, display=True)
        self.site.login(username=tests.settings.betplacement_user)
        if self.device_type == 'mobile':
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(self.quick_link_name, list(quick_links.keys()),
                          msg=f'Can not find "{self.quick_link_name}" in "{list(quick_links.keys())}"')
            quick_links.get(self.quick_link_name).click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()

        self.site.wait_content_state_changed(timeout=20)
        sleep(6)
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(self.contest_name1)
        section.click()
        self.site.five_A_side_leaderboard.build_btn.click()
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get(self.Test['Combination']).click()

    def test_001_select_at_least_2_valid_players_on_pitch_view(self):
        """
        DESCRIPTION: Select all players for 5-A-Side formation
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

    def test_002_click_tap_place_bet_button(self):
        """
        DESCRIPTION: Click/Tap 'Place Bet' button
        DESCRIPTION: Verify the contests created for the event
        EXPECTED: - Title of the Banach Betslip is '5-A-Side Betslip'
        EXPECTED: All the contests should be available along with contest names
        EXPECTED: 1st contest should be selected by default
        EXPECTED: User can see left and right navigation arrows
        EXPECTED: User can click on left and right navigation arrows and select the intended contest
        """
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest_header.is_displayed(),
                        msg='leaderboard is not displayed')
        created_contests = [self.contest_name1, self.contest_name2, self.contest_name3, self.contest_name4]
        ui_contests = byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.keys()
        for contest in created_contests:
            self.assertIn(contest, ui_contests, msg=f'{contest} is not present in UI contexts {ui_contests}')
        self.assertTrue(list(byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.values())[0].has_active_contest, msg='first contest is selected')
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest.next_arrow.is_displayed(),
                        msg='next arrow is not displayed')
        byb_betslip_panel.select_your_leaderboard.contest.next_arrow.click()
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest.prev_arrow.is_displayed(),
                        msg='prev arrow is not displayed')
        if byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
                self.contest_name3).active_contest is None:
            byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict[self.contest_name3].click()
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
            self.contest_name3).active_contest.is_displayed(), msg='contest3 is not selected')
        byb_betslip_panel.select_your_leaderboard.contest.prev_arrow.click()
        if byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
                self.contest_name2).active_contest is None:
            byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict[self.contest_name2].click()
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
            self.contest_name2).active_contest.is_displayed(), msg='contest2 is not selected')
