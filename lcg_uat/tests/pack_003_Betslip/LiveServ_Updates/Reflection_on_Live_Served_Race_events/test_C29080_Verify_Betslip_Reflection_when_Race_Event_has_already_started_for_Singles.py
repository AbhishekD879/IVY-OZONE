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
@vtest
class Test_C29080_Verify_Betslip_Reflection_when_Race_Event_has_already_started_for_Singles(BaseBetSlipTest):
    """
    TR_ID: C29080
    NAME: Verify Betslip Reflection when <Race> Event has already started for Singles
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Greyhound Racing event
        """
        start_time = self.get_date_time_formatted_string(seconds=10)
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time)
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        self.__class__.eventID = event_params.event_id

    def test_001_add_race_selection_of_event_which_is_not_yet_started_to_the_betslip(self):
        """
        DESCRIPTION: Add <Race> selection of event which is not yet started to the Betslip
        EXPECTED: Added selection is displayed in the betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        single_section = self.get_betslip_sections().Singles

        self.__class__.stake = single_section.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name}" section not found')

    def test_002_trigger_event_has_already_started(self):
        """
        DESCRIPTION: Trigger for this event the following situation:
        DESCRIPTION: **isStarted = true** ("isOff = Yes")
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Coral:
        EXPECTED: *Yellow message: 'Event has already started!" is shown above the selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * Message is displayed at the top of the betslip 'Event has already started!" with duration: 5s
        """
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=True)
        try:
            self.verify_betslip_is_suspended(stakes=[self.stake], is_started=True)
        except Exception:
            self.device.refresh_page()
            single_section = self.get_betslip_sections().Singles
            self.__class__.stake = single_section.get(self.selection_name)
            self.site.open_betslip()
            self.verify_betslip_is_suspended(stakes=[self.stake], is_started=True)

    def test_003_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: No selections are present in the Betslip
        """
        self.clear_betslip()

    def test_004_add_a_few_race_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add a few race selections from different events to the Betslip
        EXPECTED: Multiples section is shown on the Betslip
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        self.__class__.selection_name_1, self.__class__.selection_id_1 = list(event_params.selection_ids.items())[0]
        self.__class__.eventID = event_params.event_id

        start_time = self.get_date_time_formatted_string(seconds=10)
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time)
        self.__class__.selection_name_2, self.__class__.selection_id_2 = list(event_params.selection_ids.items())[0]

        self.open_betslip_with_selections(selection_ids=[self.selection_id_1, self.selection_id_2])

        sections = self.get_betslip_sections(multiples=True)

        single_section = sections.Singles
        self.__class__.stake = single_section.get(self.selection_name_1)
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name_1}" section not found')
        stake_2 = single_section.get(self.selection_name_2)
        self.assertTrue(stake_2, msg=f'Stake: "{self.selection_name_2}" section not found')

        multiple_section = sections.Multiples
        self.__class__.double_stake = multiple_section.get(vec.betslip.DBL)
        self.assertTrue(self.double_stake, msg=f'"{vec.betslip.DBL}" stake is not found')

    def test_005_trigger_event_has_already_started_for_one_of_the_events(self):
        """
        DESCRIPTION: Trigger **isStarted = true** ("isOff = Yes") for one of the events
        EXPECTED: Coral:
        EXPECTED: *Yellow message: 'Event has already started!" is shown above the selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * Message is displayed at the top of the betslip 'Event has already started!" with duration: 5s
        """
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=True)
        try:
            self.verify_betslip_is_suspended(stakes=[self.stake], is_started=True)
        except Exception:
            self.device.refresh_page()
            sections = self.get_betslip_sections(multiples=True)
            single_section, multiple_section = sections.Singles, sections.Multiples
            self.__class__.stake = single_section.get(self.selection_name_1)
            self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name_1}" section not found')
            self.__class__.double_stake = multiple_section.get(vec.betslip.DBL)
            self.assertTrue(self.double_stake, msg=f'"{vec.betslip.DBL}" stake is not found')
            self.verify_betslip_is_suspended(stakes=[self.stake], is_started=True)

    def test_006_enter_stake_into_multiple(self):
        """
        DESCRIPTION: Enter Stake into Multiple
        EXPECTED: Message is not changed:
        EXPECTED: Coral:
        EXPECTED: Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        """
        self.enter_stake_amount(stake=(self.double_stake.name, self.double_stake))

        expected_message = vec.betslip.SINGLE_DISABLED
        actual_message = self.get_betslip_content().error
        self.assertEqual(actual_message, expected_message,
                         msg=f'Error message "{actual_message}" != expected "{expected_message}"')
