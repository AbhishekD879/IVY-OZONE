import re

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.est_returns
@vtest
class Test_C29039_Multiples_Stake_and_Est_Returns_LP_Price_Type(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C29039
    NAME: Multiples Stake and Est Returns - LP Price Type
    DESCRIPTION: This test case verifies calculations of 'Stake', 'Est. Returns', 'Total Stake'
    DESCRIPTION: and 'Total Est. Returns' fields for Multiples
    PRECONDITIONS: 1. In order to check the potential payout value for multiple bets please go to
    PRECONDITIONS:    Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: * For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: * For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    """
    keep_browser_open = True
    currency = '£'
    prices = {0: '1/2', 1: '2/3'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create events
        DESCRIPTION: PROD: Find events in SS
        EXPECTED: Events are created/found
        """
        if tests.settings.backend_env != 'prod':
            event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.prices)
            self.__class__.selection_id_1 = list(event_params1.selection_ids.values())[0]

            event_params2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2, lp_prices=self.prices)
            self.__class__.selection_id_2 = list(event_params2.selection_ids.values())[0]

            event_params3 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2, lp_prices=self.prices)
            self.__class__.selection_id_3 = list(event_params3.selection_ids.values())[0]
        else:
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP')), \
                exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE))
            events = self.get_active_events_for_category(all_available_events=True,
                                                         additional_filters=additional_filter,
                                                         expected_template_market='Win or Each Way',
                                                         category_id=self.ob_config.horseracing_config.category_id)
            selections = []
            for event in events:
                outcomes = next(((market['market'].get('children')) for market in event['event']['children']
                                 if 'LP' in market['market']['priceTypeCodes'] and market['market'].get('children')), None)
                if not outcomes:
                    raise SiteServeException(f'There are no available outcomes in "{event["event"]["name"]}" with LP prices')
                selection_id = None
                for outcome in outcomes:
                    if outcome['outcome'].get('children'):
                        for child in outcome['outcome']['children']:
                            if child.get('price'):
                                if 'LP' in child.get('price').get('priceType'):
                                    if 'Unnamed' not in outcome['outcome']['name']:
                                        selection_id = outcome['outcome']['id']
                                break
                        break
                if not selection_id:
                    continue
                selections.append(selection_id)
                if len(selections) == 3:
                    break
            if len(selections) < 3:
                raise SiteServeException('There is no available selection id with LP price')

            self.__class__.selection_id_1 = selections[0]
            self.__class__.selection_id_2 = selections[1]
            self.__class__.selection_id_3 = selections[2]
            self._logger.info(f'*** Found selection ids: [{self.selection_id_1, self.selection_id_2, self.selection_id_3}]')

    def test_001_add_several_selections_with_lp_price_type_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections with 'LP' price type from different events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id_1, self.selection_id_2, self.selection_id_3])

    def test_002_go_to_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to Betslip-> 'Multiples' section
        EXPECTED: * 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: * Multiples are available for added selections
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        self.__class__.stake_name, self.__class__.stake = list(multiples_section.items())[0]

    def test_003_verify_est_returns(self):
        """
        DESCRIPTION: Verify 'Est. Returns' field
        EXPECTED: 'Total Est. Returns' = £0.00
        """
        est_returns = self.stake.est_returns
        actual_est_returns = self.currency + str(est_returns)
        expected_est_returns = '£0.00'
        self.assertEqual(actual_est_returns, expected_est_returns,
                         msg='Est. Returns field: "%s" is not as expected: "%s"' %
                             (actual_est_returns, expected_est_returns))

    def test_004_verify_total_stake(self):
        """
        DESCRIPTION: Verify 'Total Stake' field
        EXPECTED: Total Stake' = £0.00
        """
        total_stake = self.get_betslip_content().total_stake
        actual_total_stake = self.currency + str(total_stake)
        expected_total_stake = '£0.00'
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg='Totals Stake value: "%s" is not as expected: "%s"' %
                             (actual_total_stake, expected_total_stake))

    def test_005_verify_total_est_returns(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' field
        EXPECTED: 'Total Est. Returns' = £0.00
        """
        total_est_returns = self.get_betslip_content().total_estimate_returns
        actual_total_est_returns = self.currency + str(total_est_returns)
        expected_total_est_returns = '£0.00'
        self.assertEqual(actual_total_est_returns, expected_total_est_returns,
                         msg='Totals Est. Returns field: "%s" is not as expected: "%s"' %
                             (actual_total_est_returns, expected_total_est_returns))

    def test_006_enter_stake_for_one_of_available_multiple_types_and_check_received_potential_payout_value(self):
        """
        DESCRIPTION: Enter 'Stake' for one of available Multiple Types and check received potential payout value
        EXPECTED: * **'Total Stake'** field corresponds to entered 'Stake' multiplied by the number
        EXPECTED:   of bets included in a Multiple Type.
        EXPECTED: * 'Est. Returns' and 'Total Est. Returns' are calculated for this Multiple Type
        # TODO: https://jira.egalacoral.com/browse/VOL-1492
        EXPECTED: * Potential payout value is received in response for appropriate Multiple Type
        # TODO: https://jira.egalacoral.com/browse/VOL-1791
        EXPECTED: * **'Est. Returns'** and **'Total Est. Returns'** values on front-end correspond
        EXPECTED:   to Potential payout value
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        entered_stake = self.stake.amount_form.input.value
        number_of_bets = re.sub("[x()]", '', self.stake.bets_multiplier)
        actual_total_stake = self.get_betslip_content().total_stake
        expected_total_stake = float(entered_stake) * (int(number_of_bets) if number_of_bets else 1)
        amount = '{:.2f}'.format(expected_total_stake)
        self.assertEqual(actual_total_stake, amount,
                         msg='Actual Total Stake value: "%s" does not correspond entered Stake value: "%s"' %
                             (actual_total_stake, amount))
        self.stake.amount_form.input.value = ''

    def test_007_enter_stake_for_a_few_of_available_multiple_types(self):
        """
        DESCRIPTION: Enter 'Stake' for a few of available Multiple Types
        EXPECTED: * **'Total Stake'** field is a sum of all entered 'Stakes' multiplied by the number
        EXPECTED:   of bets included in a Multiple Type.
        # TODO: https://jira.egalacoral.com/browse/VOL-1791
        EXPECTED: * **'Total Est. Returns'** field is a sum of all 'Est. Returns'.
        """
        sections = self.get_betslip_sections(multiples=True)
        stake = sections.Multiples.get('Double')
        self.assertTrue(stake, msg='"Double" stake not found')
        self.enter_stake_amount(stake=(stake.name, stake))
        number_of_bets = int(re.sub("[x()]", '', stake.bets_multiplier))
        stake = sections.Multiples.get('Trixie')
        if stake:
            self.enter_stake_amount(stake=(stake.name, stake))
            number_of_bets += int(re.sub("[x()]", '', stake.bets_multiplier))
        entered_stake = stake.amount_form.input.value
        actual_total_stake = self.get_betslip_content().total_stake
        expected_total_stake = float(entered_stake) * int(number_of_bets)
        self.assertAlmostEqual(float(actual_total_stake), expected_total_stake, delta=0.01,
                               msg=f'Actual Total Stake value: "{actual_total_stake}" does not correspond entered '
                                   f'Stake value: "{expected_total_stake}" within 0.01 delta')
