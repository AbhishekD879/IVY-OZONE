import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl  # can't change event state for prod/hl env
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@vtest
class Test_C2514477_Betslip_Reflection_on_Sport_Outcome_Suspended_Unsuspended_for_Multiple_Bet(BaseBetSlipTest):
    """
    TR_ID: C2514477
    NAME: Betslip Reflection on <Sport> Outcome Suspended/Unsuspended for Multiple Bet
    DESCRIPTION: This test case verifies Betslip reflection for Multiples section when outcome is Suspended
    PRECONDITIONS: Access to OB TI is required
    """
    keep_browser_open = True

    def assert_double_stake_present(self):
        """
        Verify 'Multiples' section is shown on the Betslip and is not rebuilt
        """
        self.assertTrue(self.multiples_section.get('Double'),
                        msg=f'"Double" stake is not found in "{self.multiples_section.keys()}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        EXPECTED: Events are created
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.team1 = self.event.team1
        self.__class__.event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.team2 = self.event2.team2
        self.__class__.selection_id_1 = self.event.selection_ids[self.team1]
        self.__class__.selection_id_2 = self.event2.selection_ids[self.team2]

    def test_001_add_a_few_selections_from_different_active_events(self):
        """
        DESCRIPTION: Add a few selections from different active events
        EXPECTED: 'Multiples' section is shown on the Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.event.selection_ids[self.team1],
                                                         self.event2.selection_ids[self.team2]))
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
        self.assert_double_stake_present()

    def test_002_suspend_one_of_outcomes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend one of outcomes:
        DESCRIPTION: **outcomeStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages/labels are displayed for active selections
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        """
        suspended_outcome, active_outcome = self.singles_section[self.team1], self.singles_section[self.team2]

        self.ob_config.change_selection_state(self.selection_id_1, displayed=True, active=False)

        self.verify_betslip_is_suspended(stakes=[suspended_outcome])

        self.assert_double_stake_present()
        self.assertTrue(all(selection in self.singles_section for selection in (self.team1, self.team2)),
                        msg=f'Selections "{self.team1}" and "{self.team2}" are not present '
                        f'within "{vec.betslip.BETSLIP_SINGLES_NAME}" betslip section')

        self.assertFalse(active_outcome.is_suspended(expected_result=False, timeout=1),
                         msg=f'Stake "{active_outcome.name}" is not suspended')

    def test_003_unsuspend_the_same_outcomes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Unsuspend the same outcome:
        DESCRIPTION: **outcomeStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_selection_state(self.selection_id_1, displayed=True, active=True)

        unsuspend_outcome = self.singles_section[self.team1]

        self.verify_betslip_is_active(stakes=[unsuspend_outcome], is_stake_filled=False)

        self.assert_double_stake_present()

    def test_004_enter_stake_for_the_multiple_bet(self):
        """
        DESCRIPTION: Enter Stake for the Multiple bet
        EXPECTED: Stake input field contains bet amount
        """
        stake = self.multiples_section.get(vec.betslip.DBL)
        self.enter_stake_amount(stake=(stake.name, stake))

    def test_005_suspend_one_of_outcomes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend two of outcomes:
        DESCRIPTION: **outcomeStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages are displayed for active selections
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        """
        self.ob_config.change_selection_state(self.selection_id_1, displayed=True, active=False)
        self.ob_config.change_selection_state(self.selection_id_2, displayed=True, active=False)

        suspended_outcome_1, suspended_outcome_2 = self.singles_section[self.team1], self.singles_section[self.team2]

        self.verify_betslip_is_suspended(stakes=[suspended_outcome_1, suspended_outcome_2],
                                         verify_overlay_message=False)

        self.assert_double_stake_present()

    def test_006_unsuspend_the_same_outcome_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Unsuspend the same outcome:
        DESCRIPTION: **outcomeStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_selection_state(self.selection_id_1, displayed=True, active=True)
        self.ob_config.change_selection_state(self.selection_id_2, displayed=True, active=True)

        self.assert_double_stake_present()
        unsuspend_outcome_1 = self.singles_section[self.team1]
        unsuspend_outcome_2 = self.singles_section[self.team2]

        self.verify_betslip_is_active(stakes=[unsuspend_outcome_1, unsuspend_outcome_2], is_stake_filled=True)
