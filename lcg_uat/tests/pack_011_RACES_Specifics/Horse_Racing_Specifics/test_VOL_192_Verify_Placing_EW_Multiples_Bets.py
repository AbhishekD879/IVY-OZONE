import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.smoke
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.betslip
@pytest.mark.each_way
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.medium
@pytest.mark.pipelines
@pytest.mark.login
@vtest
class Test_VOL_192_Verify_Placing_EW_Multiples_Bets(BaseRacing, BaseBetSlipTest):
    """
    NAME: Place E/W Multiples bet
    DESCRIPTION: Due to OCC BMA-21781 INC0495993 - Unable to place E/W trebles on mobile
    """
    keep_browser_open = True
    selection_ids_2, selection_ids_3 = None, None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events with Each Way terms available
        EXPECTED: Racing events with Each Way terms are created
        """
        if tests.settings.backend_env == 'prod':

            ew_available_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            events = \
                self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                    additional_filters=ew_available_filter,
                                                    number_of_events=3)
            selections = []
            for event in events:
                outcomes = next((market_info['market']['children'] for market_info in event['event']['children'] if
                                 'Win or Each Way' == market_info['market']['name']), None)
                for outcome in outcomes:
                    outcome_name = outcome['outcome']['name']
                    if 'Unnamed' not in outcome_name and 'N/R' not in outcome_name:
                        selections.append(outcome['outcome']['id'])
                        break
            if len(selections) != 3:
                raise SiteServeException('Not enough Horse events found')
            self.__class__.selection_ids, self.__class__.selection_ids_2, self.__class__.selection_ids_3 = selections
        else:
            event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
            self.__class__.selection_ids = list(event_parameters.selection_ids.values())[0]
            event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
            self.__class__.selection_ids_2 = list(event_parameters.selection_ids.values())[0]
            event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
            self.__class__.selection_ids_3 = list(event_parameters.selection_ids.values())[0]

    def test_001_login_and_add_two_selections_to_betslip(self):
        """
        DESCRIPTION: Login into app
        DESCRIPTION: Add two selections to betslip
        EXPECTED: User is logged in
        EXPECTED: Betslip is opened with selections added
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=(self.selection_ids, self.selection_ids_2))

    def test_002_check_terms_displaying(self):
        """
        DESCRIPTION: Check E/W terms displaying on each Stake
        EXPECTED: Each-way terms checkbox is present on each Stake
        """
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        for stake_name, stake in dict(singles_section.items() + multiples_section.items()).items():
            ew = stake.has_each_way_checkbox()
            self.assertTrue(ew, msg=f'Each Way checkbox is not present on "{stake_name}" stake')

    def test_003_place_multiples_bet(self):
        """
        DESCRIPTION: Place Multiples E/W bet
        EXPECTED: Bet is placed successfully
        """
        self.place_multiple_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_004_add_three_selections_to_betslip(self):
        """
        DESCRIPTION: Add two selections to betslip
        EXPECTED: Betslip is opened with selections added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids, self.selection_ids_2, self.selection_ids_3))

    def test_005_check_terms_displaying(self):
        """
        DESCRIPTION: Check E/W terms displaying on each Stake
        EXPECTED: Each-way terms checkbox is present on each Stake
        """
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        for stake_name, stake in dict(singles_section.items() + multiples_section.items()).items():
            ew = stake.has_each_way_checkbox()
            self.assertTrue(ew, msg=f'Each Way checkbox is not present on "{stake_name}" stake')

    def test_006_place_multiple_bet(self):
        """
        DESCRIPTION: Place Multiple E/W bet
        EXPECTED: Bet is placed successfully
        """
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
