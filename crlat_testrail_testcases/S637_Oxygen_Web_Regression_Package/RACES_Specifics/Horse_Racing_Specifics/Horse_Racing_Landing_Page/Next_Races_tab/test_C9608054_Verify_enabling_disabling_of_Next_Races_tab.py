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
class Test_C9608054_Verify_enabling_disabling_of_Next_Races_tab(Common):
    """
    TR_ID: C9608054
    NAME: Verify enabling/disabling of "Next Races" tab
    DESCRIPTION: This test case verifies enabling/disabling of "Next Races" tab on Horse Racing EDP via CMS
    DESCRIPTION: Note: cannot automate as we cannot disable anything in CMS as it might affect other tests and QAs
    PRECONDITIONS: 1. "Next Races" tab on Horse Racing EDP should be disabled(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=false)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Navigate to the Horse Racing EDP
    """
    keep_browser_open = True

    def test_001_check_availability_of_next_races_tab_on_horse_racing_edp(self):
        """
        DESCRIPTION: Check availability of "Next Races" tab on Horse Racing EDP
        EXPECTED: * "Next Races" tab is not displayed on Horse Racing EDP
        """
        pass

    def test_002_in_cms___system_configuration___structure___nextracestoggle_and_check_the_checkbox_for_nextracestabenabled(self):
        """
        DESCRIPTION: In CMS -> system-configuration -> structure -> NextRacesToggle and check the checkbox for nextRacesTabEnabled.
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_oxygen_app_page_and_verify_the_availability_of_next_races_tab_on_horse_racing_edp(self):
        """
        DESCRIPTION: Refresh the Oxygen app page and verify the availability of "Next Races" tab on Horse Racing EDP.
        EXPECTED: * "Next Races" tab is displayed on Horse Racing EDP
        """
        pass
