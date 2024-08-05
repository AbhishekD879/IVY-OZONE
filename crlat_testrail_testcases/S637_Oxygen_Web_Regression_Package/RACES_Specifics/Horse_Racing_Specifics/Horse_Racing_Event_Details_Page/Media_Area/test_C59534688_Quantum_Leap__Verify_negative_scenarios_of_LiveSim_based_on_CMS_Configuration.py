import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C59534688_Quantum_Leap__Verify_negative_scenarios_of_LiveSim_based_on_CMS_Configuration(Common):
    """
    TR_ID: C59534688
    NAME: [Quantum Leap] - Verify negative scenarios of LiveSim  based on CMS Configuration
    DESCRIPTION: This test case verifies the behavior of LiveSim: in case the configs are missing or configured with mistakes - then the previous logic remains
    PRECONDITIONS: - Log in to CMS and navigate to 'System-configuration' -> 'Config' (Coral and Ladbrokes)
    PRECONDITIONS: - Create or make sure the 'QuantumLeapTimeRange' Configs are available:
    PRECONDITIONS: *Field Name: 'startTime' and 'endTime'
    PRECONDITIONS: *Field time: 'input' and 'input'
    PRECONDITIONS: *Possible Value: 'Any text', 'Any text'
    PRECONDITIONS: *Default Value: '03:00am', '11:59pm'
    PRECONDITIONS: *Action - -
    PRECONDITIONS: *Config boxes above the table: 'Edit Table', 'Add Property', 'Remove group', Initial Data Checkbox is checked
    PRECONDITIONS: ![](index.php?/attachments/get/117706480)
    PRECONDITIONS: - Navigate to 'System-configuration' -> 'Structure' tab
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: Keep in mind that *the PRE-PARADE button is shown based on local time*. Therefore, despite the start time of events - the time is received from CMS settings and shown based on the user's local time on the device.
    PRECONDITIONS: Please not that Live Sim/Quantum Leap is available for UK or IRE Horseracing and Greyhounds (The following parameters are received: eventEntity.isUKorIRE; sportName !== 'greyhound')
    """
    keep_browser_open = True

    def test_001__in_structure_tab_find_quantumleaptimerange_in_the_search_field_select_an_invalid_time_range_for_example_2500pm_or_when_starttime_is_later_than_endtime_save_the_changesindexphpattachmentsget118215010(self):
        """
        DESCRIPTION: * In 'Structure' tab find 'QuantumLeapTimeRange' in the search field
        DESCRIPTION: * Select an invalid time range (for example, 25:00pm or when startTime is later than endTime)
        DESCRIPTION: * Save the changes
        DESCRIPTION: ![](index.php?/attachments/get/118215010)
        EXPECTED: The changes are saved
        """
        pass

    def test_002_open_devtools_on_the_homepage_and_verify_the_initial_data_response_in_network(self):
        """
        DESCRIPTION: Open Devtools on the homepage and verify the Initial Data response in 'Network'
        EXPECTED: The Invalid Time Range of 'QuantumLeapTimeRange' is received in the Initial Data response
        """
        pass

    def test_003_navigate_to_any_upcoming_horse_racing_event(self):
        """
        DESCRIPTION: Navigate to any upcoming Horse Racing event
        EXPECTED: The event is open and the button 'PRE-PARADE' is available
        EXPECTED: ![](index.php?/attachments/get/118618380)
        """
        pass

    def test_004__navigate_to_the_structure_tab_and_find_quantumleaptimerange_in_the_search_field_delete_the_starttime_or_endtime_save_the_changesindexphpattachmentsget118215010_repeat_steps_2_3(self):
        """
        DESCRIPTION: * Navigate to the 'Structure' tab and find 'QuantumLeapTimeRange' in the search field
        DESCRIPTION: * Delete the startTime' or 'endTime'
        DESCRIPTION: * Save the changes
        DESCRIPTION: ![](index.php?/attachments/get/118215010)
        DESCRIPTION: * Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_005__navigate_to_the_config_tab_and_find_quantumleaptimerange_in_the_search_fieldindexphpattachmentsget118215298_delete_all_quantumleaptimerange_configs_save_changes_repeat_steps_2_3(self):
        """
        DESCRIPTION: * Navigate to the 'Config' tab and find 'QuantumLeapTimeRange' in the search field
        DESCRIPTION: ![](index.php?/attachments/get/118215298)
        DESCRIPTION: * Delete all 'QuantumLeapTimeRange' configs
        DESCRIPTION: * Save changes
        DESCRIPTION: * Repeat steps #2-3
        EXPECTED: 
        """
        pass
