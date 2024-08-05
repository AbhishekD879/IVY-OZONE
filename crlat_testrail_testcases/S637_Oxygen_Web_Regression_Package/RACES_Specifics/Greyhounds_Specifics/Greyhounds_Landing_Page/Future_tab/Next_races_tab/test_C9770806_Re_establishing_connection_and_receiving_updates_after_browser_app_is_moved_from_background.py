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
class Test_C9770806_Re_establishing_connection_and_receiving_updates_after_browser_app_is_moved_from_background(Common):
    """
    TR_ID: C9770806
    NAME: Re-establishing connection and receiving updates after browser/app is moved from background
    DESCRIPTION: This test case verifies re-establishing connection to Greyhounds and receiving updates when user brings a browser/app from the background in order to receive the latest Greyhounds Next races Events data.
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds "Next races" Tab
    """
    keep_browser_open = True

    def test_001_move_app_to_background_for_as_much_time_so_connection_to_greyhounds_is_completely_lost(self):
        """
        DESCRIPTION: Move app to background for as much time, so connection to Greyhounds is completely lost
        EXPECTED: 
        """
        pass

    def test_002_move_app_to_foregroundverify_next_races_tab(self):
        """
        DESCRIPTION: Move app to foreground
        DESCRIPTION: Verify Next races tab
        EXPECTED: Next races tab content is displayed.
        """
        pass
