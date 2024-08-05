import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29274_Watching_a_Racing_Post_Greyhound_TV_RPGTV_Stream(Common):
    """
    TR_ID: C29274
    NAME: Watching a Racing Post Greyhound TV (RPGTV) Stream
    DESCRIPTION: User is doing video adjustments while watching a stream
    PRECONDITIONS: 1. SiteServer event should be configured to support RPGTV streaming (**'typeFlagCodes'**='RPG, ... ' AND **'drilldownTagNames'**='EVFLAG_RPM' flags should be set) and should be mapped to RPGTV stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: *   isMarketBetInRun = "true" (applicable for <Sports> only)
    PRECONDITIONS: 3. User placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_with_credentials_with_positive_balance(self):
        """
        DESCRIPTION: Login with credentials with positive balance
        EXPECTED: User is logged in
        """
        pass

    def test_003_open_event_details_page_of_any_race_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> for the event which satisfies Preconditions
        EXPECTED: 'Video Stream' button is displayed
        """
        pass

    def test_004_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: Stream is launched
        EXPECTED: Note: different devices will launch stream differently (via native player iOS, in page playing on Android)
        """
        pass

    def test_005_mobiletabletrotate_device_from_portrait_to_landscape_mode_and_vice_versa(self):
        """
        DESCRIPTION: [Mobile,Tablet]Rotate device from Portrait to Landscape mode and vice versa
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

    def test_008_all_devicesonly_mobiletablet_not_valid_for_desktopenter_and_exit_the_full_screen_view_of_the_video_player_using_provided_controls(self):
        """
        DESCRIPTION: All Devices(Only Mobile/Tablet, not valid for Desktop)
        DESCRIPTION: Enter and exit the Full Screen view of the Video player using provided controls
        EXPECTED: Stream is resized full screen, playing correctly.
        EXPECTED: It is possible to minimize the player, exiting from Full Screen view.
        """
        pass
