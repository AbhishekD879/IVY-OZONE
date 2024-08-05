import pytest
import tests
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from time import sleep, time
from tests.base_test import vtest
from selenium.common.exceptions import ElementClickInterceptedException
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from urllib.parse import quote
from voltron.utils.waiters import wait_for_result, wait_for_haul


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
@pytest.mark.five_a_side_url_fix
@pytest.mark.cms
@pytest.mark.banach
@pytest.mark.reg156_fix
@pytest.mark.reg157_fix
@vtest
class test_C65271589_Verify_CONTEST_FULL_button_on_Leaderboard_for_a_single_contest_and_Size_entry_as_1_in_CMS_public_contest(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65271589
    NAME: Verify CONTEST FULL button on Leaderboard for a single contest and Size entry as 1 in CMS - Public contest via lobby
    DESCRIPTION: This testcase Verifies CONTEST FULL button on Leaderboard for a single contest and Size entry as 1 in CMS - Public contest via lobby
    """
    keep_browser_open = True
    stake_value = 1
    proxy = None
    sport_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/5-a-side/lobby'
    size = 1
    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Passes',
            'Passes': 'Shots Outside The Box',
            'Assists': 'Goals',
            'Shots': 'Shots'
        },
        'Stats': {
            'To Concede': '1',
            'Tackles': '35',
            'Passes': '1',
            'Assists': '1',
            'Shots': '2'
        }
    }

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS, quick link should be configured for Lobby
        PRECONDITIONS: Homepage> Quick Links > Create Sports Quick Link.
        PRECONDITIONS: Homepage> Quick Links > Create Sports Quick Link.
        PRECONDITIONS: Destination: https://beta2-sports.ladbrokes.com/5-a-side/lobby
        PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
        PRECONDITIONS: Stake: 1
        PRECONDITIONS: Event: {event id}
        PRECONDITIONS: Size: 1
        PRECONDITIONS: Teams: {blank}
        PRECONDITIONS: User's Allowed: Test Account
        PRECONDITIONS: In Fronend:
        PRECONDITIONS: Click on the ""LOBBY"" from sports header
        PRECONDITIONS: Click on the contest created as per precondition
        PRECONDITIONS: Click on Build Team
        PRECONDITIONS: Capture the Contest Id"
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
            wait_for_haul(10)
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
        response_id = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                                   entryStake=self.stake_value, size=self.size,
                                                                   teams="",
                                                                   event_id=event_id, display=True,
                                                                   isInvitationalContest=True,
                                                                   isPrivateContest=False)['id']
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
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(self.contest_name)
        section.click()
        self.assertIn(quote(response_id), self.device.get_current_url(),
                      msg=f'{quote(response_id)} contest id not in leaderboard url {self.device.get_current_url()}')
        self.site.five_A_side_leaderboard.build_btn.click()
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get(self.Test['Combination']).click()

    def test_001_select_all_players_for_5_a_side_formation(self):
        """
        DESCRIPTION: Select all players for 5-A-Side formation
        EXPECTED: On Betslip page (Before placing bet):
        EXPECTED: Single contest should be available along with contest name
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
                        if not five_a_side_dailog:
                            try:
                                wait_for_haul(3)
                                if self.site.sport_event_details.tab_content.player_card:
                                    pass
                            except:
                                continue
                        else:
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
                    sleep(2)
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
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')

    def test_002_enter_Stake_1_Place_bet(self):
        """
        DESCRIPTION: Enter Stake: 1 & Place bet
        EXPECTED: On Bet Receipt Page:
        EXPECTED: The message '✓Bet Placed Successfully'
        EXPECTED: "Your team has been entered into a 5-A-Side Leaderboard!"
        EXPECTED: "VIEW ENTRY" Button is displayed.
        """
        byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest_header.is_displayed(),
                        msg='leaderboard is not displayed')
        self.assertIn(self.contest_name,
                      byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.keys(),
                      msg=f'{self.contest_name} is not in leaderboard keys {byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.keys()} ')
        if not byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
                self.contest_name).has_active_contest:
            byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict[self.contest_name].click()
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.assertTrue(byb_betslip_panel.view_entry.is_displayed(), msg='View Entry panel is not displayed')

    def test_003_click_on_button_VIEW_ENTRY(self):
        """
        DESCRIPTION: Click on button "VIEW ENTRY
        EXPECTED: User should be on Leaderboard
        """
        bet_receipt_view_entry = self.site.byb_bet_receipt_panel.view_entry
        bet_receipt_view_entry.view_entry_button.click()
        sleep(2)
        wait_for_result(lambda: self.site.five_A_side_leaderboard.is_displayed(),
                        timeout=5,
                        name='five a side leaderboard is displayed')

    def test_004_Verify_button_CONTEST_FULL_and_is_disabled(self):
        """
        DESCRIPTION: Verify button "CONTEST FULL" and is disabled
        DESCRIPTION: Verify <Maximum {Size} total entries (1/{Size}) should be displayed
        EXPECTED: Team1 name, Team2 name should be displayed.
        EXPECTED: 5-A-Side logo is displayed.
        EXPECTED: Header "5-A-SIDE LEADERBOARD" is displayed.
        EXPECTED: "CONTEST FULL" Button is disabled.
        EXPECTED: "RETURN TO LOBBY" is displayed.
        EXPECTED:  Verify <Maximum {Size} total entries (1/{Size})>
        """
        self.assertTrue(self.site.five_A_side_leaderboard.home_team_name.is_displayed(),
                        msg='"Home team" name is not displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.away_team_name.is_displayed(),
                        msg='"Away team" name is not displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.terms_rules_header.is_displayed(),
                        msg='"5-A-SIDE LEADERBOARD" header not displayed')
        context_full = self.site.five_A_side_leaderboard.build_btn.text
        self.assertEqual(context_full, 'CONTEST FULL',
                         msg=f'actual text {context_full} is not same as Expected text "CONTEST FULL"')
        self.assertTrue(self.site.five_A_side_leaderboard.return_to_lobby.is_displayed(),
                        msg='"RETURN TO LOBBY" Link Not Displayed')
        self.assertTrue(self.site.five_A_side_leaderboard.total_entries.is_displayed(),
                        msg=f'"Maximum {self.size} total entries (1/{self.size}" Link Not Displayed')
        actual_message = self.site.five_A_side_leaderboard.total_entries.text
        self.assertEqual(actual_message, vec.five_a_side.TOTAL_ENTRIES.format(s=1, n=self.size),
                         msg=f'Actual message: {actual_message} is not same as Expected message: {vec.five_a_side.TOTAL_ENTRIES.format(s=1, n=self.size)}')