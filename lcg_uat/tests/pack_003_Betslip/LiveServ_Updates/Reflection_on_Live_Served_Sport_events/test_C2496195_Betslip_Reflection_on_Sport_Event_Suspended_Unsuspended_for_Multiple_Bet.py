import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.high
@pytest.mark.ob_smoke
@pytest.mark.desktop
@vtest
class Test_C2496195_Betslip_Reflection_on_Sport_Event_Suspended_Unsuspended_for_Multiple_Bet(BaseBetSlipTest):
    """
    TR_ID: C2496195
    NAME: Betslip Reflection on <Sport> Event Suspended/Unsuspended for Multiple Bet
    DESCRIPTION: This test case verifies Betslip reflection for Multiples section when Event is Suspended/Unsuspended
    """
    keep_browser_open = True
    event = event2 = None
    singles_section = multiples_section = None

    def test_000_create_test_events(self):
        """
        DESCRIPTION: Create test events.
        EXPECTED: User should be able to use previously generated events.
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID_1 = self.event.event_id
        self.__class__.team1 = self.event.team1

        self.__class__.event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID_2 = self.event2.event_id
        self.__class__.team2 = self.event2.team2

        self.__class__.event3 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.team3 = self.event3.team2

    def test_001_add_a_few_selections_from_different_active_events_and_open_betslip(self):
        """
        DESCRIPTION: Add a few selections from different active events
        EXPECTED: 'Multiples' section is shown on the Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.event.selection_ids[self.team1],
                                                         self.event2.selection_ids[self.team2],
                                                         self.event3.selection_ids[self.team3]))
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
        self.assertTrue(self.multiples_section.get(vec.betslip.DBL),
                        msg=f'"{vec.betslip.DBL}" stake is not found in "{self.multiples_section.keys()}"')

    def test_002_suspend_one_of_the_events(self):
        """
        DESCRIPTION: Suspend one of the events:
        DESCRIPTION: **eventStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages/labels are displayed for active selections
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=False)

        self.assertTrue(all(selection in self.singles_section for selection in (self.team1, self.team2)),
                        msg=f'Selections "{self.team1}" and "{self.team2}" are not present '
                        f'within "{vec.betslip.BETSLIP_SINGLES_NAME}" betslip section')

        suspended_event_stake, active_event_stake = self.singles_section[self.team1], self.singles_section[self.team2]

        self.verify_betslip_is_suspended(stakes=[suspended_event_stake], verify_overlay_message=False)

        self.assertFalse(active_event_stake.is_suspended(expected_result=False, timeout=1), msg=f'Stake is suspended')

    def test_003_unsuspend_the_same_event(self, is_enabled=False):
        """
        DESCRIPTION: Unsuspend the same event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=True)

        unsuspended_event_stake = self.singles_section[self.team1]

        self.verify_betslip_is_active(stakes=[unsuspended_event_stake], is_stake_filled=is_enabled)

    def test_004_enter_stake_for_the_multiple_bet(self):
        """
        DESCRIPTION: Enter Stake for the Multiple bet
        EXPECTED: Stake input field contains bet amount
        """
        stake = self.multiples_section.get(vec.betslip.TBL)
        self.enter_stake_amount(stake=(stake.name, stake))
        stake.click()

    def test_005_suspend_two_of_the_events(self):
        """
        DESCRIPTION: Suspend two of the events:
        DESCRIPTION: **eventStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages are displayed for active selections
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Some of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'Some of your selections have been suspended' with duration: 5s
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=False)
        self.ob_config.change_event_state(event_id=self.eventID_2, displayed=True, active=False)

        suspended_event_stake_1, suspended_event_stake_2, active_event_stake = (self.singles_section[self.team1],
                                                                                self.singles_section[self.team2],
                                                                                self.singles_section[self.team3])

        self.verify_betslip_is_suspended(stakes=[suspended_event_stake_1, suspended_event_stake_2], verify_overlay_message=False)

        self.assertFalse(active_event_stake.is_suspended(expected_result=False, timeout=1), msg=f'Stake is suspended')

    def test_006_unsuspend_the_same_event(self):
        """
        DESCRIPTION: Unsuspend the same event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_event_state(event_id=self.eventID_2, displayed=True, active=True)

        unsuspended_event_stake = self.singles_section[self.team2]
        self.assertFalse(unsuspended_event_stake.is_suspended(expected_result=False, timeout=30),
                         msg=f'Stake is suspended')
        self.assertTrue(unsuspended_event_stake.amount_form.input.is_enabled(timeout=5),
                        msg='Stake amount field is not enabled')

        self.test_003_unsuspend_the_same_event(is_enabled=True)

        betnow_section = self.get_betslip_content()
        self.assertTrue(betnow_section.bet_now_button.is_enabled(), msg='"Log In and Bet" button is not enabled')
