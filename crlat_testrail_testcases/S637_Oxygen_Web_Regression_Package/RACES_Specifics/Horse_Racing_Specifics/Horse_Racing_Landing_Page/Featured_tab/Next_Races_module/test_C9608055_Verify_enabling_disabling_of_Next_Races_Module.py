import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C9608055_Verify_enabling_disabling_of_Next_Races_Module(Common):
    """
    TR_ID: C9608055
    NAME: Verify enabling/disabling of 'Next Races' Module
    DESCRIPTION: This test case verifies enabling/disabling of "Next Races" Module on Horse Racing EDP via CMS
    PRECONDITIONS: 1. "Next Races" Module for Horse Racing EDP should be disabled(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesComponentEnabled=false)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Navigate to the Horse Racing EDP
    """
    keep_browser_open = True

    def test_001_check_availability_of_next_races_module_on_horse_racing_featured_tab(self):
        """
        DESCRIPTION: Check availability of "Next Races" Module on Horse Racing Featured tab
        EXPECTED: * "Next Races" Module is not displayed on Horse Racing Featured tab
        """
        pass

    def test_002_in_cms___system_configuration___structure___nextracestoggle_and_check_the_checkbox_for_nextracescomponentenabled(self):
        """
        DESCRIPTION: In CMS -> system-configuration -> structure -> NextRacesToggle and check the checkbox for nextRacesComponentEnabled.
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_oxygen_app_page_and_verify_the_availability_of_next_races_module_on_horse_racing_featured_tab(self):
        """
        DESCRIPTION: Refresh the Oxygen app page and verify the availability of "Next Races" Module on Horse Racing Featured tab.
        EXPECTED: * "Next Races" Module is displayed on Horse Racing Featured tab
        """
        pass
