import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.iphone
@pytest.mark.betslip
@pytest.mark.numeric_keyboard
@pytest.mark.mobile_only
@pytest.mark.deeplink
@pytest.mark.high
@vtest
class Test_C2351458_Verify_displaying_numeric_keyboard_for_one_selection(BaseBetSlipTest):
    """
    TR_ID: C2351458
    VOL_ID: C9698026
    NAME: Verify displaying numeric keyboard for one selection
    DESCRIPTION: This test case verifies displaying numeric keyboard for one selection in Betslip
    PRECONDITIONS: - Oxygen application is loaded on Mobile device
    PRECONDITIONS: - One selection is added to the Betslip
    PRECONDITIONS: - Betslip is opened
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    currency = '£'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Open betslip
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self.__class__.team2 = list(self.selection_ids.keys())[1]
            self._logger.info(f'*** Found Football event with selections {self.selection_ids} with team1 "{self.team1}" and team2 "{self.team2}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1 = event.team1
            self.__class__.team2 = event.team2
            self.__class__.selection_ids = event.selection_ids

        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_001_verify_availability_of_numeric_keyboard(self):
        """
        DESCRIPTION: Verify availability of numeric keyboard
        EXPECTED: Numeric keyboard is not opened automatically
        """
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3,
                                                                          expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_002_add_one_more_selection_to_betslip(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        EXPECTED: Added selection is displayed on Bet Slip
        EXPECTED: Numeric keyboard is NOT shown above 'BET NOW'/LOG IN & BET' button
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team2])
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team2)
        self.assertTrue(stake, msg=f'{self.team2} stake was not found')
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_003_remove_one_selection_using_bin_icon_within_section_section(self):
        """
        DESCRIPTION: Remove one selection using 'Bin' icon within section section
        EXPECTED: Betslip content is reloaded
        EXPECTED: One selection is displayed on Bet Slip
        EXPECTED: Numeric keyboard is not shown above 'BET NOW'/LOG IN & BET' button
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team2)
        self.assertTrue(stake, msg=f'{self.team2} stake was not found')
        stake.remove_button.click()
        singles_section = self.get_betslip_sections().Singles
        self.assertEqual(len(singles_section.items()), 1, msg='Only one Stake must be found in betslip Singles section')

        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3,
                                                                          expected_result=False),
                         msg='Betslip keyboard is not hidden')
