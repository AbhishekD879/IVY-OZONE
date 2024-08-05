import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.slow
@vtest
class Test_C29037_Multiples_ordering(BaseBetSlipTest):
    """
    TR_ID: C29037
    NAME: Multiples ordering
    DESCRIPTION:
    PRECONDITIONS: Note: Multiples may not be available after adding Special events to the Betslip.
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_create_events(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(number_of_events=4)
            selections = []
            for event in events:
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Match Betting' and market['market'].get('children'):
                        selections.append(market['market']['children'][0]['outcome']['id'])
                        break

            self.__class__.selection_id_1 = selections[0]
            self.__class__.selection_id_2 = selections[1]
            self.__class__.selection_id_3 = selections[2]
            self.__class__.selection_id_4 = selections[3]
        else:
            self.__class__.selection_id_1 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
            self.__class__.selection_id_2 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
            self.__class__.selection_id_3 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
            self.__class__.selection_id_4 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]

    def test_002_add_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections from different events to the betslip
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_003_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: Multiples are available for added selections
        """
        sections = self.get_betslip_sections(multiples=True, timeout=10)
        self.__class__.multiples_section = sections.Multiples

        self.assertTrue(self.multiples_section, msg='*** No Multiple stakes found')

    def test_004_verify_order_of_multiples(self):
        """
        DESCRIPTION: Verify order of Multiples
        EXPECTED: *   'Double' bet type is the first in the list at any time
        EXPECTED: *   The rest bet types are displayed below as they are returned from OpenBet
        """
        stake_name, stake = list(self.multiples_section.items())[0]
        self.assertEqual(stake_name, vec.betslip.DBL,
                         msg=f'First section is "{stake_name}" not "{vec.betslip.DBL}"')

    def test_005_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: Bet is removed from Betslip successfully
        """
        self.clear_betslip()

    def test_006_add_three_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add three selections from different events to the betslip
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2, self.selection_id_3),
                                          timeout=10)

    def test_007_verify_order_of_multiples(self):
        """
        DESCRIPTION: Verify order of Multiples
        EXPECTED: *   'Treble' bet type is the first in the list at any time
        EXPECTED: *   The rest bet types are displayed below as they are returned from OpenBet
        """
        sections = self.get_betslip_sections(multiples=True, timeout=10)
        multiples_section = sections.Multiples

        stake_name, stake = list(multiples_section.items())[0]
        self.assertEqual(stake_name, vec.betslip.TBL,
                         msg=f'First section is "{stake_name}" not "{vec.betslip.TBL}"')

    def test_008_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED:
        """
        self.test_005_clear_betslip()

    def test_009_add_three_or_more_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add three or more selections from different events to the betslip
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1,
                                                         self.selection_id_2,
                                                         self.selection_id_3,
                                                         self.selection_id_4),
                                          timeout=10)

    def test_010_verify_order_of_multiples(self):
        """
        DESCRIPTION: Verify order of Multiples
        EXPECTED: *   'Accumulator(X)' bet type is the first in the list at any time, where (X) - number of added single selections
        EXPECTED: *   The rest bet types are displayed below as they are returned from OpenBet
        """
        sections = self.get_betslip_sections(multiples=True, timeout=5)
        multiples_section, self.__class__.singles_section = sections.Multiples, sections.Singles
        stake_name, stake = list(multiples_section.items())[0]
        self.assertEqual(stake_name, vec.betslip.ACC4,
                         msg=f'First section is "{stake_name}" not "{vec.betslip.ACC4}"')

    def test_011_manually_remove_selections_to_leave_in_the_betslip_three_selections(self):
        """
        DESCRIPTION: Manually remove selection(s) to leave in the betslip three selections
        EXPECTED: Multiples are rebuilt
        """
        stake_name, stake = list(self.singles_section.items())[0]
        stake.remove_button.click()

    def test_012_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step №7
        EXPECTED:
        """
        self.test_007_verify_order_of_multiples()

    def test_013_manually_remove_selection_to_leave_in_the_betslip_two_selections(self):
        """
        DESCRIPTION: Manually remove selection to leave in the betslip two selections
        EXPECTED: Multiples are rebuilt
        """
        sections = self.get_betslip_sections()
        singles_section = sections.Singles
        stake_name, stake = list(singles_section.items())[0]
        stake.remove_button.click()

    def test_014_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps №3-4
        EXPECTED:
        """
        self.test_003_go_to_betslip()
        self.test_004_verify_order_of_multiples()
