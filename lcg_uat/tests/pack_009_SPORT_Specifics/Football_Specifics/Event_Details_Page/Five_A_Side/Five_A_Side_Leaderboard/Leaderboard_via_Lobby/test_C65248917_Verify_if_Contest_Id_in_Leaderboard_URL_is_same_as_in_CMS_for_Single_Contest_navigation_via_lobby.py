import pytest
import time

from crlat_cms_client.utils.date_time import get_date_time_as_string

import tests
from tests.base_test import vtest
from datetime import datetime
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from time import sleep
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
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
class Test_C65248917_Verify_if_Contest_Id_in_Leaderboard_URL_is_same_as_in_CMS_for_Single_Contest_navigation_via_lobby(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65248917
    NAME: Verify if Contest Id in Leaderboard URL is same as in CMS for Single Contest  - navigation via lobby
    DESCRIPTION: Verify if Contest Id in Leaderboard URL is same as in CMS for Single Contest  - navigation via lobby
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 2
    PRECONDITIONS: Teams: 1
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}//5-a-side/lobby'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 5
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: User is logged in and on Football event details page:
        DESCRIPTION: - '5 A Side' sub tab (event type specified above):
        DESCRIPTION: - 'Build a team' button (pitch view)
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        quick_link_title = 'Autotest Beta2 Lobby' + '_C65248917'
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                            days=-1,
                                            minutes=-1)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                          days=3)[:-3] + 'Z'
        self.cms_config.create_quick_link(title=quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from, date_to=date_to)
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        market_name = vec.yourcall.MARKETS.player_bets
        event_name = normalize_name(event_resp[0]['event']['name'])
        event_start_time = event_resp[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=time_format,
            ss_data=True)
        self.__class__.full_event_name = f'{event_name} {self.event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{self.full_event_name}" with market name "{market_name}", '
            f'event id "{event_name}", event start time "{self.event_start_time_local}"')
        self.__class__.contest_name_1 = f"Auto test " + event_name + " " + "(" + str(event_id) + ")_8917"
        self.__class__.contest1 = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name_1,
                                                                               entryStake="1", size="5", teams="2",
                                                                               event_id=event_id, display=True)
        self.site.login()
        if self.device_type == 'mobile':
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(quick_link_title, list(quick_links.keys()),
                          msg=f'Can not find "{quick_link_title}" in "{list(quick_links.keys())}"')
            quick_links.get(quick_link_title).click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()

        self.site.wait_content_state_changed(timeout=20)
        sleep(3)
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(self.contest_name_1)
        section.click()
        self.site.five_A_side_leaderboard.build_btn.click()
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
            self.__class__.first_player_name = list(players.keys())[0]
            self.__class__.last_player_name = list(players.keys())[-1]
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
                        self.assertNotEqual(self.current_player_name, self.last_player_name,
                                            msg=f'No compatible players found for "{self.first_player_name}"')
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
        if not self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.get(
                self.contest_name_1).has_active_contest:
            self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict[self.contest_name_1].click()
        self.__class__.betslip_odds = self.byb_betslip_panel.selection.content.odds
        self.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(self.byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        self.byb_betslip_panel.place_bet.click()
        a = self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25)
        self.assertTrue(a,
                        msg='5-A-Side Bet Receipt is not displayed')
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
        result = wait_for_result(lambda: self.site.five_A_side_leaderboard.is_displayed(),
                                 timeout=15,
                                 name='five a side leaderboard is displayed')
        self.assertTrue(result, msg='five a side leaderboard is not displayed')

    def test_004_verify_contest_id_in_the_url(self):
        """
        DESCRIPTION: Verify Contest id in the URL
        EXPECTED: Contest id in the URL should be the same as in CMS
        """
        actual_contest_id = self.device.get_current_url()
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
        EXPECTED: Maximum 2 total entries (1/2)
        EXPECTED: Verify button "MAX ENTRIES REACHED (1/1)"
        EXPECTED: Verify link "RETURN TO LOBBY" presence
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
        self.assertTrue(leaderboard.build_btn.is_displayed(),
                        msg='"MAXIMUM ENTRIES REACHED(1/1)" button is not displayed')
        self.assertTrue(leaderboard.return_to_lobby.is_displayed(),
                        msg='"Return to lobby" link is not displayed')
        actual_message = leaderboard.build_btn.text
        self.assertEqual(actual_message, 'BUILD ANOTHER TEAM',
                         msg=f'Actual message: "{actual_message}" is not same as Expected message: "BUILD ANOTHER TEAM"')
