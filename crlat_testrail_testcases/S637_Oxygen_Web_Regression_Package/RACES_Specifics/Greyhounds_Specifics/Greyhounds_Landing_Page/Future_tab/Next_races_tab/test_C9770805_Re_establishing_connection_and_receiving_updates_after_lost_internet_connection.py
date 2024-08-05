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
class Test_C9770805_Re_establishing_connection_and_receiving_updates_after_lost_internet_connection(Common):
    """
    TR_ID: C9770805
    NAME: Re-establishing connection and receiving updates after lost internet connection
    DESCRIPTION: This test case verifies re-establishing connection to Greyhounds and receiving updates when connection is lost in order to receive the latest Greyhounds Next races Events data.
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds "Next races" Tab
    """
    keep_browser_open = True

    def test_001_make_device_lose_internet_connection_for_as_much_time_so_connection_to_greyhounds_is_completely_lost(self):
        """
        DESCRIPTION: Make device lose internet connection for as much time, so connection to Greyhounds is completely lost
        EXPECTED: 
        """
        pass

    def test_002_restore_internet_connectionverify_next_races_tab(self):
        """
        DESCRIPTION: Restore internet connection
        DESCRIPTION: Verify Next races tab
        EXPECTED: Next races tab content is displayed.
        """
        pass
