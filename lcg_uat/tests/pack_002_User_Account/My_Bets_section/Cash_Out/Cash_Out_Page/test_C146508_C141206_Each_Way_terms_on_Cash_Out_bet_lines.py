import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.each_way
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@pytest.mark.slow
@pytest.mark.timeout(800)
@vtest
class Test_C146508_C141206_Each_Way_terms_on_Cash_Out_bet_lines(BaseCashOutTest):
    """
    TR_ID: C146508
    TR_ID: C141206
    NAME: Each Way terms on Cash Out bet lines
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed bets with E/W where Cash Out offer is available
    PRECONDITIONS: Use the next link in order to get information about event:
    """
    keep_browser_open = True
    long_racing_name = 'Auto test name that is long enough to test if long horse name is truncated with dots dots dots'
    long_racing_name_1 = 'Test auto name that is long enough to test if long horse name is truncated with dots dots dots'
    racing_event_name, racing_event_name2 = None, None
    single_bet, double_bet = None, None

    ew_terms = {'ew_places': 2, 'ew_fac_num': 1, 'ew_fac_den': 6}
    ew_my_bet_format = vec.bet_history.EXPECTED_MY_BETS_EACH_WAY_FORMAT
    each_way = ew_my_bet_format.format(ew_fac_num=ew_terms['ew_fac_num'], ew_fac_den=ew_terms['ew_fac_den'],
                                       ew_places=','.join(str(place) for place in range(1, ew_terms['ew_places'] + 1)))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        name_pattern = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.name_pattern
        horse_event = self.ob_config.add_UK_racing_event(number_of_runners=1, runner_names=[self.long_racing_name],
                                                         cashout=True, ew_terms=self.ew_terms)
        start_time = horse_event.event_date_time
        start_time_local = self.convert_time_to_local(date_time_str=start_time)
        self.__class__.racing_event_name = f'{name_pattern} {start_time_local}'

        horse_event2 = self.ob_config.add_UK_racing_event(number_of_runners=1, runner_names=[self.long_racing_name_1],
                                                          cashout=True, ew_terms=self.ew_terms)

        start_time2 = horse_event2.event_date_time
        start_time_local2 = self.convert_time_to_local(date_time_str=start_time2)
        self.__class__.racing_event_name2 = f'{name_pattern} {start_time_local2}'

        username = tests.settings.betplacement_user
        self.site.login(username=username)

        self.open_betslip_with_selections(selection_ids=[list(horse_event.selection_ids.values())[0],
                                                         list(horse_event2.selection_ids.values())[0]])

        self.place_bet_on_all_available_stakes(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED:
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_each_way_terms(self):
        """
        DESCRIPTION: Verify Each Way terms
        EXPECTED: * Each way terms are displayed if **'isEachWayAvailable' = 'true'** attribute is present in response
        EXPECTED: * Terms correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes from response
        EXPECTED: * Terms are displayed in the following format:
        EXPECTED: "x/y odds - places z,j,k"
        EXPECTED: where:
        EXPECTED: * x = eachWayFactorNum
        EXPECTED: * y= eachWayFactorDen
        EXPECTED: * z,j,k = eachWayPlaces
        """
        bet_name, self.__class__.double_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE (EACH WAY)', event_names=[self.racing_event_name, self.racing_event_name2])
        bet_legs = self.double_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: {bet_name}')
        [self.assertIn(self.each_way, betleg.market_name,
                       msg=f'Each way "{self.each_way}" is not present or not '
                           f'match required format in "{betleg.market_name}"')
         for betleg_name, betleg in bet_legs.items()]

        bet_name, self.__class__.single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='SINGLE (EACH WAY)', event_names=self.racing_event_name)
        bet_legs = self.single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: {bet_name}')
        [self.assertIn(self.each_way, betleg.market_name,
                       msg=f'Each way "{self.each_way}" is not present or not '
                           f'match required format in "{betleg.market_name}"')
         for betleg_name, betleg in bet_legs.items()]

    def test_003_verify_unit_stake_and_total_stake_values(self):
        """
        DESCRIPTION: Verify 'Unit Stake' and 'Total Stake' values correctness
        """
        for bet in (self.single_bet, self.double_bet):
            self.assertEqual(bet.unit_stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                             msg=f'Unit Stake amount "{bet.unit_stake.stake_value}" is not equal '
                                 f'to expected "{self.bet_amount}" for bet "{bet.name}"')

        for bet in (self.single_bet, self.double_bet):
            self.assertEqual(bet.stake.stake_value, '{0:.2f}'.format(self.bet_amount * 2),
                             msg=f'Total Stake amount "{bet.unit_stake.stake_value}" is not equal '
                                 f'to expected "{self.bet_amount*2}" for bet "{bet.name}"')

    def test_004_verify_line_with_too_long_selection_name(self):
        """
        DESCRIPTION: Verify line with too long Selection Name
        EXPECTED: Selection Name is truncated with 3 dots if it is too long to be shown in one line with Odds
        EXPECTED: After the truncation some space is present between Selection Name and Odds
        """
        bet_legs = self.single_bet.items_as_ordered_dict
        [self.assertFalse(betleg.is_outcome_name_truncated(), msg=f'Outcome name "{betleg.outcome_name}" is truncated')
         for betleg_name, betleg in bet_legs.items()]

        bet_legs = self.double_bet.items_as_ordered_dict
        [self.assertFalse(betleg.is_outcome_name_truncated(), msg=f'Outcome name "{betleg.outcome_name}" is truncated')
         for betleg_name, betleg in bet_legs.items()]
