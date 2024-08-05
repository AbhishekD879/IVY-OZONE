import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C29265_Watching_a_Racing_UK_RUK_Stream(Common):
    """
    TR_ID: C29265
    NAME: Watching a Racing UK (RUK) Stream
    DESCRIPTION: User is doing video adjustments while watching a stream
    PRECONDITIONS: 1. SiteServer event should be configured to support RUK/Perform streaming (**'typeFlagCodes'**='RVA , ... ' AND **'drilldownTagNames'**='EVFLAG_RVA' flags should be set) and should be mapped to RUK/Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: 3. User placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_003_open_event_details_page_of_any_race_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> for the event which satisfies Preconditions
        EXPECTED: 'Video stream' button is displayed
        """
        pass

    def test_004_clicktap_video_stream_button(self):
        """
        DESCRIPTION: Click/Tap 'Video stream' button
        EXPECTED: Stream is launched
        EXPECTED: Note: different devices will launch stream differently (via native player iOS, in page playing on Android)
        """
        pass

    def test_005_for_mobiletabletrotate_device_from_portrait_to_landscape_mode_and_vice_versa(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Rotate device from Portrait to Landscape mode and vice versa
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: Video stream is rotated accordingly
        """
        pass

    def test_006_pause_and_play_again_the_stream(self):
        """
        DESCRIPTION: Pause and play again the stream
        EXPECTED: It is possible to pause and play it again
        """
        pass

    def test_007_adjust_volume(self):
        """
        DESCRIPTION: Adjust volume
        EXPECTED: Volume can be adjusted
        """
        pass

    def test_008_all_devicesonly_mobiletablet_not_valid_for_desktopenter_and_exit_the_full_screen_view_of_the_video_player_using_provided_controlsrotate_the_device_from_portrait_to_landscape_mode_and_vice_versa_for_native_apps(self):
        """
        DESCRIPTION: All Devices(Only Mobile/Tablet, not valid for Desktop)
        DESCRIPTION: Enter and exit the Full Screen view of the Video player using provided controls
        DESCRIPTION: Rotate the device from Portrait to Landscape mode and vice versa for Native Apps.
        EXPECTED: Stream is resized full screen, playing correctly.
        EXPECTED: It is possible to minimize the player, exiting from Full Screen view.
        """
        pass
