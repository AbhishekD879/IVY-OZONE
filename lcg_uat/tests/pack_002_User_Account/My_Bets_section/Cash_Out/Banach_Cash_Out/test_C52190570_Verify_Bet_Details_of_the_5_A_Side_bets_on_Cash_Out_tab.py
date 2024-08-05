import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
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
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@vtest
@pytest.mark.issue("https://jira.egalacoral.com/browse/BMA-55778")
class Test_C52190570_Verify_Bet_Details_of_the_5_A_Side_bets_on_Cash_Out_tab(BaseFiveASide):
    """
    TR_ID: C52190570
    NAME: Verify Bet Details of the '5-A-Side' bet(s) on 'Cash Out' tab
    DESCRIPTION: Test case verifies Bet Details of the '5-A-Side' bet(s) on 'Cash Out' tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in the app
    PRECONDITIONS: 3. User has placed '5-A-Side' bet(s)
    PRECONDITIONS: 4. Navigate to 'Cash Out' tab via 'My Bets' page **Mobile** and via 'Bet Slip' widget **Tablet/Desktop**
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5-A-Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check data for the event on 'Cash Out' tab on 'My Bets' open the Dev tools > Network find **bet-details** request
    PRECONDITIONS: * To identify that it's the '5-A-Side' bet(s) verify the 'source' ('channel') parameter in the response - it should be 'f'
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Login
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        DESCRIPTION: User has placed '5-A-Side' bet(s)
        """
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.__class__.market_name = vec.yourcall.MARKETS.player_bets
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        event_start_time = event_resp[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=self.time_format,
            ss_data=True)
        self.__class__.full_event_name = f'{self.event_name} {self.event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{self.full_event_name}" with market name "{self.market_name}", '
            f'event id "{event_id}", event start time "{self.event_start_time_local}"')
        self.site.login()
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        five_a_side_tab = self.site.sport_event_details.markets_tabs_list.open_tab(
            tab_name=self.expected_market_tabs.five_a_side)
        self.assertTrue(five_a_side_tab, msg=f'{self.expected_market_tabs.five_a_side} tab is not active')
        tab_content = self.site.sport_event_details.tab_content
        tab_content.team_launcher.build_button.click()
        self.assertTrue(tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        self.__class__.expected_players_list = []
        markets = tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        used_players = []
        for market_name, market in list(markets.items())[:2]:
            if tab_content.pitch_overlay.has_journey_panel:
                tab_content.pitch_overlay.journey_panel.close_button.click()
            players = self.open_players_list(market=market, market_name=market_name)
            self.assertTrue(players, msg='Players are not displayed on the Players List')
            first_player_name = list(players.keys())[0]
            last_player_name = list(players.keys())[-1]
            counter = 0
            for player_name, player in players.items():
                if player_name not in used_players:
                    if counter > 0:
                        players = self.open_players_list(market=market, market_name=market_name)
                        player = players.get(player_name)
                    player.click()
                    self._logger.info(f'*** Selecting player "{player_name}" for market "{market_name}"')
                    self.assertTrue(tab_content.wait_for_players_card(),
                                    msg='Player Card is not shown')
                    player_card = tab_content.player_card
                    player_card.add_player_button.click()
                    self.assertTrue(market.added_player_name,
                                    msg=f'Failed to display added Player\'s Name "{player_name}"')
                    used_players.append(player_name)
                    if tab_content.pitch_overlay.content.wait_for_error_message(timeout=2):
                        self._logger.info(
                            f'Encountered error "{tab_content.pitch_overlay.content.error_message_text}", '
                            f'trying next player')
                        self.assertNotEqual(player_name, last_player_name,
                                            msg=f'No compatible players found for "{first_player_name}"')
                    else:
                        if market_name == 'To Be Carded':
                            expected_market_name = \
                                f'{market.added_player_name}'.split(' - ')[0]
                        elif 'Shots' in market_name:
                            expected_market_name = f'{market.added_player_name} To Have {market.name}'
                        else:
                            expected_market_name = f'{market.added_player_name} To Make {market.name}'

                        self.expected_players_list.append(expected_market_name)
                        break
                    counter += 1
        self.assertTrue(tab_content.pitch_overlay.content.football_field.place_bet_button.is_enabled(timeout=3),
                        msg='"Place Bet" button is disabled')
        tab_content.pitch_overlay.content.football_field.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')
        byb_betslip_panel = self.site.byb_betslip_panel
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)
        self.__class__.expected_odds = byb_betslip_panel.selection.content.odds
        self.assertTrue(self.expected_odds, msg='Odds/price are not shown')
        self.__class__.est_returns = byb_betslip_panel.selection.bet_summary.total_estimate_returns
        self.assertTrue(self.est_returns, msg='Total Est. Returns value not found')
        byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_5_a_side_bet_receipt_panel(timeout=25),
                        msg='5-A-Side Bet Receipt is not displayed')
        self.site.byb_bet_receipt_panel.header.close_button.click()

    def test_001_navigate_to_the_cash_out_tab_verify_displaying_of_5_a_side_bets(self):
        """
        DESCRIPTION: * Navigate to the 'Cash Out' tab.
        DESCRIPTION: * Verify displaying of '5-A-Side' bet(s).
        EXPECTED: The following bet details are shown for '5-A-Side' bet(s):
        EXPECTED: - Bet type **Single - 5-A-SIDE**
        EXPECTED: - Selections names have the following format:[Market name SELECTION NAME] and separated by a comma, truncated into a few lines
        EXPECTED: - **5-A-Side** text
        EXPECTED: - Corresponding Event name which redirects users to corresponding Event Details Page
        EXPECTED: - Event start date in HH:MM, DD MMM (e.g. 20:00, 21 Feb) and is shown next to Teams name (eg. A vs B)
        EXPECTED: - 'Watch' label if stream is available for the event
        EXPECTED: - Stake: <currency symbol> <value> (e.g., £10.00) shown in the footer of event card on the left
        EXPECTED: - Est. Returns/Potential Returns: <currency symbol> <value> (e.g., £30.00) shown next to stake value on the right
        EXPECTED: - Odds (displayed through '@' symbol next to selection name) eg.@1/5
        EXPECTED: - 'Cash Out <currency symbol> <value>' and 'Partial Cashout' buttons
        EXPECTED: All the details correspond to the placed '5-A-Side' bet(s)
        """
        self.site.open_my_bets_cashout()
        bet_name, single_byb_section = \
            self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.FIVE_A_SIDE_BET_TYPE,
                                                                  event_names=self.full_event_name,
                                                                  number_of_bets=1)
        bet_legs = single_byb_section.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'"{bet_name}" bet has no bet legs')
        betleg_name, betleg = list(bet_legs.items())[0]

        expected_players_list = self.convert_outcome_names(self.expected_players_list)
        outcome_name = list(betleg.byb_selections.items_as_ordered_dict.keys())
        self.assertListEqual(outcome_name, expected_players_list,
                             msg=f'Outcome name "{outcome_name}" is not '
                             f'the same as expected "{expected_players_list}"')

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

        self.assertTrue(single_byb_section.buttons_panel.has_full_cashout_button(),
                        msg=f'CASHOUT button was not found on bet: "{bet_name}" section or '
                            f'check "bet-details" response "cashoutValue" parameter value')
