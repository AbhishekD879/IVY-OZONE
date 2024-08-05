import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59530290_Quantum_Leap__Display_product_based_on_CMS_Configuration(Common):
    """
    TR_ID: C59530290
    NAME: [Quantum Leap] - Display product based on CMS Configuration
    DESCRIPTION: This test case verifies that:
    DESCRIPTION: -The Quantum Leap product(PRE-PARADE) is displayed only when it's available
    DESCRIPTION: -The Quantum Leap product(PRE-PARADE) is hidden when it's unavailable
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
    PRECONDITIONS: Keep in mind that *the PRE-PARADE Button is shown based on local time*. Therefore, despite the start time of events - the time is received from CMS settings and shown based on the user's local time on the device.
    PRECONDITIONS: Please note that Live Sim/Quantum Leap is available for UK or IRE Horseracing and Greyhounds (The following parameters are received: eventEntity.isUKorIRE; sportName !== 'greyhound')
    """
    keep_browser_open = True

    def test_001_in_structure_tab_find_quantumleaptimerange_in_the_search_field(self):
        """
        DESCRIPTION: In 'Structure' tab find 'QuantumLeapTimeRange' in the search field
        EXPECTED: 'QuantumLeapTimeRange' Configs are displayed:
        EXPECTED: -Field Name ('startTime' and 'endTime')
        EXPECTED: -Field Value (is editable, for example, 11:45am, 23:00pm)
        EXPECTED: -Initial Data Checkbox is checked
        EXPECTED: ![](index.php?/attachments/get/117706499)
        """
        pass

    def test_002_open_devtools_on_the_homepage_and_verify_the_initial_data_response_in_network(self):
        """
        DESCRIPTION: Open Devtools on the homepage and verify the Initial Data response in 'Network'
        EXPECTED: 'QuantumLeapTimeRange' is received in the Initial Data response
        EXPECTED: ![](index.php?/attachments/get/117706674)
        """
        pass

    def test_003_navigate_to_any_horse_racing_event_with_live_sim_available_and_within_the_given_time_range(self):
        """
        DESCRIPTION: Navigate to any Horse Racing event with Live Sim available and within the given time range
        EXPECTED: PRE-PARADE Button is available and clickable
        EXPECTED: ![](index.php?/attachments/get/118618379)
        """
        pass

    def test_004_navigate_to_any_horse_racing_event_out_of_the_given_time_range(self):
        """
        DESCRIPTION: Navigate to any Horse Racing event out of the given time range
        EXPECTED: PRE-PARADE Button is not displayed
        EXPECTED: ![](index.php?/attachments/get/118215462)
        """
        pass
