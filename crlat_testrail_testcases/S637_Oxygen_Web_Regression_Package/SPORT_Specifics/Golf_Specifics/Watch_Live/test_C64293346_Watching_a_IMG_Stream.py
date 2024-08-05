import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64293346_Watching_a_IMG_Stream(Common):
    """
    TR_ID: C64293346
    NAME: Watching a IMG Stream
    DESCRIPTION: User is doing video adjustments while watching a stream.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: SiteServer event should be configured to support IMG streaming (**'typeFlagCodes'**='IVA , ... ' AND 'drilldownTagNames'='EVFLAG_IVM' flags should be set) and should be mapped to IMG stream event
    PRECONDITIONS: Event should have the following attributes:
    PRECONDITIONS: isStarted = "true"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: User is logged in to the Oxygen app and has positive balance.
    PRECONDITIONS: Endpoints of Optin MS:
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    PRECONDITIONS: The next provider info should received from Optin MS when stream is launched:
    PRECONDITIONS: {
    PRECONDITIONS: priorityProviderCode: "IMG"
    PRECONDITIONS: priorityProviderName: "IMG Video Streaming"
    PRECONDITIONS: }
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any for the event which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: For Mobile/Tablet:
        EXPECTED: 'Watch Live' button is shown when scoreboard is present(for both brands);
        EXPECTED: 'Watch'  (Coral) /  (Ladbrokes) button is shown when scoreboard is absent.
        EXPECTED: -
        EXPECTED: For Desktop:
        EXPECTED: 'Watch Live'  (Coral) /  (Ladbrokes) button is shown in case of scoreboard/visualization being present.
        EXPECTED: No stream buttons are shown if Stream is available WITHOUT mapped Visualization/Scoreboard
        """
        pass

    def test_002_for_desktop_onlyverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: Stream is launched
        EXPECTED: The Video player is shown above market tabs
        EXPECTED: Player contains following controls: Play/Pause; Mute/Unmute; Fullscreen (Only Mobile/Tablet, absent on Desktop)/Default size.
        EXPECTED: No stream buttons(Watch Live/Watch) appear for the player
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: Stream is launched
        EXPECTED: For Mobile/Tablet:
        EXPECTED: Note: Depending on where you are launching the stream(wrapper/browser) a different type of player will be summoned(native/built-in browser)
        EXPECTED: Native iOS/Android contains following controls:
        EXPECTED: (Portrait view): Mute/Unmute; Close player; Back to Event; Shrink Player.
        EXPECTED: (Landscape view): Pause/Play; Increase/Decrease Sound; Shrink Player.
        EXPECTED: Android/iOS built-in browser player contains following controls: Play/Pause; Mute/Unmute; Fullscreen/Default size.
        EXPECTED: For Desktop:
        EXPECTED: Desktop Player contains following controls: Play/Pause; Mute/Unmute; Fullscreen(Only Mobile/Tablet, absent on Desktop)/Default size.
        EXPECTED: Video player is shown above market tabs(for all devices)
        """
        pass

    def test_004_all_devicespause_and_play_the_stream_again_using_provided_controls(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Pause and Play the stream again using provided controls
        EXPECTED: It is possible to pause and play it again
        """
        pass

    def test_005_all_devicesadjust_volume_with_provided_controls_muteunmute_increasedecrease_soundnative_player(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Adjust volume with provided controls (Mute/Unmute; Increase/Decrease Sound[Native player])
        EXPECTED: Volume can be adjusted
        """
        pass

    def test_006_all_devicesonly_mobiletablet_not_valid_for_desktopenter_and_exit_the_full_screen_view_of_the_video_player_using_provided_controlsrotate_the_device_from_portrait_to_landscape_mode_and_vice_versa_for_native_apps(self):
        """
        DESCRIPTION: All Devices(Only Mobile/Tablet, not valid for Desktop)
        DESCRIPTION: Enter and exit the Full Screen view of the Video player using provided controls
        DESCRIPTION: Rotate the device from Portrait to Landscape mode and vice versa for Native Apps.
        EXPECTED: Stream is resized full screen, playing correctly.
        EXPECTED: It is possible to minimize the player, exiting from Full Screen view.
        """
        pass
