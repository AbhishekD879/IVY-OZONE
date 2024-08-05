import pytest

from tests.base_test import vtest
import voltron.environments.constants as vec
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
class Test_C29062_Betslip_Reflection_on_Sport_Event_Suspended_Unsuspended_for_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C29062
    NAME: Betslip Reflection on <Sport> Event Suspended/Unsuspended for Single Bet
    DESCRIPTION: This test case verifies Betslip reflection when <Sport> Event is Suspended/Unsuspended for Single Bet.
    """
    keep_browser_open = True

    def test_000_create_test_events(self):
        """
        DESCRIPTION: Create test event.
        EXPECTED: User should be able to use previously generated event.
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids

    def test_001_add_sport_bet_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add single <Sport> bet to the Betslip
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[vec.sb.DRAW.title()])
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(vec.sb.DRAW.title(), singles_section.items()[0],
                      msg=f'"{vec.sb.DRAW}" title is not displayed within "{vec.betslip.BETSLIP_SINGLES_NAME}" section')
        self.__class__.stake = singles_section[vec.sb.DRAW.title()]
        self.assertTrue(self.stake, msg=f'"{vec.sb.DRAW}" stake is not displayed')

    def test_002_suspend_event(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode="S"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.stake.amount_form.input.value = self.bet_amount
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_003_for_ladbrokes_wait_5_sec_verify_that_message_on_the_top_ob_betslip_is_removed(self):
        """
        DESCRIPTION: **From OX 99 for Ladbrokes:**
        DESCRIPTION: Wait 5 sec
        DESCRIPTION: Verify that message on the top ob Betslip is removed
        EXPECTED: Message  'Some of your selections have been suspended' is removed from the top of the Betslip
        """
        # verified on step 2

    def test_004_make_event_active_again(self):
        """
        DESCRIPTION: Make the event active again: eventStatusCode="A"
        DESCRIPTION: and at the same time have Betslip page opened to watch for update
        EXPECTED: * Selection becomes enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=True)
