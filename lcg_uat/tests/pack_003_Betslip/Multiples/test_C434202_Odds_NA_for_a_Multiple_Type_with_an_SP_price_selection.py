import pytest
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.racing
@pytest.mark.horseracing
@vtest
class Test_C434202_Odds_NA_for_a_Multiple_Type_with_an_SP_price_selection(BaseBetSlipTest):
    """
    TR_ID: C434202
    NAME: Odds N/A for a Multiple Type with an SP price selection
    DESCRIPTION: This test case verifies displaying N/A odds for a Multiple in case if one of the selections contains Races event (SP price only)
    PRECONDITIONS: 1. In order to check the potential payout value for multiple bets please go to Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: * For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: * For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: create events
        """
        if tests.settings.backend_env != 'prod':
            event_params_sp = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=2, sp=True, lp=False)
            self.__class__.event = list(event_params_sp.selection_ids.keys())[0]
            self.__class__.selection_id_SP = list(event_params_sp.selection_ids.values())[0]

            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team_1 = event_params.team1
            self.__class__.selection_id_football_1 = event_params.selection_ids[self.team_1]

            event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team_2 = event_params_2.team2
            self.__class__.selection_id_football_2 = event_params_2.selection_ids[self.team_2]
        else:
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'SP'))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)
            event, selection_id, selection_name = None, None, None
            for event in events:
                for market in event['event']['children']:
                    if market['market'].get('children') and market.get('market').get(
                            'templateMarketName') == 'Win or Each Way':
                        for outcome in market['market']['children']:
                            if not outcome['outcome'].get(
                                    'children') and 'Unnamed' not in outcome['outcome'].get('name'):  # outcomes that does not have children are usually outcomes with SP prices
                                selection_id = outcome['outcome']['id']
                                selection_name = outcome['outcome']['name']
                                break
                        break
                if selection_id:
                    break
            outcomes = selection_id
            if not outcomes:
                raise SiteServeException('There are no selections with SP prices')

            self.__class__.selection_id_SP = selection_id
            self.__class__.event = selection_name

            events = self.get_active_events_for_category(number_of_events=2)
            selection_ids = []
            selections_names = []
            for event in events:
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Match Betting' and market['market'].get('children'):
                        selection_ids.append(market['market']['children'][0]['outcome']['id'])
                        selections_names.append(market['market']['children'][0]['outcome']['name'])
                        break
            self.__class__.selection_id_football_1 = selection_ids[0]
            self.__class__.selection_id_football_2 = selection_ids[1]

            self.__class__.team_1 = selections_names[0]
            self.__class__.team_2 = selections_names[1]

    def test_001_add_two_selections_from_different_events_to_the_betslip_one_of_which_is_from_races_with_sp_price(self):
        """
        DESCRIPTION: Add two selections from different events to the Betslip one of which is from Races with SP price
        EXPECTED: Events are added to the Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_SP, self.selection_id_football_1))
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.multiples_section = sections.Multiples
        singles_section = sections.Singles
        list_of_outcomes = list(singles_section.keys())

        self.assertIn(self.team_1, list_of_outcomes,
                      msg=f'{self.team_1} is not added to the Betslip')
        self.assertIn(self.event, list_of_outcomes,
                      msg=f'{self.event} is not added to the Betslip')

    def test_002_go_to_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to Betslip->'Multiples' section
        EXPECTED: * Multiples are available for added selections
        EXPECTED: * Odds and 'Est. Returns' value for a Multiple Type Double(1) is 'N/A'
        """
        self.assertTrue(self.multiples_section, msg='*** No Multiple stakes found')
        stake_name, self.__class__.stake = list(self.multiples_section.items())[0]

        self.assertEqual(stake_name, 'Double', msg='Section name is "%s" not "Double"' % stake_name)

        self.assertEqual(self.stake.odds, 'N/A', msg=f'Odds are not the same as expected. '
                                                     f'Actual: {self.stake.odds}. Expected: "N/A"')
        self.assertEqual(self.stake.est_returns, 'N/A', msg=f'Est. Returns are not the same as expected.'
                                                            f'Actual: {self.stake.est_returns}. Expected: "N/A".')

    def test_003_enter_stake_for_available_multiple_type_and_check_received_potential_payout_value(self):
        """
        DESCRIPTION: Enter 'Stake' for available Multiple Type and check received potential payout value
        EXPECTED: * 'Total Est. Returns' field contains "N/A"
        EXPECTED: * Potential payout values is NOT received in response for an appropriate Multiple Type
        """
        # TODO https://jira.egalacoral.com/browse/VOL-1815

        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.assertEqual(self.get_betslip_content().total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns are not the same as expected. '
                             f'Actual: {self.get_betslip_content().total_estimate_returns}. Expected: "N/A"')

    def test_004_add_one_or_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add one or more selections to the Betslip
        EXPECTED: Events are added to the Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_football_2)

        singles_section = self.get_betslip_sections().Singles
        expected_outcomes = list(singles_section.keys())

        self.assertIn(self.team_1, expected_outcomes,
                      msg=f'{self.team_1} is not added to the Betslip')
        self.assertIn(self.team_2, expected_outcomes,
                      msg=f'{self.team_2} is not added to the Betslip')
        self.assertIn(self.event, expected_outcomes,
                      msg=f'{self.event} is not added to the Betslip')

    def test_005_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: * Place your ACCA section is displayed with corresponding Multiple Type (Treble/Accumulator) on the top of the Betslip
        EXPECTED: * Odds and 'Est. Returns' value for a Multiple Type (Treble/Accumulator) is 'N/A'
        """
        sections = self.get_betslip_sections(multiples=True).Multiples

        stake_name, self.__class__.stake = list(sections.items())[0]
        self.assertEqual(stake_name, 'Treble', msg='Section name is "%s" not "Treble"' % stake_name)

        self.assertEqual(self.stake.odds, 'N/A', msg=f'Odds are not the same as expected. '
                                                     f'Actual: {self.stake.odds}. Expected: "N/A"')
        self.assertEqual(self.stake.est_returns, 'N/A', msg=f'Est. Returns are not the same as expected.'
                                                            f'Actual: {self.stake.est_returns}. Expected: "N/A".')

    def test_006_enter_stake_for_available_multiple_type_in_place_your_acca_section_and_check_received_potential_payout_value(self):
        """
        DESCRIPTION: Enter 'Stake' for available Multiple Type in 'Place Your ACCA' section and check received potential payout value
        EXPECTED: * 'Total Est. Returns' field contains "N/A"
        EXPECTED: * Potential payout value is NOT received in response for an appropriate Multiple Type
        """
        # TODO https://jira.egalacoral.com/browse/VOL-1815

        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.assertEqual(self.get_betslip_content().total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns are not the same as expected. '
                             f'Actual: {self.get_betslip_content().total_estimate_returns}. Expected: "N/A"')
