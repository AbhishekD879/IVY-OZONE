from datetime import datetime

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.critical
@pytest.mark.bet_history_open_bets
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1377275_Verify_Bet_Details_of_Regular_Open_Bets_Singles(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C1377275
    NAME: Verify Bet Details of Regular Open Bets Singles
    DESCRIPTION: This test case verifies bet details of Regular Open bets
    PRECONDITIONS: 1. User should be logged in to view their open bets.
    PRECONDITIONS: 2. User should have a few open bets
    PRECONDITIONS: 3. User should have "My Bets" page opened
    """
    keep_browser_open = True
    created_event_name_with_time = None
    bet_name = None
    bet_amount = 1.00
    now = datetime.now()
    today = now.strftime('%m/%d/%Y')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test football event, PROD: Find active Football event
        """
        expected_template_market = 'Match Betting'

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        expected_template_market=expected_template_market)[0]
            eventID = event['event']['id']
            self.__class__.team1, self.__class__.team2 = (event['event']['name']).split(' v ')
            event_name = event['event']['name']
            self.__class__.created_event_name = normalize_name(event_name)
            event_start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                                ob_format_pattern=self.ob_format_pattern,
                                                                ss_data=True,
                                                                future_datetime_format=self.event_card_future_time_format_pattern)
            markets = event['event']['children']
            match_result = next((market for market in markets
                                 if market['market']['templateMarketName'] == expected_template_market), None)
            self.assertTrue(match_result,
                            msg=f'{expected_template_market} market was not found for event "{eventID}"')

            outcomes = match_result['market']['children']

            for outcome in outcomes:
                if outcome['outcome']['name'] == self.team1:
                    self.__class__.selection_ids = outcome['outcome']['id']
                    break
            self._logger.info(
                f'\n *** Found event "{self.created_event_name}" with id "{eventID}" local start time "{event_start_time_local}" '
                f'teams "{self.team1}" v "{self.team2}" selection ids "{self.selection_ids}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
                event.team1, event.team2, event.selection_ids[event.team1]
            event_start_time_local = self.convert_time_to_local(date_time_str=event.event_date_time)
            self.__class__.created_event_name = f'{self.team1} v {self.team2}'

        self.__class__.bet_name = f'SINGLE - [{self.created_event_name}]'
        self.__class__.created_event_name_with_time = f'{self.created_event_name} {event_start_time_local}'

    def test_001_login_and_place_bet(self):
        """
        DESCRIPTION: Log in user
        DESCRIPTION: Place a bet
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_place_single_bet(self):
        """
        DESCRIPTION: Place Single Bet
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_003_verify_bet_details_of_a_single_open_bet_in_the_bet_overview_pre_match_event(self):
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

        bet_name, self.__class__.single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.created_event_name_with_time, number_of_bets=2)

        bet_legs = self.single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}')

        outcome_name = next((bet['outcome_name'] for bet_name, bet in self.betslip_info.items()
                             if bet_name not in ['total_stake', 'total_estimate_returns', 'Double', 'Trixie',
                                                 'Round Robin', 'Flag', 'Single Stakes About', 'Double Stakes About']))

        for betleg_name, betleg in bet_legs.items():
            name = f'{outcome_name} - {self.created_event_name_with_time}'
            self.assertTrue(name in betleg_name, msg=f'"{name}" not found in "{betleg_name}')

            self.assertEqual(betleg.market_name, self.betslip_info[self.team1]['market_name'],
                             msg=f'"{betleg.market_name}" market name '
                             f'is not as expected: "{self.betslip_info[self.team1]["market_name"]}"')
            self.assertEqual(betleg.odds_value, self.betslip_info[self.team1]['odds'],
                             msg=f'"{betleg.odds_value}" odds value '
                             f'is not as expected: "{self.betslip_info[self.team1]["odds"]}"')
            self.assertTrue(betleg.event_time, msg='Can not find event time')
            self.assertFalse(betleg.has_link, msg='Event is hyperlinked')

        stake_value = self.single_bet.stake.stake_value
        expected_stake = self.betslip_info['total_stake']
        self.assertEqual(stake_value, '{0:.2f}'.format(self.bet_amount),
                         msg=f'Stake amount "{stake_value}" is not equal to expected "{expected_stake}" '
                             f'for bet "{self.single_bet.name}"')

        est_returns = float(self.single_bet.est_returns.stake_value)
        expected_est_returns = float(self.betslip_info['total_estimate_returns'])
        self.assertAlmostEqual(est_returns, expected_est_returns, delta=0.05,
                               msg=f'Estimated returns: "{est_returns}" '
                                   f'does not match with required: "{expected_est_returns}" '
                                   f'with delta 0.05')
