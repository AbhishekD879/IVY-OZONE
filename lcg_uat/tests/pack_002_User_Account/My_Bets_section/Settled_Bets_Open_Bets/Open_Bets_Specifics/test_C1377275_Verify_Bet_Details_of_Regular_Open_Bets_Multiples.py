from datetime import datetime
from random import choice

import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1377275_Verify_Bet_Details_of_Regular_Open_Bets_Multiples(BaseCashOutTest, BaseBetSlipTest):
    """
    TR_ID: C1377275
    NAME: Verify Bet Details of Regular Open Bets Multiples
    DESCRIPTION: This test case verifies bet details of Regular Open bets
    PRECONDITIONS: 1. User should be logged in to view their open bets.
    PRECONDITIONS: 2. User should have a few open bets
    PRECONDITIONS: 3. User should have "My Bets" page opened
    """
    keep_browser_open = True
    long_name = 'New Auto test name that is long enough to test if long name is wrapped to next line'
    expected_bet_leg_1, expected_bet_leg_2 = None, None
    bet_amount = 1
    now = datetime.now()
    today = now.strftime('%m/%d/%Y')
    is_live = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test football event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.is_live = False
            expected_template_market = 'Match Betting'
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         expected_template_market=expected_template_market,
                                                         all_available_events=True)
            # event 1
            event = choice(events)
            events.remove(event)
            self.__class__.eventID = event['event']['id']
            event_name = normalize_name(event['event']['name'])
            self.__class__.created_event_name = normalize_name(event_name)
            self.__class__.event_start_time = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                                         ob_format_pattern=self.ob_format_pattern,
                                                                         ss_data=True,
                                                                         future_datetime_format=self.event_card_future_time_format_pattern)
            markets = event['event']['children']
            match_result_and_both_teams_to_score = next((market for market in markets
                                                         if market['market']['templateMarketName'] == expected_template_market), None)
            self.assertTrue(match_result_and_both_teams_to_score,
                            msg=f'Market with templateMarketName "{expected_template_market}" was not found for event "{self.eventID}"')

            outcomes = match_result_and_both_teams_to_score['market']['children']

            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            # it's better to get the lowest possible odds so we won't fail on est returns calculation
            self.__class__.team1 = min(outcomes, key=lambda o: o['outcome']['children'][0]['price']['priceDec'])['outcome']['name']

            self._logger.info(f'*** Found event "{self.eventID}" - "{self.created_event_name}" - "{self.event_start_time}" '
                              f'with selection id\'s {self.selection_ids} selection "{self.team1}"')

            # event 2
            event_2 = choice(events)
            self.__class__.eventID_2 = event_2['event']['id']
            self.__class__.created_event_2_name = event_2['event']['name']
            self.__class__.event_2_start_time = self.convert_time_to_local(date_time_str=event_2['event']['startTime'],
                                                                           ob_format_pattern=self.ob_format_pattern,
                                                                           ss_data=True)
            markets = event_2['event']['children']
            match_result_and_both_teams_to_score = next((market for market in markets
                                                         if market['market']['templateMarketName'] == expected_template_market), None)
            self.assertTrue(match_result_and_both_teams_to_score,
                            msg=f'Market with templateMarketName "{expected_template_market}" was not found for event "{self.eventID}"')

            outcomes_2 = match_result_and_both_teams_to_score['market']['children']

            self.__class__.selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}

            # it's better to get the lowest possible odds so we won't fail on est returns calculation
            self.__class__.team2 = min(outcomes_2, key=lambda o: o['outcome']['children'][0]['price']['priceDec'])['outcome']['name']

            self._logger.info(f'*** Found event "{self.eventID_2}" - "{self.created_event_2_name}" - "{self.event_2_start_time}" '
                              f'with selection id\'s {self.selection_ids2} selection "{self.team2}"')

        else:
            self.__class__.is_live = True
            event_params = self.ob_config.add_autotest_premier_league_football_event(team1=self.long_name,
                                                                                     markets=[('match_result_and_both_teams_to_score',
                                                                                              {'cashout': True})],
                                                                                     is_live=self.is_live)
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, \
                list(event_params.selection_ids.values())[0]
            self.__class__.created_event_name = f'{self.team1} v {event_params.team2}'
            self.__class__.event_start_time = self.convert_time_to_local(date_time_str=event_params.event_date_time)

            event_params2 = self.ob_config.add_autotest_premier_league_football_event(
                markets=[('match_result_and_both_teams_to_score', {'cashout': True})], is_live=self.is_live)
            self.__class__.team2, self.__class__.selection_ids2 = event_params2.team2, \
                list(event_params2.selection_ids.values())[0]
            self.__class__.created_event_2_name = f'{event_params2.team1} v {self.team2}'
            self.__class__.event_2_start_time = self.convert_time_to_local(date_time_str=event_params2.event_date_time,
                                                                           future_datetime_format=self.event_card_future_time_format_pattern)
        self.__class__.expected_bet_leg_1 = f'{self.team1} - {self.created_event_name} {self.event_start_time}'
        self.__class__.expected_bet_leg_2 = f'{self.team2} - {self.created_event_2_name} {self.event_2_start_time}'

    def test_001_login_and_place_bet(self):
        """
        DESCRIPTION: Log in user
        DESCRIPTION: Place a bet
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_banners=False)
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1],
                                                         self.selection_ids2[self.team2]))

    def test_002_place_multiple_bet(self):
        """
        DESCRIPTION: Place Multiple Bet
        """
        self.__class__.betslip_info = self.place_and_validate_multiple_bet(number_of_stakes=1)

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_003_verify_bet_details_of_a_multiple_open_bet_in_the_bet_overview_pre_match_event(self):
        """
        DESCRIPTION: Verify bet details of a **Single** Open bet in the bet overview **(Pre-match event)**
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: * Bet type
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name and event start date and time in DD MM, HH:MM format using 12-hour clock (AM/PM) (e.g. 05 Jan, 1:49PM)
        EXPECTED: Note: Event name is NOT hyperlinked if bet was placed on selections from Enhanced Multiples market
        EXPECTED: * Date when bet was placed
        EXPECTED: * Bet Receipt number
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        """
        self.site.open_my_bets_open_bets()

        bet_name, self.__class__.multiple_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE',
            event_names=self.created_event_name,
            number_of_bets=1)
        bet_legs = self.multiple_bet.items_as_ordered_dict
        self.assertTrue(len(bet_legs) == 2, msg=f'No one bet leg was found for bet: "{bet_name}')

        for betleg_name, betleg in bet_legs.items():
            market_name = self.betslip_info[betleg.outcome_name]['market_name']

            self.assertEqual(betleg.market_name, market_name,
                             msg=f'"{betleg.market_name}" market name '
                             f'is not as expected: "{market_name}"')
            self.assertEqual(betleg.odds_value, self.betslip_info[betleg.outcome_name]['odds'])

            if self.is_live:
                self.assertTrue(betleg.has_live_label, msg='Can not find live event label')
            else:
                self.assertFalse(betleg.has_live_label, msg='Found live event label')

            self.assertFalse(betleg.has_link, msg='Event is hyperlinked')

            self.assertEqual(self.multiple_bet.stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                             msg='Stake amount "%s" is not equal to expected "%s" for bet "%s"' %
                                 (self.multiple_bet.stake.value, self.betslip_info['total_stake'],
                                  self.multiple_bet.name))

        actual_est_returns = float(self.multiple_bet.est_returns.stake_value)
        expected_est_returns = 'N/A' if self.betslip_info['total_estimate_returns'] == 'N/A' else float('{0:.2f}'.format(float(self.betslip_info['total_estimate_returns'])))
        delta = 0.03
        self.assertAlmostEqual(actual_est_returns, expected_est_returns, delta=delta,
                               msg=f'Actual Estimated returns: "{actual_est_returns}" '
                                   f'does not match with excepted: "{expected_est_returns}" with delta "{delta}"')

    def test_004_verify_long_names_on_open_bet_card(self):
        """
        DESCRIPTION: Verify long names on Open bet card
        EXPECTED: * Long name of a selection is wrapped to the next line
        EXPECTED: * Long name of a market is wrapped to the next line
        EXPECTED: * Long name of an event is wrapped to the next line
        """
        if tests.settings.backend_env != 'prod':
            # we cannot control length of outcome/market on prod
            bet_legs = self.multiple_bet.items_as_ordered_dict
            [self.assertTrue(betleg.is_outcome_name_wrapped(),
                             msg=f'Outcome name "{betleg.outcome_name}" is not wrapped to the next line')
             for betleg_name, betleg in bet_legs.items()]
            [self.assertTrue(betleg.is_market_name_wrapped(),
                             msg=f'Market name "{betleg.market_name}" is not wrapped to the next line')
             for betleg_name, betleg in bet_legs.items()]
            wrapped_event = next(betleg for betleg_name, betleg in bet_legs.items() if
                                 self.created_event_name in betleg_name)
            self.assertTrue(wrapped_event.is_event_name_wrapped(),
                            msg=f'Event name "{wrapped_event.event_name}" is not wrapped to the next line')
