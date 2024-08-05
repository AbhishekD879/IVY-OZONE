import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15392873_Vanilla_Verify_Total_Stake_and_Estimated_Returns_values_calculation(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C15392873
    NAME: [Vanilla] Verify 'Total Stake' and 'Estimated Returns' values calculation
    DESCRIPTION: This test case verifies 'Total Stake' and 'Estimated Returns' values calculation on Quick Bet
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True
    selection_name = []
    lp = {0: '1/2'}
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing event with each way
        EXPECTED: Created event
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP'))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)
            for event in events:
                self.__class__.each_way_market = next((market for market in event['event']['children']
                                                       if market['market']['templateMarketName'] == 'Win or Each Way'), None)['market']
                outcomes_resp = self.each_way_market['children']
                for outcome in outcomes_resp:
                    for child in outcome.get('outcome', {}).get('children', []):
                        if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                            priceNum, priceDen = child['price']['priceNum'], child['price']['priceDen']
                            self.lp[0] = f'{priceNum}/{priceDen}'
                            self.__class__.eventID = event['event']['id']
                            self.selection_name.append(outcome['outcome']['name'])
                            break
                    if self.selection_name:
                        break
                if self.selection_name:
                    break
            if not self.selection_name:
                raise SiteServeException('There are no selections with LP prices')
            self._logger.debug(f'*** Found Horse racing event with id "{self.eventID}"')
        else:
            event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms,
                                                       number_of_runners=1,
                                                       lp_prices=self.lp)
            self.__class__.each_way_market = event.ss_response['event']['children'][0]['market']
            self.__class__.eventID = event.event_id
            self.selection_name.append(list(event.selection_ids.keys())[0])

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage in loaded
        """
        self.site.login()

    def test_002_add_sport_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race> selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        self.add_selection_to_quick_bet(outcome_name=self.selection_name[0])

    def test_003_enter_some_value_in_stake_field(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        self.__class__.quick_bet_value = self.site.quick_bet_panel.selection.content.amount_form.input.value
        self.assertEqual(float(self.quick_bet_value), float(self.bet_amount),
                         msg=f'Actual amount "{float(self.quick_bet_value)}" does not match with '
                             f'expected "{float(self.bet_amount)}"')

    def test_004_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is equal to Stake value entered
        """
        total_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake
        self.assertEqual(float(total_stake), float(self.quick_bet_value),
                         msg=f'Actual Total Stake amount value: "{float(total_stake)}" '
                             f'does not match expected stake value entered: "{float(self.quick_bet_value)}"')

    def test_005_verify_estimated_returns_value(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value
        EXPECTED: 'Estimated Returns' value is calculated based on the formula:
        EXPECTED: **stake * Odds** if Odds has a decimal format
        EXPECTED: **(stake* Odds) + stake** - if Odds has fractional  format
        """
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=[self.lp[0]],
                                      bet_amount=self.bet_amount)

    def test_006_select_ew_option_for_race_selection(self):
        """
        DESCRIPTION: Select 'E/W' option (for <Race> selection)
        EXPECTED: 'E/W' option is selected
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.each_way_checkbox.click()
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way checkbox is not selected')

    def test_007_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is calculated based on the formula:
        EXPECTED: **(stake * 2)**
        """
        actual_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake
        expected_stake = f'{self.bet_amount * 2}'
        self.assertEqual(float(actual_stake), float(expected_stake),
                         msg=f'Actual "Total Stake" value "{float(actual_stake)}" is not same as Expected "{float(expected_stake)}"')

    def test_008_verify_estimated_returns_value(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value
        EXPECTED: 'Estimated Returns' is calculated based on the formula:
        EXPECTED: **Est.Returns  = Return1 + Return2**
        EXPECTED: **Return1 = stake*Odds +stake**
        EXPECTED: **Return2 =  (stake * Odds) * (eachnum*eachden) + stake**
        EXPECTED: 'Estimated Returns' value is equal to **N/A** in case of SP priceType selection added to Quick Bet
        """
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        ew_coef = self.calculate_each_way_coef(self.each_way_market)
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=self.lp[0],
                                      each_way_coef=ew_coef,
                                      bet_amount=self.bet_amount)
