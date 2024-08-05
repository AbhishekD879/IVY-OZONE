import pytest

from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot settle bet on prod / hl
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.bet_history_open_bets
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.login
@vtest
class Test_C28145_Verify_Bet_Details_of_a_Multiple_Bet(BaseBetSlipTest):
    """
    TR_ID: C28145
    NAME: Verify Bet Details of a Multiple Bet
    DESCRIPTION: This test case verifies Bet Details of a Multiple Bet
    PRECONDITIONS: 1. User should be logged in to view their settled bets.
    PRECONDITIONS: 2. User should have few open/won/settled/void/cashed out Multiples bets
    PRECONDITIONS: 3. User should have Multiples bets that were reviewed by Overask functionality (rejected, offered and so on)
    """
    keep_browser_open = True
    username = None
    currency = '£'
    selection_ids_won, selection_ids_lost, selection_ids_void, selection_ids_cashed_out = [], [], [], []
    expected_odds = '@ 1/2'

    def verify_betlegs(self, bet, bet_name, expected_icon, expected_selections, expected_event_names):
        """
        Helper method to verify each betleg item of bet
        """
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No bet leg was found for bet "{bet_name}"')
        expected_market = self.expected_market_sections.match_result.title()

        for index in range(len(betlegs.items())):
            betleg_name, betleg = list(betlegs.items())[index]
            expected_event_selection_name = f'{expected_selections[index]} - {expected_event_names[index]}'
            self.assertEqual(betleg_name, expected_event_selection_name,
                             msg=f'Bet selection / event names: "{betleg_name}" '
                                 f'is not as expected: "{expected_event_selection_name}"')

            self.assertEqual(betleg.market_name, expected_market,
                             msg=f'Bet market name: "{betleg.market_name}" is not as expected: "{expected_market}"')

            odds_sign = betleg.odds_sign.strip('"')
            bet_odds = f'{odds_sign}{betleg.odds_value}'
            self.assertEqual(bet_odds, self.expected_odds,
                             msg=f'Bet odds: "{bet_odds}" are not as expected: "{self.expected_odds}"')

            if expected_icon:
                self.assertEquals(betleg.icon.status, expected_icon,
                                  msg=f'Actual icon status "{betleg.icon.status}" for "{bet_name}" '
                                      f'is not as expected "{expected_icon}"')

    def check_settled_bet_information(self, won=False, lost=False, void=False, cashed_out=False,
                                      bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_name=None):
        """
        Helper method which verifies correctness of bet details on 'Settled Bets' tab.
        Created in order to combine and not use copy-pasted code for same verifications
        """
        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                                  event_names=event_name)
        self.assertEqual(bet.bet_type, vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                         msg=f'Bet type: "{bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE}"')
        self.assertTrue(bet.date, msg=f'Bet date is not shown')
        self.assertEqual(bet.stake.value, f'{bet.stake.currency}{self.bet_amount}',
                         msg=f'Bet Stake value: "{bet.stake.value}" '
                             f'is not as expected: "{bet.stake.currency}{self.bet_amount}"')
        if won:
            expected_status = vec.betslip.WON_STAKE
            expected_returns = bet.cashed_out_value.text

            actual_message = f'{bet.cashed_out_message.text} {bet.cashed_out_value.text}'
            expected_message = f'{vec.bet_history.YOU_WON_LABEL} {bet.est_returns.value}'
            self.assertEqual(actual_message, expected_message,
                             msg=f'Bet message: "{actual_message}" '
                                 f'is not as expected: "{expected_message}"')
            self.verify_betlegs(bet=bet, bet_name=bet_name, expected_icon='won',
                                expected_selections=self.won_selections_names,
                                expected_event_names=self.won_events_name)

        if lost:
            expected_status = vec.betslip.LOST_STAKE
            expected_returns = f'{self.currency}0.00'
            self.verify_betlegs(bet=bet, bet_name=bet_name, expected_icon='lost',
                                expected_selections=self.lost_selections_names,
                                expected_event_names=self.lost_events_name)

        if void:
            expected_status = vec.betslip.CANCELLED_STAKE
            expected_returns = bet.stake.value
            self.verify_betlegs(bet=bet, bet_name=bet_name, expected_icon='void',
                                expected_selections=self.void_selections_names,
                                expected_event_names=self.void_events_name)

        if cashed_out:
            expected_status = vec.betslip.CASHOUT_STAKE
            expected_returns = bet.cashed_out_value.text

            actual_message = f'{bet.cashed_out_message.text} {bet.cashed_out_value.text}'
            expected_message = vec.bet_history.CASHED_OUT_LABEL.format(float(bet.stake.stake_value))
            self.assertEqual(actual_message, expected_message,
                             msg=f'Bet message: "{actual_message}" '
                                 f'is not as expected: "{expected_message}"')
            self.verify_betlegs(bet=bet, bet_name=bet_name, expected_icon=None,
                                expected_selections=self.cashed_out_selections_names,
                                expected_event_names=self.cashed_out_events_name)

        self.assertEqual(bet.bet_status, expected_status,
                         msg=f'Bet status: "{bet.bet_status}" is not as expected: "{expected_status}"')
        self.assertEqual(bet.est_returns.value, expected_returns,
                         msg=f'Bet Returns value: "{bet.est_returns.value}" is not as expected: "{expected_returns}"')

    def cashout_selection(self, event_name=None):
        self.site.open_my_bets_open_bets()

        bet_name, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=event_name)

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test football event
        DESCRIPTION: Login as user that have enough funds to place a bet
        EXPECTED: User logged and event created
        """
        # 'Won' events
        event_params_1 = self.ob_config.add_autotest_premier_league_football_event()
        event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
        event_id1, event_id2 = event_params_1.event_id, event_params_2.event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID = self.ob_config.market_ids[event_params_1.event_id][market_short_name]

        team1_1, team1_2, team2_1, team2_2 = \
            event_params_1.team1, event_params_1.team2, event_params_2.team1, event_params_2.team2
        self.__class__.won_events_name = [f'{team1_1} v {team1_2} FT', f'{team2_1} v {team2_2} FT']
        self.__class__.won_bet_name = f'DOUBLE - [{team1_1} v {team1_2} FT, {team2_1} v {team2_2} FT]'
        self.__class__.won_selections_names = (team1_1, team2_1)
        for event_params in (event_params_1, event_params_2):
            self.selection_ids_won.append(list(event_params.selection_ids.values())[0])

        # 'Lost' events
        event_params_3 = self.ob_config.add_autotest_premier_league_football_event()
        event_params_4 = self.ob_config.add_autotest_premier_league_football_event()
        event_id3, event_id4 = event_params_3.event_id, event_params_4.event_id

        team1_1, team1_2, team2_1, team2_2 = \
            event_params_3.team1, event_params_3.team2, event_params_4.team1, event_params_4.team2
        self.__class__.lost_events_name = [f'{team1_1} v {team1_2} FT', f'{team2_1} v {team2_2} FT']
        self.__class__.lost_bet_name = f'DOUBLE - [{team1_1} v {team1_2} FT, {team2_1} v {team2_2} FT]'
        self.__class__.lost_selections_names = (team1_1, team2_1)
        for event_params in (event_params_3, event_params_4):
            self.selection_ids_lost.append(list(event_params.selection_ids.values())[0])

        # 'Void' events
        event_params_5 = self.ob_config.add_autotest_premier_league_football_event()
        event_params_6 = self.ob_config.add_autotest_premier_league_football_event()
        event_id5, event_id6 = event_params_5.event_id, event_params_6.event_id

        team1_1, team1_2, team2_1, team2_2 = \
            event_params_5.team1, event_params_5.team2, event_params_6.team1, event_params_6.team2
        self.__class__.void_events_name = [f'{team1_1} v {team1_2} FT', f'{team2_1} v {team2_2} FT']
        self.__class__.void_bet_name = f'DOUBLE - [{team1_1} v {team1_2} FT, {team2_1} v {team2_2} FT]'
        self.__class__.void_selections_names = (team1_1, team2_1)
        for event_params in (event_params_5, event_params_6):
            self.selection_ids_void.append(list(event_params.selection_ids.values())[0])

        # 'Cashed Out' events
        event_params_7 = self.ob_config.add_autotest_premier_league_football_event()
        event_params_8 = self.ob_config.add_autotest_premier_league_football_event()

        team1_1, team1_2, team2_1, team2_2 = \
            event_params_7.team1, event_params_7.team2, event_params_8.team1, event_params_8.team2

        local_start_time_7 = self.convert_time_to_local(date_time_str=event_params_7.event_date_time)
        local_start_time_8 = self.convert_time_to_local(date_time_str=event_params_8.event_date_time)
        self.__class__.cashed_out_events_name = [f'{team1_1} v {team1_2} {local_start_time_7}',
                                                 f'{team2_1} v {team2_2} {local_start_time_8}']
        self.__class__.cashed_out_bet_name = f'DOUBLE - [{team1_1} v {team1_2} {local_start_time_7}, ' \
                                             f'{team2_1} v {team2_2} {local_start_time_8}]'
        self.__class__.cashed_out_selections_names = (team1_1, team2_1)
        for event_params in (event_params_7, event_params_8):
            self.selection_ids_cashed_out.append(list(event_params.selection_ids.values())[0])

        self.site.login(async_close_dialogs=False)
        for selection in [self.selection_ids_won, self.selection_ids_lost, self.selection_ids_void,
                          self.selection_ids_cashed_out]:
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=selection)
            self.place_multiple_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.done_button.click()

        self.result_event(selection_ids=self.selection_ids_won[0],
                          market_id=self.marketID, event_id=event_id1, result='W')
        self.result_event(selection_ids=self.selection_ids_won[1],
                          market_id=self.marketID, event_id=event_id2, result='W')
        self.result_event(selection_ids=self.selection_ids_lost[0],
                          market_id=self.marketID, event_id=event_id3, result='L')
        self.result_event(selection_ids=self.selection_ids_lost[1],
                          market_id=self.marketID, event_id=event_id4, result='L')
        self.result_event(selection_ids=self.selection_ids_void[0],
                          market_id=self.marketID, event_id=event_id5, result='V')
        self.result_event(selection_ids=self.selection_ids_void[1],
                          market_id=self.marketID, event_id=event_id6, result='V')

        # Cashing out 'Cashed out' bet
        self.site.open_my_bets_open_bets()

        bet_name, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.cashed_out_bet_name)

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page
        EXPECTED: * 'Settled' page is opened with 'Settled Bets' header and Back button
        EXPECTED: *  Open/won/settled/void/cashed out bet sections are present
        """
        self.site.open_my_bets_settled_bets()
        self.__class__.bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')

    def test_002_verify_bet_details_of_a_won_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **WON** Multiple bet
        EXPECTED: * "WON" status is shown in the top right corner of the section
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: * All selections have "green tick" icons on the left to them
        EXPECTED: Bet details are correct:
        EXPECTED: * Bet type (Multiple)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name
        EXPECTED: * Event match time next to event name
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) in the card footer
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Bet Receipt number and date of placing the bet
        """
        self.check_settled_bet_information(won=True, event_name=self.won_bet_name)

    def test_003_verify_bet_details_of_a_lost_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **LOST** Multiple bet
        EXPECTED: * "LOST" status is shown in the top right corner of the section
        EXPECTED: * Won selections have "green tick" icons on the left of the selection
        EXPECTED: * Lost selections have "red cross" icons on the left of the selection
        EXPECTED: * In case selection is not resulted  - No label is shown
        EXPECTED: Bet details are correct: same as in Step#2
        """
        self.check_settled_bet_information(lost=True, event_name=self.lost_bet_name)

    def test_004_verify_bet_details_of_a_void_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **VOID** Multiple bet
        DESCRIPTION: NOTE: ALL Selection in the bet should be resulted
        EXPECTED: * "VOID" status is shown in the top right corner of the section
        EXPECTED: * Won selections have "green tick" icons on the left of the selection
        EXPECTED: * Lost selections have "red cross" icons on the left of the selection
        EXPECTED: Bet details are correct: same as in Step#2
        """
        self.check_settled_bet_information(void=True, event_name=self.void_bet_name)

    def test_005_verify_bet_details_of_a_cashed_out_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **CASHED OUT** Multiple bet
        EXPECTED: * "CASHED OUT" status is shown in the top right corner of the section
        EXPECTED: Bet details are correct: same as in Step#2
        """
        self.check_settled_bet_information(cashed_out=True, event_name=self.cashed_out_bet_name)
