import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger LiveServ updates on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.critical
@pytest.mark.liveserv_updates
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C29073_Verify_Betslip_Reflection_on_Race_Event_Suspended_Unsuspended_for_Singles(BaseBetSlipTest):
    """
    TR_ID: C29073
    NAME: Verify Betslip Reflection on <Race> Event Suspended/Unsuspended for Singles
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Greyhound Racing event
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        self.__class__.eventID = event_params.event_id

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login()

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

        single_section = self.get_betslip_sections().Singles
        self.__class__.stake = single_section.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name}" section not found')

    def test_003_trigger_event_suspension(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_004_trigger_event_unsuspension(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: *  All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=False)

    def test_005_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Tap 'Bin' icon to remove Bet from Betslip
        EXPECTED: Bet is removed from Betslip successfully
        """
        self.clear_betslip()
        if self.device_type == 'mobile':
            self.verify_betslip_counter_change(expected_value=0)
        else:
            self.assertEqual(self.get_betslip_content().no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'BetSlip content: "{self.get_betslip_content().no_selections_title}" '
                             f'is not equal to "{vec.betslip.NO_SELECTIONS_TITLE}"')
