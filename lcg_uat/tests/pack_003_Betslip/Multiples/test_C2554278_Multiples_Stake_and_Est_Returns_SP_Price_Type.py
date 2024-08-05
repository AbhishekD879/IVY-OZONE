import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
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
@pytest.mark.safari
@vtest
class Test_C2554278_Multiples_Stake_and_Est_Returns_SP_Price_Type(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2554278
    NAME: Multiples Stake and Est Returns - SP Price Type
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

    def find_sp_hr_selection(self, events):
        selection_id = None
        for event in events:
            for market in event['event']['children']:
                if market['market'].get('children') and market.get('market').get(
                        'templateMarketName') == 'Win or Each Way':
                    for outcome in market['market']['children']:
                        if not outcome['outcome'].get(
                                'children') and 'Unnamed' not in outcome['outcome'].get('name'):  # outcomes that does not have children are usually outcomes with SP prices
                            events.remove(event)
                            selection_id = outcome['outcome']['id']
                            return selection_id
                    break
            if selection_id:
                break
        if not selection_id:
            raise SiteServeException('There are no selections with SP prices')

    def test_000_create_test_events(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env != 'prod':
            event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2)
            self.__class__.selection_id_1 = list(event_params1.selection_ids.values())[0]

            event_params2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2)
            self.__class__.selection_id_2 = list(event_params2.selection_ids.values())[0]
        else:
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'SP'))
            events = self.get_active_events_for_category(additional_filters=additional_filter,
                                                         category_id=self.ob_config.horseracing_config.category_id,
                                                         all_available_events=True)

            self.__class__.selection_id_1 = self.find_sp_hr_selection(events)
            self.__class__.selection_id_2 = self.find_sp_hr_selection(events)

    def test_001_add_several_selections_with_sp_price_type_from_different_race_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections with 'SP' price type from different <Race> events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id_1, self.selection_id_2])

    def test_002_go_to_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to Betslip-> 'Multiples' section
        EXPECTED: 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: Multiples are available for added selections
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        self.__class__.stake_name, self.__class__.stake = list(multiples_section.items())[0]

    def test_003_verify_est_returns(self):
        """
        DESCRIPTION: Verify 'Est. Returns'
        EXPECTED: 'Est. Returns' field contains "N/A"
        """
        actual_est_returns = self.stake.est_returns
        expected_est_returns = 'N/A'
        self.assertEqual(actual_est_returns, expected_est_returns,
                         msg='Est. Returns field: "%s" is not as expected: "%s"' %
                             (actual_est_returns, expected_est_returns))

    def test_004_verify_total_stake(self):
        """
        DESCRIPTION: Verify 'Total Stake' field
        EXPECTED: 'Total Stake' = £0.00
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
        EXPECTED: 'Total Est. Returns' = £0.00
        """
        total_est_returns = self.get_betslip_content().total_estimate_returns
        actual_total_est_returns = self.currency + str(total_est_returns)
        expected_total_est_returns = '£0.00'
        self.assertEqual(actual_total_est_returns, expected_total_est_returns,
                         msg='Totals Est. Returns field: "%s" is not as expected: "%s"' %
                             (actual_total_est_returns, expected_total_est_returns))

    def test_006_enter_stake_for_at_least_one_of_available_multiple_types(self):
        """
        DESCRIPTION: Enter 'Stake' for at least one of available Multiple Types
        EXPECTED: * **'Total Stake'** field corresponds to entered 'Stake' multiplied by
        EXPECTED:   the number of bets included in a Multiple Type.
        EXPECTED: * **'Est. Returns'** and **'Total Est. Returns'** contain "N/A"
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        entered_stake = f'{float(self.stake.amount_form.input.value):.2f}'
        total_stake = f'{float(self.get_betslip_content().total_stake):.2f}'
        self.assertEqual(total_stake, entered_stake,
                         msg='Total Stake value: "%s" does not corresponds entered Stake value: "%s"' %
                             (total_stake, entered_stake))
        self.test_003_verify_est_returns()
        actual_total_est_returns = self.get_betslip_content().total_estimate_returns
        expected_total_est_returns = 'N/A'
        self.assertEqual(actual_total_est_returns, expected_total_est_returns,
                         msg='Totals Est. Returns field: "%s" is not as expected: "%s"' %
                             (actual_total_est_returns, expected_total_est_returns))
