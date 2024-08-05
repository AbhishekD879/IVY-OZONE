import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.critical
@vtest
class Test_C29036_Multiples_are_available(BaseBetSlipTest):
    """
    TR_ID: C29036
    NAME: Multiples are available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Invictus application, create events
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(number_of_events=3)
            selections = []
            for event in events:
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Match Betting' and market['market'].get('children'):
                        selections.append(market['market']['children'][0]['outcome']['id'])
                        break

            self.__class__.selection_id_1 = selections[0]
            self.__class__.selection_id_2 = selections[1]
            self.__class__.selection_id_3 = selections[2]
        else:
            self.__class__.selection_id_1 = list(
                self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
            self.__class__.selection_id_2 = list(
                self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
            self.__class__.selection_id_3 = list(
                self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]

    def test_001_add_several_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        EXPECTED: Go to Betslip
        EXPECTED: 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: Multiples are available for added selections
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_002_verify_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        EXPECTED: Go to Betslip
        EXPECTED: 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: Multiples are available for added selections
        """
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        multiples_section_stakes = multiples_section.keys()
        self.__class__.number_of_multiple_stakes = len(multiples_section_stakes)

    def test_003_add_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add more selections to the Betslip
        EXPECTED: List of available Multiples is updated, more Multiple types are available
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_3)

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        self.__class__.singles_section_stakes = singles_section
        self.assertTrue(len(singles_section.keys()) == 3,
                        msg=f'Should be present 3 Single stakes, but found "{len(singles_section.keys())}"')

        self.assertTrue(self.number_of_multiple_stakes < len(multiples_section.keys()),
                        msg=f'Should be present more than "{self.number_of_multiple_stakes}" stakes '
                            f'but found "{len(multiples_section.keys())}"')
        self.__class__.number_of_multiple_stakes = len(multiples_section.keys())

    def test_004_remove_some_selections(self):
        """
        DESCRIPTION: Remove some selections
        EXPECTED: List of Multiples is updated
        """
        stake = list(self.singles_section_stakes.values())[0]
        stake.remove_button.click()

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        self.assertTrue(len(singles_section.keys()) == 2,
                        msg=f'Should be present 3 Single stakes, but found "{len(singles_section.keys())}"')

        self.assertTrue(self.number_of_multiple_stakes > len(multiples_section.keys()),
                        msg=f'Should be present less than "{self.number_of_multiple_stakes}" stakes '
                            f'but found "{len(multiples_section.keys())}"')
        self.__class__.number_of_multiple_stakes = len(multiples_section.keys())

    def test_005_leave_only_1_selection_in_the_betslip(self):
        """
        DESCRIPTION: Leave only 1 selection in the Betslip
        EXPECTED: Multiples are not available for 1 selection
        """
        singles_section = self.get_betslip_sections(multiples=True).Singles
        stake = list(singles_section.values())[0]
        stake.remove_button.click()

        betslip_sections = wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                           timeout=1,
                                           name='Betslip sections to load')
        self.assertTrue(betslip_sections, msg='*** No bets found')
        self.assertTrue(vec.betslip.BETSLIP_SINGLES_NAME in betslip_sections.keys(), msg='SINGLES section is not found')
        stakes = betslip_sections[vec.betslip.BETSLIP_SINGLES_NAME]
        self.assertTrue(stakes, msg='*** No Single stakes found')
        self.assertTrue(len(stakes.keys()) == 1,
                        msg=f'Should be present 1 Single stakes, but found "{len(stakes.keys())}"')

        self.assertTrue(vec.betslip.MULTIPLES not in betslip_sections.keys(),
                        msg=f'Section "{vec.betslip.MULTIPLES}" should not be displayed on BetSlip page')
