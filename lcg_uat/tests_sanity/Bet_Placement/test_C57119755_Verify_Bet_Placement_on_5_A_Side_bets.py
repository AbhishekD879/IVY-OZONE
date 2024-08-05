import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2  # Ladbrokes Only
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.banach
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@pytest.mark.sanity
@vtest
class Test_C57119755_Verify_Bet_Placement_on_5_A_Side_bets(BaseFiveASide):
    """
    TR_ID: C57119755
    NAME: Verify Bet Placement on '5-A-Side' bets
    DESCRIPTION: This test case verifies bet placement on '5-A-Side' bets
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on the 'Build Team' button on '5-A-Side' launcher
    PRECONDITIONS: 5. Make sure that '5-A-Side' overlay is opened
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - '5-A-Side' tab is created in CMS > EDP Markets
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Statistic is mapped for the particular event. Use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91089483#OPTA/BWINScoreboardmappingtoanOBevent-Appendix_A
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId':
    PRECONDITIONS: ![](index.php?/attachments/get/73440082)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    """
    keep_browser_open = True
    proxy = None
    enable_bs_performance_log = True

    # For future reference ..
    # def convert_outcome_names(self, outcomes_list) -> list:
    #     """
    #     Convert outcome names for Open Bets
    #     :param outcomes_list: 5-A-Side outcomes list
    #     :return: list of converted outcome names
    #     """
    #     converted_outcomes = []
    #     for outcome in outcomes_list:
    #         name = 'To Have'
    #         if name not in outcome:
    #             name = 'To Make'
    #         num = ''.join(re.findall(r'\d*\+', outcome))
    #         market = re.split(r'\d*\+', outcome)[1].strip(' ')
    #         try:
    #             player = outcome.split(name)[0].split('.')[1].strip(' ')
    #         except IndexError:
    #             player = outcome.split(name)[0].strip(' ')
    #         converted_outcomes.append(f' {player} {name} {num} {market}')
    #     return converted_outcomes

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        DESCRIPTION: Choose the '5-A-Side' tab
        DESCRIPTION: Click/Tap on the 'Build Team' button on '5-A-Side' launcher
        DESCRIPTION: Login
        EXPECTED: Make sure that '5-A-Side' overlay is opened
        """
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.__class__.market_name = vec.yourcall.MARKETS.player_bets
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        event_start_time = event_resp[0]['event']['startTime']
        utcoffset = -330 if self.device_type == 'mobile' and self.use_browser_stack else 0
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=time_format,
            ss_data=True, utcoffset=utcoffset)
        self.__class__.full_event_name = f'{self.event_name} {self.event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{self.full_event_name}" with market name "{self.market_name}", '
            f'event id "{self.event_name}", event start time "{self.event_start_time_local}"')
        self.site.login()
        self.__class__.user_balance = self.get_balance_by_page('all')
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.five_a_side),
                        msg=f'"{self.expected_market_tabs.five_a_side}" tab is not active')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')

    def test_001_select_at_least_2_players_on_the_pitch_view(self):
        """
        DESCRIPTION: Select at least 2 players on the 'Pitch View'
        EXPECTED: * The players are added and displayed on the corresponding position on the 'Pitch View'
        EXPECTED: * 'Odds/Place Bet' button is active
        EXPECTED: * Corresponding Odds value is displayed on 'Odds/Place Bet' button taken from <price> response
        """
        tab_content = self.site.sport_event_details.tab_content
        self.__class__.expected_players_list = []
        self.__class__.pitch_overlay = tab_content.pitch_overlay.content
        markets = self.pitch_overlay.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        self.__class__.used_players = []
        self.__class__.current_player_name = None
        for market_name, market in list(markets.items())[:2]:
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

    def test_002_click_tap_the_place_bet_button_verify_5_a_side_betslip_content(self):
        """
        DESCRIPTION: Click/Tap the' Place Bet' button.
        DESCRIPTION: Verify '5-A-Side Betslip' content.
        EXPECTED: * '5-A-Side Betslip' appears over the 'Pitch View'
        EXPECTED: * '50001' request is triggered in 'remotebetslip' connection in the WS
        EXPECTED: * '5-A-Side Betslip' contains the following elements:
        EXPECTED: * Header with 'Betslip' title and 'Close' button
        EXPECTED: * The list of added selections in the following format:
        EXPECTED: * 'Player Bets' title
        EXPECTED: * 'Player Name' + 'Market Name'
        EXPECTED: * 'Odds' and 'Stake' box
        EXPECTED: * 'Quick Stakes' buttons (e.g. "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * 'Total Stake' value
        EXPECTED: * 'Estimated returns'/'Potential returns' value
        EXPECTED: * 'Back' button is active
        EXPECTED: * 'Place bet' is disabled
        """
        self.assertTrue(self.pitch_overlay.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        self.pitch_overlay.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        if not self.is_safari:
            self.get_web_socket_response(self.response_50001)
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(self.byb_betslip_panel.is_displayed(), msg='5-A-Side BetSlip is not shown')
        title = self.byb_betslip_panel.header.title
        self.assertEqual(title, vec.yourcall.FIVE_A_SIDE_BETSLIP_TITLE,
                         msg=f'Header title "{title}" is not the same as expected '
                             f'"{vec.yourcall.FIVE_A_SIDE_BETSLIP_TITLE}"')
        self.assertTrue(self.byb_betslip_panel.header.close_button.is_displayed(), msg='"Close" button is not shown')
        selections = self.byb_betslip_panel.selection.content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='Players are not displayed on the 5-A-Side Betslip')
        selection_keys = [item.title() for item in list(selections.keys())]
        self.expected_players_list = [item.title() for item in self.expected_players_list]
        self.assertListEqual(selection_keys, self.expected_players_list,
                             msg=f'Selections names: \n"{selection_keys}" \nare not the same as they were on dashboard:'
                                 f' \n"{self.expected_players_list}"')

        self.__class__.expected_odds = self.byb_betslip_panel.selection.content.odds
        self.assertTrue(self.expected_odds, msg='Odds/price are not shown')

        stake_box = self.byb_betslip_panel.selection.content.amount_form
        self.assertTrue(stake_box.is_displayed(), msg='Stake box is not shown')

        self.assertTrue(self.byb_betslip_panel.quick_stake_panel.is_displayed(), msg='Quick stakes are not shown')

        self.__class__.stake = self.site.byb_betslip_panel.selection.bet_summary.total_stake
        self.assertTrue(self.stake, msg='Stake is not shown')

        self.__class__.est_returns = self.byb_betslip_panel.selection.bet_summary.total_estimate_returns
        self.assertTrue(self.est_returns, msg='Est. Returns is not shown')
        self.assertTrue(self.byb_betslip_panel.back_button.is_displayed(), msg='Back button is not shown')

        place_bet_button = self.byb_betslip_panel.place_bet
        self.assertFalse(place_bet_button.is_enabled(expected_result=False), msg='Place bet button is not disabled')

    def test_003_enter_any_value_into_the_stake_field_click_tap_place_bet_button(self):
        """
        DESCRIPTION: * Enter any value into the 'Stake' field.
        DESCRIPTION: * Click/Tap 'Place bet' button.
        EXPECTED: * Spinner is displayed on "Place bet" for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is displayed
        EXPECTED: * User Balance is updated
        """
        self.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.verify_user_balance(expected_user_balance=self.user_balance - self.stake_value)

    def test_004_verify_data_in_remote_betslip_connection_in_ws_client(self):
        """
        DESCRIPTION: Verify data in 'remotebetslip' connection in WS client
        EXPECTED: * '50011' request contains price, stake, currency, token and channel: "f" (for '5-A-Side' bets) info
        EXPECTED: * '51101' response contains "response code":1, date, betPotentialWin, numLines, betNo, betID, receipt, totalStake info
        EXPECTED: **Note:** if we receive 'Connection timeout' in websocket: (51102) from Banach, bet is not placed at 1st time, thus try several times to place a bet. It's related to tst2 env, could be reproduced only for this env.
        """
        if not self.is_safari:
            ws_client_response_structure = ['price', 'stake', 'currency']
            response_50011 = self.get_web_socket_response(self.response_50011)
            self.assertTrue(response_50011, msg=f'Response with frame ID #{self.response_50011} not received')
            self.assertTrue(all(response_50011.get(item) for item in ws_client_response_structure),
                            msg=f'Actual request data "{response_50011.keys()}" does not contain '
                                f'expected info "{ws_client_response_structure}"')

            ws_client_response_structure = ['betId', 'receipt', 'totalStake']
            response_51101 = self.get_web_socket_response(self.response_51101)
            self.assertTrue(response_51101, msg=f'Response with frame ID #"{self.response_51101}" not received')
            self._logger.debug(f'*** Request data "{response_51101}" for "{self.response_51101}"')
            actual_response_code = response_51101['data']['responseCode']
            self.assertEqual(actual_response_code, 1,
                             msg=f'Response code "{actual_response_code}" is not equalt to "1"')
            request_data = response_51101['data']['betPlacement']
            self.assertTrue(all(request_data[0].get(item) for item in ws_client_response_structure),
                            msg=f'Actual request data "{request_data[0].keys()}" does not contain '
                                f'expected info "{ws_client_response_structure}"')

    def test_005_verify_the_bet_receipt_content(self):
        """
        DESCRIPTION: Verify the 'Bet Receipt' content
        EXPECTED: Bet Receipt consists of:
        EXPECTED: * Header with 'Bet Receipt' title and 'Close' button
        EXPECTED: * Subheader with '✓Bet Placed Successfully' title and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * 'Single @' title with 'Odds'
        EXPECTED: * 'Receipt No' value
        EXPECTED: * The list of added selections in the following format:
        EXPECTED: * 'Player Bets' title
        EXPECTED: * 'Player Name' + 'Market Name'
        EXPECTED: * 'Stake for this bet' value
        EXPECTED: * 'Estimated returns'/'Potential returns' value
        """
        bet_receipt_selection = self.site.byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in 5-A-Side receipt')
        selection_keys = [item.title() for item in list(selections.keys())]
        self.assertListEqual(selection_keys, self.expected_players_list,
                             msg=f'Incorrect market names.\nActual list: {selection_keys}'
                                 f'\nExpected list: {self.expected_players_list}')

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
        self.__class__.est_returns = bet_receipt_selection.total_est_returns_value
        self.assertTrue(self.est_returns, msg='Total Est. Returns value not found')

    def test_006_click_tap_on_the_close_button(self):
        """
        DESCRIPTION: Click/Tap on the 'Close' button
        EXPECTED: * '5-A-Side Betslip' is closed
        EXPECTED: * '5-A-Side Overlay' is closed as well
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(expected_result=False),
                         msg='Pitch overlay is shown')

    def test_007_navigate_to_the_my_bets_page_tab_verify_the_bet_details_displaying(self):
        """
        DESCRIPTION: Navigate to the 'My Bets' page/tab.
        DESCRIPTION: Verify the Bet Details displaying.
        EXPECTED: The following data is displayed for the bet:
        EXPECTED: * Type of bet (e.g. SINGLE-5-A-SIDE)
        EXPECTED: * 'Market name' + 'Player Name'
        EXPECTED: * 'Odds' value
        EXPECTED: * '5-A-Side' label
        EXPECTED: * Event name (e.g. Team 1 v Team 2)
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * 'Stake' value
        EXPECTED: * 'Est. Returns'/'Potential returns' value
        EXPECTED: * 'Cashout' button (if available)
        """
        self.site.open_my_bets_open_bets()
        if self.device_type == 'mobile':
            self.site.wait_content_state(state_name='OpenBets', timeout=20)
        bet_name, single_byb_section = \
            self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.FIVE_A_SIDE_BET_TYPE_NAME.upper(),
                event_names=self.full_event_name,
                number_of_bets=1)
        bet_legs = single_byb_section.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'"{bet_name}" bet has no bet legs')
        betleg_name, betleg = list(bet_legs.items())[0]

        outcome_names = list(betleg.byb_selections.items_as_ordered_dict.keys())

        temp = ''.join(self.expected_players_list)
        found = outcome_names[0].strip() in temp and outcome_names[1].strip() in temp
        self.assertTrue(found, msg=f'Outcome name "{outcome_names}" is not '
                                   f'the same as expected "{self.expected_players_list}"')
        self.assertEqual(betleg.market_name.upper(), vec.yourcall.FIVE_A_SIDE_TITLE,
                         msg=f'Market name "{betleg.market_name.upper()}" is not '
                             f'the same as expected "{vec.yourcall.FIVE_A_SIDE_TITLE}"')

        self.assertEqual(betleg.event_name, self.event_name,
                         msg=f'Event name "{betleg.event_name}" is not '
                             f'the same as expected "{self.event_name}"')

        self.assertEqual(betleg.event_time, self.event_start_time_local,
                         msg=f'Event time "{betleg.event_time}" is not '
                             f'the same as expected "{self.event_start_time_local}"')

        self.assertEqual(single_byb_section.stake.currency, self.user_currency,
                         msg=f'Stake currency "{single_byb_section.stake.currency}" is '
                             f'not the same as expected "{self.user_currency}"')

        self.assertEqual(float(single_byb_section.stake.stake_value), self.stake_value,
                         msg=f'Stake amount value "{float(single_byb_section.stake.stake_value)}" is'
                             f' not the same as expected "{self.stake_value}"')

        self.assertEqual(betleg.odds_value, self.expected_odds,
                         msg=f'Odds value "{betleg.odds_value}" is not the same as expected "{self.expected_odds}"')

        self.assertEqual(single_byb_section.est_returns.currency, self.user_currency,
                         msg=f'Est. Returns currency "{single_byb_section.est_returns.currency}" is '
                             f'not the same as expected "{self.user_currency}"')

        actual_est_returns = single_byb_section.est_returns.stake_value
        self.assertAlmostEqual(float(actual_est_returns), float(self.est_returns), delta=0.02,
                               msg=f'Est. Returns amount value "{actual_est_returns}" is not '
                                   f'the same as expected "{self.est_returns}" with delta 0.02')
