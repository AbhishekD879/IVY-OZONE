import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod  # Ladbrokes Only
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.five_a_side_leaderboard
@vtest
class Test_C65233209_Verify_user_can_see_n_number_of_contests_on_betslip_as_created_in_CMS_for_an_event(BaseFiveASide,
                                                                                                        BaseSportTest):
    """
    TR_ID: C65233209
    NAME: Verify user can see n number of contests on betslip as created in CMS for an event
    DESCRIPTION: Verify user can see n number of contests on betslip as created in CMS for an event
    PRECONDITIONS: Create a two contests
    """
    keep_browser_open = True
    proxy = None

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Goals Inside The Box',
            'Passes': 'Shots',
            'Assists': 'To Be Carded',
            'Shots': 'Assists'
        },
        'Stats': {
            'To Concede': '1',
            'Tackles': '1',
            'Passes': '1',
            'Assists': 'Yes',
            'Shots': '1'
        }
    }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Contest1:
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 5
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Contest2:
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)_1
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 5
        DESCRIPTION: Teams: 2
        DESCRIPTION: User's Allowed: Test Account"
        """
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        market_name = vec.yourcall.MARKETS.player_bets
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
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
        # Creating contest
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        self.__class__.contest_names = []
        for i in range(1, 3):
            contest_name = f"Auto test multi-contest " + self.event_name + " " + str(i)
            self.cms_config.create_five_a_side_show_down(contest_name=contest_name, entryStake="0.10", size="1",
                                                         teams="1",
                                                         event_id=event_id)
            self.contest_names.append(contest_name)

        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.get_balance_by_page('all')
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')

    def test_001_Select_all_players_for_five_A_Side_formation(self):
        """
        DESCRIPTION: Select all players for 5-A-Side formation
        DESCRIPTION: Click on Place Bet"
        EXPECTED: On Betslip page (Before placing bet):
        EXPECTED: Both the contests should be available along with contest names"
        """
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.five_a_side),
                        msg=f'"{self.expected_market_tabs.five_a_side}" tab is not active')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')

        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_carousel.get(self.Test['Combination']).click()
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
                    sleep(2)
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
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        byb_betslip_panel = self.site.byb_betslip_panel
        contest_header = byb_betslip_panel.select_your_leaderboard.contest_header.text
        self.assertTrue(contest_header, msg='contest header is missing')
        self.assertTrue(byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict,
                        msg='Created contests are not appearing on Betslip')
        UI_contests = list(byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict.keys())
        count = 0
        for contest in self.contest_names:
            self.assertIn(contest, UI_contests,
                          msg=f'Created contest "{contest}" is not matching with UI contest "{sorted(UI_contests)}"')
            count = count + 1
        self.assertEqual(count, 2,
                         msg=f'Created contest "{sorted(self.contest_names)}" is not matching with UI contest "{sorted(UI_contests)}"')
