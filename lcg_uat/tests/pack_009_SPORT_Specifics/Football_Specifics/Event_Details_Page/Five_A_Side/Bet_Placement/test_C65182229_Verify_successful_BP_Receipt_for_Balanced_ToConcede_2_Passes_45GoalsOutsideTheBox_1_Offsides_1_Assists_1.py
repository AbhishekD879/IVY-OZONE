import pytest
import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from time import sleep


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.bet_placements
@pytest.mark.event_details
@pytest.mark.login
@pytest.mark.five_a_side_combinations
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@vtest
class Test_C65182229_Verify_successful_Bet_Placement_and_Receipt_for_Balanced_ToConcede_2_Passes_45GoalsOutsideTheBox_1_Offsides_1_Assists_1(BaseFiveASide):
    """
    TR_ID: C65182229
    NAME: 	Verify successful Bet Placement and Receipt for Balanced - To Concede-1 Passes-35 Goals Outside The Box-1 Goals Inside The Box-1 Shots Outside The Box-1
    DESCRIPTION: Test case verifies successful Banach bet placement and Bet receipt.
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Story: https://jira.egalacoral.com/browse/BMA-49310
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    """
    keep_browser_open = True
    proxy = None

    Test = {
        'Combination': 'BALANCED',
        'Market': {
            'To Concede': 'To Concede',
            'Tackles': 'Passes',
            'Passes': 'Goals Outside The Box',
            'Assists': 'Offsides',
            'Shots': 'Assists'
        },
        'Stats': {
            'To Concede': '1',
            'Tackles': '45',
            'Passes': '1',
            'Assists': '1',
            'Shots': '1'
        }
    }

    def test_000_preconditions(self):
        """
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
        self.__class__.full_event_name = f'{event_name} {event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{self.full_event_name}" with market name "{market_name}", '
            f'event id "{event_name}", event start time "{event_start_time_local}"')
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.get_balance_by_page('all')
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

    def test_001_select_at_least_2_valid_players_on_pitch_view(self):
        """
        DESCRIPTION: Select at least 2 valid players on Pitch view
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
                        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(), msg='Player Card is not shown')
                    except VoltronException:
                        # Handling <Player cannot Be Selected> dialog
                        five_a_side_dailog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_5ASIDE_PLAYER_NOT_SELECTED,
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
                    self.site.sport_event_details.tab_content.player_card.items_as_ordered_dict[self.Test['Market'][market_name]].click()

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
                            self.assertTrue(update_player_btn, msg='Update player button is not present in player cards')
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
        EXPECTED: - Banach Betslip appears at the bottom of the page on top of pitch view
        EXPECTED: - 'remotebetslip' request is triggered in WS
        EXPECTED: - Title of the Banach Betslip is '5-A-Side Betslip'
        EXPECTED: - '5-A-Side' logo is present
        """
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        if not self.is_safari:
            self.get_web_socket_response(self.response_50001)
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

    def test_003_enter_any_value_into_the_stake_field_and_click_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter any value into the 'Stake' field and click/tap 'Place bet' button
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - User Balance is updated
        EXPECTED: - Bet Placement details: WS code "51101"
        EXPECTED: *Note*: if we receive 'Connection timeout' in websocket: (51102) from Banach, bet is not placed at 1st time, thus try several times to place a bet.
        """
        byb_betslip_panel = self.site.byb_betslip_panel
        self.__class__.betslip_odds = byb_betslip_panel.selection.content.odds
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.assertTrue(byb_betslip_panel.place_bet.is_enabled(),
                        msg='Place bet button is disabled')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.verify_user_balance(expected_user_balance=self.user_balance - self.stake_value)

    def test_004_verify_channel_used_for_5_a_side_bets(self):
        """
        DESCRIPTION: Verify channel used for 5-A-Side bets
        EXPECTED: Channel: "f" is present in '50011' request in 'remotebetslip' websocket
        """
        if not self.is_safari:
            response_50011 = self.get_web_socket_response(self.response_50011)
            self.assertTrue(response_50011, msg=f'Response with frame ID #"{self.response_50011}" not received')
            response_channel = response_50011.get('channel')
            self.assertIsNotNone(response_channel,
                                 msg="Response channel is absent in '50011' request in 'remotebetslip' websocket")
            self.assertEqual('f', response_channel,
                             msg=f"Channel in '50011' request in 'remotebetslip' websocket does not equal 'f' and is '{response_channel}' instead")
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

    def test_005_verify_bet_receipt_on_ui(self):
        """
        DESCRIPTION: Verify Bet receipt on UI
        EXPECTED: - Main Header: 'Bet receipt' title with 'X' button
        EXPECTED: - Sub header : Tick icon, 'Bet Placed Successfully' text, date & time stamp (in the next format: i.e. 19/09/2019, 14:57)
        EXPECTED: - Block of Bet Type Summary:
        EXPECTED: - Win Alerts Toggle (if enabled in CMS)
        EXPECTED: - bet type name: i.e. 5-A-Side
        EXPECTED: - price of bet : e.g @90/1
        EXPECTED: - Bet ID:( Coral )/Receipt No:( Ladbrokes ) e.g Bet ID: 0/17781521/0000041
        EXPECTED: For each selection:
        EXPECTED: - selection name and market in the format of X.X To Make X+ Passes
        EXPECTED: Footer:
        EXPECTED: - 'Total stake'( Coral ) / 'Stake for this bet' ( Ladbrokes )
        EXPECTED: - 'Est. returns'( Coral ) / 'Potential returns' ( Ladbrokes )
        EXPECTED: - '5-A-Side Bet Receipt' title is shown in the bet receipt header
        EXPECTED: - '5-A-Side' logo can be seen in the bet receipt header (from 104)
        """
        self.assertEqual(vec.yourcall.FIVE_A_SIDE_BETRECEIPT_TITLE, self.site.byb_bet_receipt_panel.header.title,
                         msg=f'Bet receipt header title does not equal "{vec.yourcall.FIVE_A_SIDE_BETRECEIPT_TITLE}" '
                             f'and is "{self.site.byb_bet_receipt_panel.header.title}" instead')
        self.assertTrue(self.site.byb_bet_receipt_panel.header.has_close_button(),
                        msg='Bet Receipt header does not have "Close" button')
        bet_receipt_header = self.site.byb_bet_receipt_panel.bet_receipt.header
        self.assertEqual(bet_receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt_header.bet_placed_text}" is not equal to expected '
                             f'"{vec.betslip.SUCCESS_BET}"')
        self.assertRegex(bet_receipt_header.receipt_datetime, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet receipt data and time: "{bet_receipt_header.receipt_datetime}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        bet_receipt_selection = self.site.byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No selection found in 5-A-Side receipt')
        # expected_players_list = [item.lower() for item in self.expected_players_list]
        # selection_keys = [item.title().lower() for item in list(selections.keys())]
        # self.assertListEqual(selection_keys, expected_players_list,
        #                      msg=f'Incorrect market names.\nActual list: {selection_keys}'
        #                          f'\nExpected list: {expected_players_list}')
        self.assertEqual(bet_receipt_content.odds, self.betslip_odds, msg=f'Odds value on bet receipt '
                                                                          f'"{bet_receipt_content.odds}" is not the '
                                                                          f'same as on bet slip "{self.betslip_odds}"')
        self.assertEqual(bet_receipt_content.type_name.text, vec.bet_history.FIVE_A_SIDE_BET_TYPE_NAME,
                         msg=f'Bet type name is not "{vec.bet_history.FIVE_A_SIDE_BET_TYPE_NAME}" and is '
                             f'"{bet_receipt_content.type_name.text}" instead')
        self.assertEqual(bet_receipt_content.bet_id_label, vec.betslip.BET_ID,
                         msg=f'Bet id label text is: "{bet_receipt_content.bet_id_label}" '
                             f'expecting "{vec.betslip.BET_ID}"')
        self.assertTrue(bet_receipt_content.bet_id_value, msg='Bet ID value not found')
        self.assertEqual(bet_receipt_selection.total_stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg=f'Total Stake label text is: "{bet_receipt_selection.total_stake_label}", '
                             f'instead of "{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}"')
        self.assertEqual(float(bet_receipt_selection.total_stake_value), self.stake_value,
                         msg=f'Actual Total Stake value: "{float(bet_receipt_selection.total_stake_value)}" '
                             f'not match with expected: "{self.stake_value}"')
        self.assertEqual(bet_receipt_selection.total_est_returns_label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Total Est. Returns label text is: "{bet_receipt_selection.total_est_returns_label}", '
                             f'instead of "{vec.bet_history.TOTAL_RETURN}"')
        est_returns = bet_receipt_selection.total_est_returns_value
        self.assertTrue(est_returns, msg='Total Est. Returns value not found')
        # todo VOL-6308 add verification for '5-A-Side' logo can be seen in the bet receipt header

    def test_006_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet Receipt
        EXPECTED: - Bet Receipt is closed together with pitch view
        EXPECTED: - User is on '5 A Side' tab on EDP
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(expected_result=False),
                         msg='Pitch overlay is shown')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.five_a_side),
                        msg=f'"{self.expected_market_tabs.five_a_side}" tab is not active')

    def test_007_navigate_to_my_bets_open__settled(self):
        """
        DESCRIPTION: Navigate to My Bets (Open & Settled)
        EXPECTED: '5 A Side' logo is present 5-A-Side as signposting on the bet (from OX104)
        """
        # TODO uncomment from OX104 (VOL-6308)
        # self.site.open_my_bets_open_bets()
        # _, single_byb_section = \
        #     self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.FIVE_A_SIDE_BET_TYPE,
        #                                                           event_names=self.full_event_name,
        #                                                           number_of_bets=1)
