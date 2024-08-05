import tests
import pytest
import time
from datetime import datetime
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide


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
class Test_C65268762_Verify_different_users_can_place_bets_until_Full_Contest_is_reached_navigation_via_lobby(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65268762
    NAME: Verify different users can place bets until Full Contest is reached - navigation via lobby
    DESCRIPTION: Verify different users can place bets until Full Contest is reached - navigation via lobby
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 1
    PRECONDITIONS: Teams: 1
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Capture the Contest Id
    """
    keep_browser_open = True
    proxy = None
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}//5-a-side/lobby'

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Passes',
            'Passes': 'Goals Outside The Box',
            'Assists': 'Goals',
            'Shots': 'Passes'
        },

        'Stats': {
            'To Concede': '1',
            'Tackles': '35',
            'Passes': '1',
            'Assists': '1',
            'Shots': '45'
        }
    }

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def navigate_to_event_details_page(self):
        if self.device_type == 'mobile':
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(self.quick_link_title, list(quick_links.keys()),
                          msg=f'Can not find "{self.quick_link_title}" in "{list(quick_links.keys())}"')
            quick_links.get(self.quick_link_title).click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()
        self.site.wait_content_state_changed(timeout=20)
        sleep(3)
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(self.contest_name)
        section.click()
        self.site.five_A_side_leaderboard.build_btn.click()
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get('BALANCED').click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 2
        DESCRIPTION: Teams: 1
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Capture the Contest Id
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_title = 'Autotest Beta2 Lobby' + '_C65268762'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from)
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        time_format = self.event_card_future_time_format_pattern
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)
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
            f'***Found Football event "{self.event_id}" "{full_event_name}" with market name "{market_name}", '
            f'event id "{event_name}", event start time "{event_start_time_local}"')
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        self.__class__.contest_name = f"Auto test " + "C65268762"
        self.__class__.response_id = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                                                  entryStake=self.stake_value, size="1",
                                                                                  teams="1",
                                                                                  event_id=self.event_id, display=True)['id']
        self.site.login(username=tests.settings.betplacement_user)
        if self.device_type == 'mobile':
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(self.quick_link_title, list(quick_links.keys()),
                          msg=f'Can not find "{self.quick_link_title}" in "{list(quick_links.keys())}"')
            quick_links.get(self.quick_link_title).click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()
        self.site.wait_content_state_changed(timeout=20)
        sleep(6)
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(self.contest_name)
        section.click()
        self.site.five_A_side_leaderboard.build_btn.click()
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get('BALANCED').click()

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: User is logged in
        """
        # Covered in above step

    def test_002_select_all_players_for_5_A_Side_formation(self):

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

    def test_003_enter_stake_1_and_place_bet(self):
        """
        DESCRIPTION: enter stake 1 and place bet
        EXPECTED: On Bet Receipt Page:
        EXPECTED: "Bet Placed Successfully" text is displayed
        EXPECTED: "Your team has been entered into a 5-A-Side Leaderboard!" is displayed
        EXPECTED: "VIEW ENTRY" button is displayed
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
        wait_for_result(lambda: self.byb_betslip_panel.view_entry.view_entry_button.is_displayed(),
                        timeout=5,
                        name='VIEW ENTRY button text to appear')
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(expected_result=False),
                         msg='Pitch overlay is shown')
        self.site.logout()

    def test_004_login_with_another_user(self):
        """
        DESCRIPTION: Login with another user
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_005_select_all_players_for_5_A_Side_formation(self):

        """
        DESCRIPTION: Select all players for 5-A-Side formation
        EXPECTED: On Betslip page (Before placing bet):
        EXPECTED: Contest should not be available
        """
        self.navigate_to_edp(event_id=self.event_id)
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
        self.test_002_select_all_players_for_5_A_Side_formation()
        has_contest = self.site.byb_betslip_panel.select_your_leaderboard.has_contest()
        if has_contest:
            contests_available = self.site.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict
            self.assertNotIn(self.contest_name, contests_available, msg='Contest is still available')
