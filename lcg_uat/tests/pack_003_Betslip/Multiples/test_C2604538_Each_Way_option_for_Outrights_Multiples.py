import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.football
@pytest.mark.each_way
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C2604538_Each_Way_option_for_Outrights_Multiples(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2604538
    NAME: Each Way option for Outrights Multiples
    DESCRIPTION: This test case verifies Each Way option for Multiples created from Outrights
    PRECONDITIONS: 1.  Make sure you have the following selections available:
    PRECONDITIONS: - <Sport> selections from markets with Each Way option available from different Outright events
    PRECONDITIONS: 2.  To get information about selected event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: USE *'isEachWayAvailable'* on market level to see whether Each Way checkbox should be displayed on the Bet Slip
    """
    keep_browser_open = True
    number_of_double_bets = 3

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with Each Way terms available and log in
        """
        event_parameters = self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms)
        event_parameters_2 = self.ob_config.add_england_premier_league_football_outright_event(ew_terms=self.ew_terms)
        event_parameters_3 = self.ob_config.add_spain_la_liga_football_outright_event(ew_terms=self.ew_terms)
        self.__class__.selection_names = (list(event_parameters.selection_ids.keys())[0],
                                          list(event_parameters_2.selection_ids.keys())[0],
                                          list(event_parameters_3.selection_ids.keys())[0])
        self.__class__.user = tests.settings.betplacement_user
        self.__class__.selection_ids = (list(event_parameters.selection_ids.values())[0],
                                        list(event_parameters_2.selection_ids.values())[0],
                                        list(event_parameters_3.selection_ids.values())[0])
        self.site.login(username=self.user)

    def test_001_add_two_or_more_sport_selections_from_markets_with_each_way_option_available_from_different_outright_events(self):
        """
        DESCRIPTION: Add two or more <Sport> selections from markets with Each Way option available from different Outright events
        EXPECTED: Selections are added to the betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selection is displayed on the Betslip
        """
        self.__class__.sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(self.sections, msg='No stakes found')
        for actual_selection in self.sections.Singles:
            self.assertIn(actual_selection, self.selection_names,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{self.selection_names}"')

    def test_003_verify_multiples_section(self):
        """
        DESCRIPTION: Verify Multiples section
        EXPECTED: - Each Multiple within 'Multiples' section contain 'Each Way' check box if all added selections have 'Each Way' option available
        EXPECTED: - Each Way check box is NOT selected by default for Multiples
        """
        multiples_section = self.sections.Multiples
        for stake_name, stake in multiples_section.items():
            self.assertTrue(stake.has_each_way_checkbox,
                            msg=f'Each Way checkbox is not present on "{stake_name}" stake')
            self.assertFalse(stake.each_way_checkbox.is_selected(),
                             msg=f'Each Way is selected by default, while shouldn\'t on "{stake_name}" stake')

    def test_004_place_a_bet_on_multiple_with_valid_stake_and_each_way_checkbox_selected(self):
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
