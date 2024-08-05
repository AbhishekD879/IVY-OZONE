import pytest
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.high
@vtest
class Test_C370841_Verify_All_Stakes_stake_field(BaseBetSlipTest):
    """
    TR_ID: C370841
    NAME: Verify All single stakes stake field
    DESCRIPTION: This test case verifies 'All Stakes' stake field in the betslip
    PRECONDITIONS: Note: 'All single stakes' functionality is the same for mobile/tablet/desktop views
    """
    keep_browser_open = True
    selection_ids_2 = None
    default_amount_value = vec.quickbet.DEFAULT_AMOUNT_VALUE

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Invictus application, create event
        """
        event_params1 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.first_selection, self.__class__.selection_ids = event_params1.team1, event_params1.selection_ids
        event_params2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.second_selection, self.__class__.selection_ids_2 = event_params2.team1, event_params2.selection_ids

    def test_001_add_one_selection_to_the_betslip_from_any_area(self):
        """
        DESCRIPTION: Add ONE selection to the betslip from any area of the application -> Open/observe betslip
        EXPECTED: Selection is added
        EXPECTED: 'All single stakes' field is NOT present in the betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.first_selection]))
        section = self.get_betslip_sections().Singles
        self.assertFalse(section.has_all_stakes(expected_result=False), msg='All stakes block is found')
        self.remove_stake(name=self.first_selection)
        self.__class__.expected_betslip_counter_value = 0

    def test_002_add_more_selections_to_the_betslip_open_observe_betslip(self):
        """
        DESCRIPTION: Add  more selections to the betslip -> Open/observe betslip
        EXPECTED: Selections are added
        EXPECTED: 'All single stakes' field is shown above all singles within 'Singles' section
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.first_selection],
                                                         self.selection_ids_2[self.second_selection]))
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
        self.assertTrue(self.singles_section.has_all_stakes(), msg='All stakes block is not found')
        self.assertEqual(self.singles_section.all_stakes_label, 'All Single Stakes', msg='Section has wrong name')

    def test_003_enter_stake_into_all_stakes_field(self):
        """
        DESCRIPTION: Enter stake into 'All single stakes' field
        EXPECTED: Entered value is shown in 'All single stakes' field
        EXPECTED: All singles stake boxes are auto-populated with value from 'All single stakes' field
        EXPECTED: Multiples/Forecast/Tricast stake boxes are not affected if available
        """
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
        self.singles_section.all_stakes_section.amount_form.input.value = self.bet_amount

        for stake_name, stake in self.singles_section.items():
            self._logger.debug(f'*** Verifying stake "{stake.outcome_name}"')
            self.assertEqual(float(stake.amount_form.input.value), self.bet_amount,
                             msg=f'The stake amount should be "{stake.amount_form.input.value}" '
                                 f'but it is "{self.bet_amount}"')

        for stake_name, stake in self.multiples_section.items():
            self._logger.debug(f'*** Verifying stake "{stake_name}"')
            self.assertEqual(stake.amount_form.default_value, self.default_amount_value,
                             msg=f'The multiple stake amount is "{stake.amount_form.default_value}" '
                                 f'but should be "{self.default_amount_value}"')

    def test_004_go_to_separate_single_stake_box_edit_stake_value(self):
        """
        DESCRIPTION: Go to separate single stake box -> Edit stake value
        EXPECTED: Stake value is changed for selected single selection
        EXPECTED: 'All single stakes' field is not changed
        EXPECTED: Stakes for other bets in the betslip are not changed
        """
        stake_name = list(self.singles_section.keys())[0]
        self.__class__.new_amount = 0.02
        try:
            self.singles_section[stake_name].amount_form.input.value = self.new_amount
            amount = self.singles_section[stake_name].amount_form.input.value
            all_stakes_amount = self.singles_section.all_stakes_section.amount_form.input.value
        except StaleElementReferenceException:
            sections = self.get_betslip_sections(multiples=True)
            self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
            self.singles_section[stake_name].amount_form.input.value = self.new_mount
            amount = self.singles_section[stake_name].amount_form.input.value
            all_stakes_amount = self.singles_section.all_stakes_section.amount_form.input.value
        self.assertEqual(self.new_amount, float(amount),
                         msg=f'The value of "{self.new_amount}" is not present in the "Stake" field, '
                             f'the value is "{float(amount)}"')
        self.assertEqual(float(all_stakes_amount), self.bet_amount,
                         msg=f'All stakes amount value "{float(all_stakes_amount)}" '
                             f'is not equal to bet amount "{self.bet_amount}"')

    def test_005_enter_new_stake_value_into_all_stakes_field(self):
        """
        DESCRIPTION: Enter new stake value into 'All single stakes' field
        EXPECTED: Entered value is shown in 'All single stakes' field
        EXPECTED: All singles stake boxes are auto-populated with new value from 'All single stakes' field
        EXPECTED: Every manipulation with 'All single stakes' field overrides all singles stake boxes with selected value
        """
        entered_amount = self.bet_amount + self.new_amount
        self.singles_section.all_stakes_section.amount_form.input.value = entered_amount

        for stake_name, stake in self.singles_section.items():
            self._logger.info(f'*** Stakes single: "{stake.outcome_name}"')
            stake_amount = stake.amount_form.input.value
            self.assertEqual(stake_amount, f'{entered_amount:.2f}',
                             msg=f'The stake amount should be "{stake_amount}" '
                                 f'but it is "{entered_amount:.2f}"')

    def test_006_delete_stake_value_from_all_stakes_field(self):
        """
        DESCRIPTION: Delete stake value from 'All single stakes' field
        EXPECTED: Stake value is removed from 'All single stakes' field
        EXPECTED: All singles stake boxes are cleared respectively
        EXPECTED: Multiples/Forecast/Tricast stake boxes are not affected if available
        """
        self.singles_section.all_stakes_section.amount_form.input.clear()
        sections = self.get_betslip_sections(multiples=True)
        singles_section = sections.Singles

        for stake_name, stake in singles_section.items():
            self._logger.info(f'*** Verifying stake "{stake.outcome_name}"')
            default_stake_amount = stake.amount_form.default_value
            self.assertEqual(default_stake_amount, self.default_amount_value,
                             msg=f'The stake amount should be "{self.default_amount_value}" '
                                 f'but it is "{default_stake_amount}"')

    def test_007_enter_stake_value_into_all_stakes_field_when_at_least_one_single_is_suspended(self):
        """
        DESCRIPTION: Enter stake value into 'All single stakes' field when at least one single is suspended
        EXPECTED: Entered value is shown in 'All single stakes' field
        EXPECTED: All active singles stake boxes are auto-populated with new value from 'All single stakes' field
        EXPECTED: All suspended singles stake boxes are not affected by the change
        EXPECTED: Multiples/Forecast/Tricast stake boxes are not affected if available
        """
        singles_section = self.get_betslip_sections().Singles
        stake_to_suspend = singles_section[self.first_selection]
        self.__class__.suspend_amount = 5.00
        # spike to format input value correctly
        stake_to_suspend.amount_form.input.value = f'{self.suspend_amount:.2f}'
        stake_amount = stake_to_suspend.amount_form.input.value
        stake_to_suspend.amount_form.input.click()
        self.singles_section.all_stakes_section.click()
        self.assertEqual(float(stake_amount), self.suspend_amount,
                         msg=f'Stake "{self.first_selection}" amount "{stake_amount}" '
                             f'is not the same as entered "{self.suspend_amount}"')
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.first_selection], displayed=True, active=False)
        result = stake_to_suspend.is_suspended(timeout=60)
        self.assertTrue(result, msg='Event is not suspended')
        self.__class__.all_stakes_amount = 0.05
        self.singles_section.all_stakes_section.amount_form.input.value = self.all_stakes_amount
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        for stake_name, stake in singles_section.items():
            self._logger.info(f'*** Verifying stake "{stake.outcome_name}"')
            if stake_name == self.first_selection:
                stake_amount = stake.amount_form.input.value
                self.assertEqual(float(stake_amount), self.suspend_amount,
                                 msg=f'Amount in suspended stake "{stake_name}" "{float(stake_amount)}'
                                     f'is not the same as expected "{self.suspend_amount}"')
            else:
                stake_amount = stake.amount_form.input.value
                self.assertEqual(float(stake_amount), self.all_stakes_amount,
                                 msg=f'The stake amount should be "{self.all_stakes_amount}" '
                                     f'but it is "{float(stake_amount)}"')

        for stake_name, stake in multiples_section.items():
            default_stake_amount = stake.amount_form.default_value
            self.assertEqual(default_stake_amount, self.default_amount_value,
                             msg=f'Amount in Multiples stake "{stake_name}" "{default_stake_amount}"'
                                 f'is not the same as expected "{self.default_amount_value}"')

    def test_008_unsuspend_previously_suspended_selection(self):
        """
        DESCRIPTION: Unsuspend previously suspended selection
        EXPECTED: Selection is unsuspended
        EXPECTED: Selection's stake box contains the same value as before suspension
        """
        singles_section = self.get_betslip_sections().Singles
        stake_to_unsuspend = singles_section[self.first_selection]
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.first_selection], displayed=True, active=True)
        result = stake_to_unsuspend.is_suspended(timeout=60, expected_result=False)
        self.assertFalse(result, msg='Event is still suspended')

        for stake_name, stake in singles_section.items():
            self._logger.info(f'*** Verifying stake "{stake.outcome_name}"')
            if stake_name == self.first_selection:
                stake_amount = stake.amount_form.input.value
                self.assertEqual(float(stake_amount), self.suspend_amount,
                                 msg=f'Amount in unsuspended stake "{stake_name}" "{float(stake_amount)}"'
                                     f'is not the same as expected "{self.suspend_amount}"')
            else:
                stake_amount = stake.amount_form.input.value
                self.assertEqual(float(stake_amount), self.all_stakes_amount,
                                 msg=f'The stake amount is "{float(stake_amount)}" '
                                     f'but expected "{self.all_stakes_amount}"')
