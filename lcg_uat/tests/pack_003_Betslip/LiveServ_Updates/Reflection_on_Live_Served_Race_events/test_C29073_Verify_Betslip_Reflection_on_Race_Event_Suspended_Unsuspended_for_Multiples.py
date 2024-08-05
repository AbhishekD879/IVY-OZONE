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
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C29073_Verify_Betslip_Reflection_on_Race_Event_Suspended_Unsuspended_for_Multiples(BaseBetSlipTest):
    """
    TR_ID: C29073
    NAME: Verify Betslip Reflection on <Race> Event Suspended/Unsuspended for Multiples
    """
    keep_browser_open = True
    bet_amount = 0.10

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create few Horse Racing events
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        self.__class__.selection_name_1, self.__class__.selection_id_1 = list(event_params.selection_ids.items())[0]
        self.__class__.marketID_1 = event_params.market_id
        self.__class__.eventID_1 = event_params.event_id

        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        self.__class__.selection_name_2, self.__class__.selection_id_2 = list(event_params.selection_ids.items())[0]
        self.__class__.marketID_2 = event_params.market_id
        self.__class__.eventID_2 = event_params.event_id

    def test_001_make_single_race_selection(self):
        """
        DESCRIPTION: Make single Race selection
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_1)

    def test_002_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Added selection is displayed in the betslip
        """
        single_section = self.get_betslip_sections().Singles
        self.assertTrue(single_section, msg='"SINGLE" Betslip section was not found')

        self.__class__.stake = single_section.get(self.selection_name_1)
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name_1}" section not found')

    def test_003_suspend_the_event(self):
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
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=False)

        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_004_from_ox_99_for_ladbrokes_wait_5_sec_verify_that_message_on_the_top_ob_betslip_is_removed(self):
        """
        DESCRIPTION: **From OX 99 for Ladbrokes:**
        DESCRIPTION: Wait 5 sec
        DESCRIPTION: Verify that message on the top ob Betslip[ is removed
        EXPECTED: Message 'Some of your selections have been suspended' is removed from the top of the Betslip
        """
        # will be verified in step 3 for Ladbrokes

    def test_005_trigger_the_following_situation_for_this_eventeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
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
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=False)

    def test_006_from_ox99tap_x_button(self):
        """
        DESCRIPTION: **From OX99**
        DESCRIPTION: Tap 'X' button
        EXPECTED: Bet is removed from Betslip successfully
        """
        self.clear_betslip()

    def test_007_add_a_few_selections_from_different_events(self):
        """
        DESCRIPTION: Add a few selections from different events
        EXPECTED: 'Singles' and 'Multiples' sections are shown in the bet slip
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id_1, self.selection_id_2])

        betslip_sections = self.get_betslip_sections(multiples=True)
        single_section = betslip_sections.Singles
        self.assertTrue(single_section, msg='"SINGLE" Betslip section was not found')

        self.__class__.stake = single_section.get(self.selection_name_1)
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name_1}" section not found')
        self.__class__.stake_2 = single_section.get(self.selection_name_2)
        self.assertTrue(self.stake_2, msg=f'Stake: "{self.selection_name_2}" section not found')

        multiple_section = betslip_sections.Multiples
        self.assertTrue(multiple_section, msg='"MULTIPLES" Betslip section was not found')
        self.__class__.double_stake = multiple_section.get(vec.betslip.DBL)
        self.assertTrue(self.double_stake, msg=f'"{vec.betslip.DBL}" stake is not found')

    def test_008_trigger_the_following_situation_for_one_of_events_eventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for one of events:
        DESCRIPTION: **eventStatusCode="S"**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.test_003_suspend_the_event()

    def test_009_enter_stake_into_multiple(self):
        """
        DESCRIPTION: Enter Stake into Multiple
        EXPECTED: Coral:
        EXPECTED: Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        """
        self.enter_stake_amount(stake=(self.double_stake.name, self.double_stake))

        self.verify_betslip_is_suspended(stakes=[self.stake], verify_overlay_message=False)

    def test_010_trigger_the_following_situation_for_suspended_event_eventstatuscodea(self):
        """
        DESCRIPTION: Trigger the following situation for suspended event:
        DESCRIPTION: **eventStatusCode="A"**
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: *  All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=True)
