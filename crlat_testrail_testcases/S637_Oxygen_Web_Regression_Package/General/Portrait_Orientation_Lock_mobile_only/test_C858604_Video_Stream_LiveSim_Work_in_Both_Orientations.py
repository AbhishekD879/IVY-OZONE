import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C858604_Video_Stream_LiveSim_Work_in_Both_Orientations(Common):
    """
    TR_ID: C858604
    NAME: Video/Stream/LiveSim Work in Both Orientations
    DESCRIPTION: This test case verifies that Video/Stream/LiveSim works in both orientations
    DESCRIPTION: ** JIRA tickets:**
    DESCRIPTION: BMA-18045 Prevent mobile devices from rotating to landscape
    PRECONDITIONS: Screen rotate option is enabled on a mobile device
    """
    keep_browser_open = True

    def test_001_load_app_device_in_portrait_orientation(self):
        """
        DESCRIPTION: Load app (device in portrait orientation)
        EXPECTED: Home Page is loaded in portrait orientation
        """
        pass

    def test_002_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_003_navigate_to_page_that_contains__video__stream__live_sim_quantum_leap(self):
        """
        DESCRIPTION: Navigate to page that contains:
        DESCRIPTION: - Video
        DESCRIPTION: - Stream
        DESCRIPTION: - Live Sim (Quantum Leap)
        EXPECTED: Page is loaded in portrait orientation and contains video player
        """
        pass

    def test_004_tap_on_play_button_in_video_player__open_video_in_full_screen(self):
        """
        DESCRIPTION: Tap on Play button in video player > Open video in full screen
        EXPECTED: Video starts to play in small window in portrait orientation with black background
        """
        pass

    def test_005_rotate_device_to_landscape(self):
        """
        DESCRIPTION: Rotate device to Landscape
        EXPECTED: Video Proceed playing in landscape orientation on full screen
        """
        pass

    def test_006_close_full_screen_video__remain_in_landscape(self):
        """
        DESCRIPTION: Close full screen video > Remain in landscape
        EXPECTED: Page is displayed with animated mobile icon and text: "Please rotate your screen back in Portrait Mode. Please ensure you have 'screen rotate' option active."
        """
        pass

    def test_007_rotate_device_to_portrait(self):
        """
        DESCRIPTION: Rotate device to Portrait
        EXPECTED: Video Proceed playing in small window in portrait orientation with black background
        """
        pass
