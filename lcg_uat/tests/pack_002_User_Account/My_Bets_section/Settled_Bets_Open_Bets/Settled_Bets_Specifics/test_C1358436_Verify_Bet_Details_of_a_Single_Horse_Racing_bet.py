import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod we can't result_event on prod
# @pytest.mark.hl we can't result_event on prod
@pytest.mark.bet_history
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.each_way
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.bet_history_open_bets
@pytest.mark.critical
@pytest.mark.login
@vtest
class Test_C1358436_Verify_Bet_Details_of_a_Single_Horse_Racing_bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C1358436
    NAME: Verify Bet Details of a Single Horse Racing bet
    DESCRIPTION: This test case verifies bet details of a single horse racing bet
    PRECONDITIONS: 1. User should be logged in to view their Settled Bets.
    PRECONDITIONS: 2. User should have Single horse racing bets placed with each way and without
    """
    keep_browser_open = True
    bet_info, bet_info_ew_terms = None, None
    bet_type, bet_type_ew = 'SINGLE', 'SINGLE (EACH WAY)'
    expected_market_name_ew = None
    ew_my_bet_format = vec.bet_history.EXPECTED_MY_BETS_EACH_WAY_FORMAT
    ew_terms = None
    each_way = None
    bet_amount = 0.5

    def check_my_bets_bet_details(self, bet, bet_type, betslip_info, ew=False):
        self.assertEqual(bet.bet_type, bet_type, msg=f'Bet type "{bet.bet_type}" is not the same'
                                                     f' as expected "{bet_type}"')
        bet_legs = bet.items_as_ordered_dict
        self.assertEqual(len(bet_legs), 1, msg=f'Number of bet legs "{len(bet_legs)}" '
                                               f'is not the same as expected for bet type "{bet_type}": "1"')
        leg_name, leg = list(bet_legs.items())[0]
        expected_market_name = self.expected_market_name_ew if ew else self.default_market_name
        self.assertEqual(leg.market_name, expected_market_name,
                         msg=f'Market name "{leg.market_name}" is not the same as expected "{expected_market_name}"')

        outcome_name = next((bet['outcome_name'] for bet_name, bet in betslip_info.items()), '')

        self.assertEqual(leg.outcome_name, outcome_name,
                         msg=f'Selection name "{leg.outcome_name}" is not the same as expected "{outcome_name}"')

        expected_odds = betslip_info[outcome_name]['odds']
        self.assertEqual(leg.odds_value, expected_odds,
                         msg=f'Odds "{leg.odds_value}" is not the same as expected "{expected_odds}"')
        expected_unit_stake = '%0.2f' % self.bet_amount
        bet_amount = self.bet_amount * 2 if ew else self.bet_amount
        expected_total_stake = '%0.2f' % bet_amount
        if ew:
            self.assertEqual(bet.unit_stake.stake_value, expected_unit_stake,
                             msg=f'Unit stake "{bet.unit_stake.stake_value}" '
                                 f'is not as entered on Betslip "{expected_unit_stake}"')
            self.assertEqual(bet.unit_stake.currency, '£',
                             msg=f'Unit stake currency "{bet.unit_stake.currency}" is not the same as expected "£"')

        self.assertEqual(bet.stake.stake_value, expected_total_stake,
                         msg=f'Total stake "{bet.stake.stake_value}" '
                             f'is not the same as expected "{expected_total_stake}"')
        self.assertEqual(bet.stake.currency, '£',
                         msg=f'Stake currency "{bet.stake.currency}" is not the same as expected "£"')

        expected_est_returns = f'{float(betslip_info[outcome_name]["estimate_returns"]):.2f}'
        self.assertAlmostEqual(float(bet.est_returns.stake_value), float(expected_est_returns), delta=0.011,
                               msg=f'Estimate returns "{bet.est_returns.stake_value}" is not the same as calculated '
                                   f'on Betslip "{expected_est_returns}" within 0.011 delta')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test horseracing event with Each Way Terms, PROD: Find Horseracing event with Each Way Terms
        """
        self.__class__.ew_terms = {'ew_places': 2, 'ew_fac_num': 1, 'ew_fac_den': 16}

        event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=2,
                                                              lp_prices={0: '1/2', 1: '5/7'})
        self.__class__.selection_ids = event_parameters.selection_ids.values()
        self.__class__.created_event_name = f'{self.horseracing_autotest_uk_name_pattern}'
        self.__class__.marketID = self.ob_config.market_ids[event_parameters.event_id]
        self.__class__.eventID = event_parameters.event_id

        self.__class__.each_way = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms['ew_fac_num'],
                                                               ew_fac_den=self.ew_terms['ew_fac_den'],
                                                               ew_places=','.join(
                                                                   str(place) for place in
                                                                   range(1, int(self.ew_terms['ew_places']) + 1)))
        self.__class__.expected_market_name_ew = f'{self.default_market_name}, {self.each_way}'

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that has enough funds to place a bet
        """
        self.site.login()

    def test_002_place_2_single_bets(self):
        """
        DESCRIPTION: Place 2 single bets - one on racing selection - one with Each Way terms selected, other - Each Way terms not selected
        EXPECTED: Bets are placed
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids)[0])
        self.__class__.bet_info = self.place_and_validate_single_bet()
        self._logger.debug(f'*** Bet info, without each way "{self.bet_info}"')

        self.site.bet_receipt.footer.click_done()
        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=list(self.selection_ids)[1])
        self.__class__.bet_info_ew_terms = self.place_and_validate_single_bet(each_way=True)
        self._logger.debug(f'*** Bet info, with each way "{self.bet_info_ew_terms}"')

        self.site.bet_receipt.footer.click_done()
        self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False), msg='Bet Receipt was not closed')
        self.result_event(selection_ids=list(self.selection_ids), market_id=self.marketID, event_id=self.eventID)

    def test_003_navigate_to_bet_history_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' tab is opened
        EXPECTED: * Default view is List view
        """
        self.site.open_my_bets_settled_bets()

    def test_004_verify_bet_details_of_a_single_horse_racing_bet_each_way(self):
        """
        DESCRIPTION: Verify bet details of a Single Horse Racing bet (each way)
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single - Each Way")
        EXPECTED: * Selection name
        EXPECTED: * Market name user has bet on and Each Way terms - e.g., "Win or Each Way, 1/4 odds - places 1,2,3,4")
        EXPECTED: * Event name and start time (e.g., "1:40 Greyville")
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Unit stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Total stake <currency symbol> <value> (e.g., £20.00)
        EXPECTED: * Est. returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: If estimated returns are not available, "N/A" is shown
        """
        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=self.bet_type_ew,
                                                                                  event_names=self.created_event_name,
                                                                                  number_of_bets=1)
        self._logger.debug(f'*** Bet name "{bet_name}", bet "{bet}"')

        self.check_my_bets_bet_details(bet=bet, bet_type=self.bet_type_ew, betslip_info=self.bet_info_ew_terms, ew=True)

    def test_005_verify_bet_details_of_a_single_horse_racing_bet_no_each_way(self):
        """
        DESCRIPTION: Verify bet details of a Single Horse Racing bet (NO each way)
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single")
        EXPECTED: * Selection name
        EXPECTED: * Market name user has bet on - e.g., "Win or Each Way")
        EXPECTED: * Event name and start time (e.g., "1:40 Greyville")
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake <currency symbol> <value> (e.g., £20.00)
        EXPECTED: * Est. returns <currency symbol> <value> (e.g., £40.00)
        EXPECTED: If estimated returns are not available, "N/A" is shown
        """
        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type,
            event_names=self.created_event_name,
            number_of_bets=2)
        self._logger.debug(f'*** Bet name "{bet_name}", bet "{bet}"')

        self.check_my_bets_bet_details(bet=bet, bet_type=self.bet_type, betslip_info=self.bet_info)

    def test_006_repeat_steps_4_5_for_bet_history_tab_account_history_page(self):
        """
        DESCRIPTION: Repeat steps 4-5 for:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile)
        """
        if self.brand != 'ladbrokes':
            self.test_003_navigate_to_bet_history_tab_on_my_bets_page_for_mobile()
            self.test_004_verify_bet_details_of_a_single_horse_racing_bet_each_way()
            self.test_005_verify_bet_details_of_a_single_horse_racing_bet_no_each_way()
