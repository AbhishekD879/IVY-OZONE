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
class Test_C9769891_Verify_enabling_disabling_of_Next_Races_tab(Common):
    """
    TR_ID: C9769891
    NAME: Verify enabling/disabling of "Next Races" tab
    DESCRIPTION: This test case verifies enabling/disabling of "Next Races" tab on Greyhounds via CMS
    DESCRIPTION: Note: cannot automate, we won't disable anything in CMS as it might affect other testers and tests
    PRECONDITIONS: 1. "Next Races" tab on Greyhounds should be disabled (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Navigate to the Greyhounds
    """
    keep_browser_open = True

    def test_001_check_availability_of_next_races_tab_on_greyhounds(self):
        """
        DESCRIPTION: Check availability of "Next Races" tab on Greyhounds
        EXPECTED: "Next Races" tab is not displayed on Greyhounds
        """
        pass

    def test_002_in_cms___system_configuration___structure___greyhoundnextracestoggle_and_check_the_checkbox_for_nextracestabenabled(self):
        """
        DESCRIPTION: In CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle and check the checkbox for nextRacesTabEnabled.
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_oxygen_app_page_and_verify_the_availability_of_the_next_races_tab_on_greyhounds(self):
        """
        DESCRIPTION: Refresh the Oxygen app page and verify the availability of the "Next Races" tab on Greyhounds.
        EXPECTED: "Next Races" tab is displayed on Greyhounds
        """
        pass
