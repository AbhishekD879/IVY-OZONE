import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl  # can't change event state for prod/hl env
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.high
@pytest.mark.desktop
@vtest
class Test_C2514476_Betslip_Reflection_on_Sport_Outcome_Suspended_Unsuspended_for_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C2514476
    NAME: Betslip Reflection on <Sport> Outcome Suspended/Unsuspended for Single Bet
    DESCRIPTION: Test case verifies Betslip reflection for Single bet when its outcome is Suspended and Unsuspended.
    PRECONDITIONS: Access to OB TI is required
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events.
        EXPECTED: User should be able to use previously generated events.
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.team1 = event.team1
        self.__class__.selection_id = event.selection_ids[self.team1]

    def test_001_add_single_sport_bet_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add single <Sport> bet to the Betslip and open Betslip
        EXPECTED: Betslip opened, selection is displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter stake
        EXPECTED: Entered stake amount is present on Betslip
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section[self.team1] if self.team1 in singles_section else None
        self.assertTrue(self.stake, msg=f'Stake of "{self.team1}" was not found')

        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(),
                        msg='Bet Now (Log In & Bet) button is disabled')

    def test_003_suspend_outcome(self):
        """
        DESCRIPTION: Trigger suspension of the outcome:
        DESCRIPTION: **outcomeStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=False)

        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_004_unsuspend_same_outcome(self):
        """
        DESCRIPTION: Make the market active again:
        DESCRIPTION: **outcomeStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * Selection become enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button enabled
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=True)
