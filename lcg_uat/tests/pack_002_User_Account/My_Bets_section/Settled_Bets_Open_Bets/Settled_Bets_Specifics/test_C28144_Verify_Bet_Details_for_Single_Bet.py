import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # we cannot settle bet on prod
# @pytest.mark.hl  # on hl as well
@pytest.mark.ob_smoke
@pytest.mark.my_bets
@pytest.mark.bet_history
@pytest.mark.bet_placement
@pytest.mark.bet_history_open_bets
@pytest.mark.cash_out
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.slow
@pytest.mark.timeout(720)  # result events takes so long
@vtest
class Test_C28144_Verify_Bet_Details_for_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C28144
    NAME: Verify Bet Details of a Single Bet
    DESCRIPTION: This test case verifies Bet Details of a Single Bet
    PRECONDITIONS: 1. User should be logged in to view his settled bets.
    PRECONDITIONS: 2. User should have few won/lost/void/cashed out Single bets
    """
    keep_browser_open = True
    username = None
    currency = '£'
    selection_ids = []
    expected_odds = '@ 1/2'

    def check_settled_bet_information(self, won=False, lost=False, void=False, cashed_out=False,
                                      bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=None):
        _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                           event_names=event_name,
                                                                           number_of_bets=4)
        self.assertEqual(bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertEqual(bet.market_name, self.expected_market_sections.match_result.title(),
                         msg=f'Bet market name: "{bet.market_name}" '
                             f'is not as expected: "{self.expected_market_sections.match_result.title()}"')
        self.assertTrue(bet.date, msg=f'Bet date is not shown')
        odds_sign = bet.odds_sign.strip('"')
        bet_odds = f'{odds_sign}{bet.odds_value}'
        self.assertEqual(bet_odds, self.expected_odds,
                         msg=f'Bet odds: "{bet_odds}" '
                             f'are not as expected: "{self.expected_odds}"')
        self.assertEqual(bet.stake.value, f'{bet.stake.currency}{self.bet_amount}',
                         msg=f'Bet Stake value: "{bet.stake.value}" '
                             f'is not as expected: "{bet.stake.currency}{self.bet_amount}"')
        if won:
            self.assertEqual(bet.bet_status, vec.betslip.WON_STAKE,
                             msg=f'Bet status: "{bet.bet_status}" '
                                 f'is not as expected: "{vec.betslip.WON_STAKE}"')
            self.assertEqual(bet.selection_name, self.selection_name_1,
                             msg=f'Bet selection name: "{bet.selection_name}" '
                                 f'is not as expected: "{self.selection_name_1}"')
            self.assertEqual(f'{bet.event_name} FT', event_name,
                             msg=f'Bet event name: "{bet.event_name} FT" '
                                 f'is not as expected: "{event_name}"')
            actual_message = f'{bet.cashed_out_message.text} {bet.cashed_out_value.text}'
            expected_message = f'{vec.bet_history.YOU_WON_LABEL} {bet.est_returns.value}'
            self.assertEqual(actual_message, expected_message,
                             msg=f'Bet message: "{actual_message}" '
                                 f'is not as expected: "{expected_message}"')
            self.assertEqual(bet.est_returns.value, bet.cashed_out_value.text,
                             msg=f'Bet Returns value: "{bet.est_returns.value}" '
                                 f'is not as expected: "{bet.cashed_out_value.text}"')
        if lost:
            self.assertEqual(bet.bet_status, vec.betslip.LOST_STAKE,
                             msg=f'Bet status: "{bet.bet_status}" '
                                 f'is not as expected: "{vec.betslip.LOST_STAKE}"')
            self.assertEqual(bet.selection_name, self.selection_name_2,
                             msg=f'Bet selection name: "{bet.selection_name}" '
                                 f'is not as expected: "{self.selection_name_2}"')
            self.assertEqual(f'{bet.event_name} FT', event_name,
                             msg=f'Bet event name: "{bet.event_name} FT" '
                                 f'is not as expected: "{event_name}"')
            self.assertEqual(bet.est_returns.value, f'{self.currency}0.00',
                             msg=f'Bet Returns value: "{bet.est_returns.value}" '
                                 f'is not as expected: "{bet.stake.value}"')
        if void:
            self.assertEqual(bet.bet_status, vec.betslip.CANCELLED_STAKE,
                             msg=f'Bet status: "{bet.bet_status}" '
                                 f'is not as expected: "{vec.betslip.CANCELLED_STAKE}"')
            self.assertEqual(bet.selection_name, self.selection_name_3,
                             msg=f'Bet selection name: "{bet.selection_name}" '
                                 f'is not as expected: "{self.selection_name_3}"')
            self.assertEqual(f'{bet.event_name} FT', event_name,
                             msg=f'Bet event name: "{bet.event_name} FT" '
                                 f'is not as expected: "{event_name}"')
            self.assertEqual(bet.est_returns.value, bet.stake.value,
                             msg=f'Bet Returns value: "{bet.est_returns.value}" '
                                 f'is not as expected: "{bet.stake.value}"')
        if cashed_out:
            self.assertEqual(bet.bet_status, vec.betslip.CASHOUT_STAKE,
                             msg=f'Bet status: "{bet.bet_status}" '
                                 f'is not as expected: "{vec.betslip.CASHOUT_STAKE}"')
            self.assertEqual(bet.selection_name, self.selection_name_4,
                             msg=f'Bet selection name: "{bet.selection_name}" '
                                 f'is not as expected: "{self.selection_name_4}"')
            actual_event_name = f'{bet.event_name} {self.event_start_time_4}'
            self.assertEqual(actual_event_name, self.event_name_4,
                             msg=f'Bet event name: "{actual_event_name}" '
                                 f'is not as expected: "{self.event_name_4}"')
            actual_message = f'{bet.cashed_out_message.text} {bet.cashed_out_value.text}'
            expected_message = vec.bet_history.CASHED_OUT_LABEL.format(float(bet.stake.stake_value))
            self.assertEqual(actual_message, expected_message,
                             msg=f'Bet message: "{actual_message}" '
                                 f'is not as expected: "{expected_message}"')
            self.assertEqual(bet.est_returns.value, bet.cashed_out_value.text,
                             msg=f'Bet Returns value: "{bet.est_returns.value}" '
                                 f'is not as expected: "{bet.cashed_out_value.text}"')

    def cashout_selection(self, event_name=None):
        self.site.open_my_bets_open_bets()

        bet_name, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=event_name, number_of_bets=4)

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test football event, PROD: Find active football event
        DESCRIPTION: Login as user that have enough funds to place a bet
        EXPECTED: User logged and event created/found
        """
        # Create test events
        # Event 1
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self._logger.info(f'*** Created event1 with params: {event_params}')
        team1, team2 = event_params.team1, event_params.team2
        self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.__class__.selection_name_1 = team1
        self.__class__.created_event_name_1 = f'{team1} v {team2}'
        self.__class__.eventID_1 = event_params.event_id
        self.__class__.marketID_1 = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.event_name_1 = f'{self.created_event_name_1} FT'
        # Event 2
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=2)
        self._logger.info(f'*** Created event2 with params: {event_params}')
        team1, team2 = event_params.team1, event_params.team2
        self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.__class__.selection_name_2 = team1
        self.__class__.created_event_name_2 = f'{team1} v {team2}'
        self.__class__.eventID_2 = event_params.event_id
        self.__class__.marketID_2 = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.event_name_2 = f'{self.created_event_name_2} FT'
        # Event 3
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=2)
        self._logger.info(f'*** Created event3 with params: {event_params}')
        team1, team2 = event_params.team1, event_params.team2
        self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.__class__.selection_name_3 = team1
        self.__class__.created_event_name_3 = f'{team1} v {team2}'
        self.__class__.eventID_3 = event_params.event_id
        self.__class__.marketID_3 = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.event_name_3 = f'{self.created_event_name_3} FT'
        # Event 4
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self._logger.info(f'*** Created event4 with params: {event_params}')
        team1, team2 = event_params.team1, event_params.team2
        self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.__class__.event_start_time_4 = self.convert_time_to_local(date_time_str=event_params.event_date_time)
        self.__class__.selection_name_4 = team1
        self.__class__.created_event_name_4 = f'{team1} v {team2}'
        self.__class__.eventID_4 = event_params.event_id
        self.__class__.marketID_4 = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.event_name_4 = f'{self.created_event_name_4} {self.event_start_time_4}'
        # Login
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        # Add selections via deeplink
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        # Place a bet
        self.place_single_bet(number_of_stakes=4)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        # Result selections to Win / Lost / Void
        self.result_event(selection_ids=self.selection_ids[0],
                          market_id=self.marketID_1, event_id=self.eventID_1, result='W')
        self.result_event(selection_ids=self.selection_ids[1],
                          market_id=self.marketID_2, event_id=self.eventID_2, result='L')
        self.result_event(selection_ids=self.selection_ids[2],
                          market_id=self.marketID_3, event_id=self.eventID_3, result='V')
        # Cashout selection
        self.cashout_selection(event_name=self.event_name_4)

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' tab is opened
        EXPECTED: * Won/lost/void/cashed out bet overview sections are present
        """
        self.site.open_my_bets_settled_bets()

    def test_002_verify_bet_with_won_status(self):
        """
        DESCRIPTION: Verify bet with **WON** status
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: * Bet type and "WON" label (in the header)
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: * green tick icon on the left of the selection
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        self.check_settled_bet_information(won=True, event_name=self.event_name_1)

    def test_003_verify_bet_with_lost_status(self):
        """
        DESCRIPTION: Verify bet with **LOST** status
        EXPECTED: * Bet type and "LOST" label (in the header)
        EXPECTED: * red cross icon on the left of the selection
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        self.check_settled_bet_information(lost=True, event_name=self.event_name_2)

    def test_004_verify_bet_with_void_status(self):
        """
        DESCRIPTION: Verify bet with **VOID** status
        EXPECTED: * Bet type and "VOID" label (in the header)
        EXPECTED: * VOID label on the left of the selection
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        self.check_settled_bet_information(void=True, event_name=self.event_name_3)

    def test_005_verify_bet_with_cashed_out_status(self):
        """
        DESCRIPTION: Verify bet with **CASHED OUT** status
        EXPECTED: * Bet type and "CASHED OUT" label (in the header)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        self.check_settled_bet_information(cashed_out=True, event_name=self.event_name_4)

    def test_006_verify_long_names_on_settled_bets_card(self):
        """
        DESCRIPTION: Verify long names on Settled Bets card
        EXPECTED: * Long name of a selection is fully displayed
        EXPECTED: * Long name of a market is truncated with ellipsis (...)
        EXPECTED: * Long name of an event is truncated with ellipsis (...)
        """
        # this part is verified in steps #2-#5 by self.check_settled_bet_information() method
        pass

    def test_007_repeat_this_test_case_for_a_bet_placed_on_private_market(self):
        """
        DESCRIPTION: Repeat this test case for a bet placed on Private Market
        DESCRIPTION: (except cashed out status, because cashout is not offered for bets placed on private market selections)
        """
        # we cannot test, as we won't settle private market event

    def test_008_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-10 for:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        """
        # this is already verified for 'bet-history' page
        pass
