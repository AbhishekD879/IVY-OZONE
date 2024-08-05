import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.medium
@pytest.mark.bet_placement
@pytest.mark.each_way
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C536586_Each_Way_option_for_Race_Multiples(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C536586
    NAME: Each Way option for Race Multiples
    DESCRIPTION: This test case verifies Each Way option for Multiples
    PRECONDITIONS: 1.  Make sure you have the following selections available:
    PRECONDITIONS: - <Race> selections from markets with Each Way option available from different events
    PRECONDITIONS: 2.  User is logged and has positive balance
    PRECONDITIONS: 3. To get information about selected event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: USE *'isEachWayAvailable'* on market level to see whether Each Way checkbox should be displayed on the Bet Slip
    """
    keep_browser_open = True
    bet_amount = 2.0
    number_of_double_bets = 3

    def test_000_create_test_event_and_login(self):
        """
        DESCRIPTION: Create racing test event
        EXPECTED: Event is created
        """
        event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
        self.__class__.selection_ids = list(event_parameters.selection_ids.values())[0]
        event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
        self.__class__.selection_ids_2 = list(event_parameters.selection_ids.values())[0]
        event_parameters = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
        self.__class__.selection_ids_3 = list(event_parameters.selection_ids.values())[0]
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_add_three_or_more_race_selections_from_markets_with_each_way_option_available_from_different_events(self):
        """
        DESCRIPTION: Add three or more <Race> selections from markets with Each Way option available from different events
        EXPECTED: Selections are added to the betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids, self.selection_ids_2, self.selection_ids_3))

    def test_002_verify_multiples_section(self):
        """
        DESCRIPTION: Verify Multiples section
        EXPECTED: - Each Multiple within 'Multiples' section contains 'Each Way' check box
        EXPECTED: - Each Way check box is NOT selected by default for Multiples
        """
        self.__class__.sections = self.get_betslip_sections(multiples=True)
        multiples_section = self.sections.Multiples
        for stake_name, stake in multiples_section.items():
            self.assertTrue(stake.has_each_way_checkbox,
                            msg=f'Each Way checkbox is not present on "{stake_name}" stake')
            self.assertFalse(stake.each_way_checkbox.is_selected(),
                             msg=f'Each Way is selected by default, while shouldn\'t on "{stake_name}" stake')

    def test_003_place_a_bet_on_multiple_with_valid_stake_and_each_way_checkbox_selected(self):
        """
        DESCRIPTION: Place a bet on Multiple with valid stake and 'Each Way' checkbox selected
        EXPECTED: - 'Stake' value corresponds to the entered stake
        EXPECTED: - Total Stake for selected Multiple is doubled
        EXPECTED: - Bet is placed successfully
        """
        bet_info = self.place_and_validate_multiple_bet(multiples=True, each_way=True, number_of_stakes=1)
        total_stake_actual = float(bet_info['total_stake'])
        unit_stake = float(bet_info[vec.betslip.TBL]['unit_stake'])
        self.assertEqual(unit_stake, self.bet_amount,
                         msg=f'Stake value "{unit_stake}" is not corresponding '
                         f'to the entered stake "{self.bet_amount}"')
        total_stake_expected = float(self.bet_amount) * 2
        self.assertEqual(total_stake_actual,
                         total_stake_expected,
                         msg=f'Each Way selection should double Total Stake Amount. '
                         f'Total stake is "{total_stake_actual}", should be "{total_stake_expected}"')
        self.check_bet_receipt_is_displayed()
