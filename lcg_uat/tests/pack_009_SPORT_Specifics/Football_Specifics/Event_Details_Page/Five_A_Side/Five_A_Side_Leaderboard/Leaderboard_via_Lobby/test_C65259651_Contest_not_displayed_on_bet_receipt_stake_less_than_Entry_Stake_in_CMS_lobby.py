import pytest
import tests
import time
from selenium.common.exceptions import ElementClickInterceptedException
from datetime import datetime
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.five_a_side_leaderboard_reg_tests
@pytest.mark.five_a_side
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
class Test_C65259651_Verify_the_contest_is_not_displayed_on_bet_receipt_if_stake_amount_is_less_than_Entry_Stake_in_CMS_lobby(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65259651
    NAME: Verify the contest is not displayed on bet receipt if stake amount is less than Entry Stake in CMS lobby
    DESCRIPTION: Verify the contest is not displayed on bet receipt if stake amount is less than Entry Stake in CMS lobby
    PRECONDITIONS: In CMS, quick link should be configured for Lobby
    PRECONDITIONS: Homepage> Quick Links > Create Sports Quick Link.
    PRECONDITIONS: Title: {title} e.g.: Beta2 Lobby
    PRECONDITIONS: Destination: https://beta2-sports.ladbrokes.com/5-a-side/lobby
    PRECONDITIONS: Below contest should be created in CMS:
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 5
    PRECONDITIONS: Teams: 2
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Capture the Contest Id
    PRECONDITIONS: In Frontend: Click on the "LOBBY" from sports header
    PRECONDITIONS: Click on the contest created as per precondition
    PRECONDITIONS: Click on Build Team
    PRECONDITIONS: Capture the Contest Id
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}//5-a-side/lobby'
    created_lobby_submenu = None

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Shots Outside The Box',
            'Passes': 'Shots',
            'Assists': 'Passes',
            'Shots': 'Assists'
        },
        'Stats': {
            'To Concede': '1',
            'Tackles': '2',
            'Passes': '3',
            'Assists': '45',
            'Shots': '1'
        }
    }

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.created_lobby_submenu:
            cms_config = cls.get_cms_config()
            cms_config.delete_header_submenu(id=cls.created_lobby_submenu['id'])

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS, quick link should be configured for Lobby
        PRECONDITIONS: Homepage> Quick Links > Create Sports Quick Link.
        PRECONDITIONS: Title: {title} e.g.: Beta2 Lobby
        PRECONDITIONS: Destination: https://beta2-sports.ladbrokes.com/5-a-side/lobby
        PRECONDITIONS: Below contest should be created in CMS:
        PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
        PRECONDITIONS: Stake: 1
        PRECONDITIONS: Event: {event id}
        PRECONDITIONS: Size: 5
        PRECONDITIONS: Teams: 1
        PRECONDITIONS: User's Allowed: Test Account
        DESCRIPTION: User is logged in and on Football event details page:
        DESCRIPTION: - '5 A Side' sub tab (event type specified above):
        DESCRIPTION: - 'Build a team' button (pitch view)
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        quick_link_title = 'AutoLobby' + '_C65259651'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from)
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
        contest_name = f"Auto test " + event_name + "_" + str(event_id) + "_" + 'C65259651'
        self.cms_config.create_five_a_side_show_down(contest_name=contest_name,
                                                     entryStake=self.stake_value, size="5", teams="1",
                                                     event_id=event_id, display=True)
        self.site.login()
        if self.device_type == 'mobile':
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(quick_link_title, list(quick_links.keys()),
                          msg=f'Can not find "{quick_link_title}" in "{list(quick_links.keys())}"')
            quick_links.get(quick_link_title).click()
        else:
            header_submenus = self.cms_config.get_header_submenus()
            is_lobby_available = any([header['linkTitle'].upper() == "lobby".upper() for header in header_submenus])
            if not is_lobby_available:
                self.__class__.created_lobby_submenu = self.cms_config.create_header_submenu(name="LOBBY",
                                                        target_url="https://beta-sports.ladbrokes.com/5-a-side/lobby")
                wait_for_haul(3)
                self.device.refresh_page()
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()

        self.site.wait_content_state_changed(timeout=20)
        sleep(5)
        self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(contest_name).click()
        self.site.wait_content_state_changed(timeout=20)
        self.site.five_A_side_leaderboard.build_btn.click()
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get(self.Test['Combination']).click()

    def test_001_Select_all_players_for_5_A_Side_formation(self):
        """
        DESCRIPTION: Select all players for 5-A-Side formation
        EXPECTED: - On Betslip page (Before placing bet):
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

    def test_002_Enter_Stake_0_9_Place_bet(self):
        """
        DESCRIPTION: Enter Stake: 0.9 & Place bet
        EXPECTED: - On Bet Receipt Page: The message '✓Bet Placed Successfully'
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
        contest_header = byb_betslip_panel.select_your_leaderboard.contest_header.text
        self.assertTrue(contest_header, msg='"ContestHeader" is not available')
        contests = byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict
        self.assertTrue(contests, msg='"Contests" are not available')
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=0.9)
        self.assertTrue(byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')

    def test_003_On_the_betreceipt_verify_for_leaderboard_page(self):
        """
        DESCRIPTION: On the betreceipt, verify for leaderboard page
        EXPECTED: - On Bet Receipt Page: Leaderboard or View Entry" button should not be displayed
        """
        bet_receipt_view_entry = self.site.byb_bet_receipt_panel.has_view_entry()
        self.assertFalse(bet_receipt_view_entry,
                         msg='"View entry" button is displayed')
