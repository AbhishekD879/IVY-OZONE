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
class Test_C9770788_Re_establishing_connection_and_receiving_updates_after_sleep_mode(Common):
    """
    TR_ID: C9770788
    NAME: Re-establishing connection and receiving updates after sleep mode.
    DESCRIPTION: This test case verifies re-establishing connection to Greyhounds and receiving updates after sleep mode in order to receive the latest Greyhounds Next races Events data.
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS(CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds "Next races" Tab
    """
    keep_browser_open = True

    def test_001_lock_device_for_as_much_time_so_it_goes_to_sleep_mode_and_web_socket_connection_to_greyhounds_next_races_is_completely_lost(self):
        """
        DESCRIPTION: Lock device for as much time, so it goes to sleep mode and web-socket connection to Greyhounds Next races is completely lost
        EXPECTED: 
        """
        pass

    def test_002_unlock_deviceverify_next_races_tab(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify Next races tab
        EXPECTED: Next races tab content is displayed.
        """
        pass
