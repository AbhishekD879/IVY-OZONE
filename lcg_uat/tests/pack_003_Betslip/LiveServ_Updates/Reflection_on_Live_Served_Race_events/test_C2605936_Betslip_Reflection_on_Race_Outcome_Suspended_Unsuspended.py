import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.crl_prod  # we can't suspend outcome on HL/Prod
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C2605936_Betslip_Reflection_on_Race_Outcome_Suspended_Unsuspended(BaseBetSlipTest):
    """
    TR_ID: C2605936
    NAME: Betslip Reflection on <Race> Outcome Suspended/Unsuspended
    DESCRIPTION: This test case verifies Betslip reflection for Single <Race> bet when it is Suspended and Unsuspended.
    PRECONDITIONS: Access to OB TI is required
    """
    keep_browser_open = True
    horse_name = None
    selection_id = None
    betnow_section = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events.
        EXPECTED: User should be able to use previously generated events.
        """
        race_event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.horse_name = list(race_event.selection_ids.keys())[0]
        self.__class__.selection_id = race_event.selection_ids[self.horse_name]

    def test_001_add_single_race_bet_to_the_betslip(self):
        """
        DESCRIPTION: Add single <Race> bet to the Betslip
        """
        self.open_betslip_with_selections(self.selection_id)

    def test_002_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get(self.horse_name)
        self.assertTrue(self.stake, msg=f'"{self.horse_name}" stake is not available')

    def test_003_enter_stake(self):
        """
        DESCRIPTION: Enter stake
        """
        self.enter_stake_amount(stake=(self.stake.name, self.stake))

    def test_004_suspend_outcome(self):
        """
        DESCRIPTION: Trigger suspension of the outcome:
        DESCRIPTION: **outcomeStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=False)

        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_005_unsuspend_same_outcome(self):
        """
        DESCRIPTION: Make the market active again:
        DESCRIPTION: **outcomeStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=True)
