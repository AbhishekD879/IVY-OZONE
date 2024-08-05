import pytest
import tests
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
class Test_C65268919_Verify_CONTEST_FULL_button_on_Leaderboard_for_a_single_contest_and_Size_entry_as_1_in_CMS_Private_Contest(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65268919
    NAME: Verify CONTEST FULL button on Leaderboard for a single contest and Size entry as 1 in CMS-Private Contest
    DESCRIPTION: Verify CONTEST FULL button on Leaderboard for a single contest and Size entry as 1 in CMS-Private Contest
    PRECONDITIONS: Below contest should be created in CMS:
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {event id}
    PRECONDITIONS: Size: 1
    PRECONDITIONS: Teams: {blank}
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Invitational Contest : True
    PRECONDITIONS: Invitational Contest Display : Private (True)
    PRECONDITIONS: Capture the Contest Id
    PRECONDITIONS: In Fronend:
    PRECONDITIONS: Navigate to private contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id}) by using contest-id or take the URL from Contest URL
    PRECONDITIONS: field in CMS
    PRECONDITIONS: Click on Build Team
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Below contest should be created in CMS:
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 1
        DESCRIPTION: Teams: {blank}
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Invitational Contest : True
        DESCRIPTION: Invitational Contest Display : Private (True)
        DESCRIPTION: Capture the Contest Id
        DESCRIPTION: In Fronend:
        DESCRIPTION: Navigate to private contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id}) by using contest-id or take the URL from Contest URL
        DESCRIPTION: field in CMS
        DESCRIPTION: Click on Build Team
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
        self.__class__.contest_name = f"Auto test " + event_name + " " + "(" + str(event_id) + ")"
        contest_response = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name, isInvitationalContest=True,
                                                                        isPrivateContest=True, entryStake=self.stake_value, size="1",
                                                                        event_id=event_id, display=True)
        get_contest = self.cms_config.get_five_a_side_show_down_contest(contest_response['id'])
        self.__class__.contest_id = get_contest['contestURL'].split('/')[-1]
        contest_url = f'https://{tests.HOSTNAME}/' + '5-a-side/leaderboard/' + self.contest_id
        self.site.login()
        self.device.navigate_to(url=contest_url, testautomation=True)
        self.site.wait_content_state_changed(timeout=20)
        sleep(3)
        self.site.five_A_side_leaderboard.build_btn.click()
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
        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        contest_header = self.byb_betslip_panel.select_your_leaderboard.contest_header.text
        self.assertTrue(contest_header, msg='"ContestHeader" is not available')
        wait_for_result(
            lambda: self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict is not None,
            timeout=10)
        self.__class__.contests = self.byb_betslip_panel.select_your_leaderboard.contest.items_as_ordered_dict
        self.assertTrue(self.contests, msg='"Contests" are not available')

    def test_002_enter_stake_1_place_bet(self):
        """
        DESCRIPTION: Enter Stake: 1 & Place bet
        EXPECTED: On Bet Receipt Page:
        EXPECTED: Verify "Bet Placed Successfully" text
        EXPECTED: Verify "Your team has been entered into a 5-A-Side Leaderboard!"
        EXPECTED: Verify button "VIEW ENTRY"
        """
        contest = self.contests.get(self.contest_name)
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

    def test_004_verify_button_contest_full_and_is_disabled(self):
        """
        DESCRIPTION:  Verify button "CONTEST FULL" and is disabled
        EXPECTED: Verify button "CONTEST FULL". Button should be disabled
        """
        actual_contest_id = self.device.get_current_url()
        self.assertIn(self.contest_id, actual_contest_id, msg=f'Actual contest id "{actual_contest_id}" '
                                                              f'is not same as Expected "{self.contest_id}"')
        context_full = self.site.five_A_side_leaderboard.build_btn.text
        self.assertEqual(context_full, 'CONTEST FULL',
                         msg=f'actual text {context_full} is not same as Expected text "CONTEST FULL"')

    def test_005_verify_leaderboard_ui_elements(self):
        """
        DESCRIPTION: Verify <Maximum {Size} total entries (1/{Size}) should be displayed
        EXPECTED: Verify Team1 name, Team2 name
        EXPECTED: Verify 5-A-Side logo
        EXPECTED: Verify header "5-A-SIDE LEADERBOARD"
        EXPECTED: Verify <Maximum {Size} total entries (1/{Size})>
        EXPECTED: Verify link "RETURN TO LOBBY" presence
        """
        leaderboard = self.site.five_A_side_leaderboard
        self.assertTrue(leaderboard.home_team_name.is_displayed(),
                        msg='"Home team" name is not displayed')
        self.assertTrue(leaderboard.away_team_name.is_displayed(),
                        msg='"Away team" name is not displayed')
        self.assertTrue(leaderboard.terms_rules_header.is_displayed(),
                        msg='"5-A-Leaderboard" header is not displayed')
        self.assertTrue(leaderboard.total_entries.is_displayed(),
                        msg='"Total entries" is not displayed')
        self.assertTrue(leaderboard.return_to_lobby.is_displayed(),
                        msg='"Return to lobby" link is not displayed')
