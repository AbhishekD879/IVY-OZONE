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
class Test_C141219_Watching_a_iGameMedia_GVM_Stream(Common):
    """
    TR_ID: C141219
    NAME: Watching a iGameMedia (GVM) Stream
    DESCRIPTION: User is doing video adjustments while watching a stream
    DESCRIPTION: Applies to <Race>(<Tote>)/<Sport> events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming ( **'drilldownTagNames'** ='EVFLAG_GVM' flag should be set) and should be mapped to GVM stream event
    PRECONDITIONS: 2. The event should have the following attributes:
    PRECONDITIONS: **isStarted** = "true"
    PRECONDITIONS: 3. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 4. The following parameters should be received in Optin MS response in order play IGMedia stream on mentioned devices/platforms:
    PRECONDITIONS: mobile: ['HLS-LOW'],
    PRECONDITIONS: wrapper: ['HLS-LOW-RAW'] (video URL link is available and native player works as expected, in another case - error that stream is not available is displayed),
    PRECONDITIONS: tablet: ['HLS-HIGH', 'HLS-LOW'],
    PRECONDITIONS: desktop: ['HLS-WEB', 'DASH', 'RTMP-HIGH']
    PRECONDITIONS: =====
    PRECONDITIONS: please note that there is different expected behavior for wrappers, described in https://ladbrokescoral.testrail.com/index.php?/cases/view/905009
    PRECONDITIONS: e.g. there is no play/pause buttons in portrait mode, etc.
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_racetote_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race>/<Tote> for the event which satisfies Preconditions
        EXPECTED: For Mobile/Tablet:
        EXPECTED: 'Live Stream' button is displayed below the HH:MM #EVENT_NAME
        EXPECTED: For Desktop:
        EXPECTED: 'LIVE STREAM' button is displayed below the HH:MM #EVENT_NAME
        """
        pass

    def test_002_clicktap_live_stream__live_stream_button(self):
        """
        DESCRIPTION: Click/Tap 'LIVE STREAM' / 'Live Stream' button
        EXPECTED: Player frame appears below the clicked/tapped button.
        EXPECTED: Player starts the playback - stream is launched.
        """
        pass

    def test_003_mobiletablet_tap_on_full_screen_icon(self):
        """
        DESCRIPTION: Mobile/Tablet: Tap on 'Full Screen' icon
        EXPECTED: Stream is resized full screen according to a view(portrait) the device is in and playing correctly.
        """
        pass

    def test_004_pause_and_play_the_stream_by_clickingtapping_on_pauseplay_buttons(self):
        """
        DESCRIPTION: Pause and Play the stream by clicking/tapping on Pause/Play buttons
        EXPECTED: It is possible to pause and play it again
        """
        pass

    def test_005_adjust_volume_with_a_device_volume_buttonsor_os_built_in_tools(self):
        """
        DESCRIPTION: Adjust volume with a device volume buttons(or OS built-in tools)
        EXPECTED: Volume can be increased/decreased
        """
        pass

    def test_006_mobiletablet_rotate_the_device_into_a_landscape_view(self):
        """
        DESCRIPTION: Mobile/Tablet: Rotate the device into a Landscape view
        EXPECTED: Stream is resized full screen according to a view(landscape) the device is in and playing correctly.
        """
        pass

    def test_007_mobiletablet_tap_on_speaker_icon_twice(self):
        """
        DESCRIPTION: Mobile/Tablet: Tap on 'Speaker' icon twice
        EXPECTED: Icon changes to 'Crossed out Speaker' on a first tap, muting the sound completely
        EXPECTED: Icon changes back to 'Speaker' on a second tap, unmuting the sound of the stream
        """
        pass

    def test_008_mobiletablet_tap_on_exit_full_screen_icon(self):
        """
        DESCRIPTION: Mobile/Tablet: Tap on 'Exit Full Screen' icon
        EXPECTED: Player frame is shown in the portrait view as in expected result of the Step #2.
        EXPECTED: Player stops the playback - stream is paused.
        """
        pass

    def test_009_desktop_onlyverify_full_screen_icon_is_not_displayed(self):
        """
        DESCRIPTION: [Desktop only]Verify 'Full Screen' icon is not displayed
        EXPECTED: 'Full Screen' icon is not displayed. It's not possible to watch video in full screen on Desktop
        """
        pass

    def test_010_open_event_details_page_of_any_sport_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which satisfies Preconditions
        EXPECTED: For Mobile/Tablet:
        EXPECTED: 'Watch Live' button is displayed on the right side of 'Markets' block
        EXPECTED: For Desktop:
        EXPECTED: Player frame appears above 'ALL MARKETS' and 'OTHER MARKETS' tabs
        EXPECTED: Player starts the playback - stream is launched.
        """
        pass

    def test_011_tap_watch_live_button_on_mobiletablet_device(self):
        """
        DESCRIPTION: Tap 'Watch Live' button on Mobile/Tablet device
        EXPECTED: Player frame appears above the tapped button.
        EXPECTED: Player starts the playback - stream is launched.
        """
        pass

    def test_012_repeat_steps_3___9(self):
        """
        DESCRIPTION: Repeat steps #3 - #9
        EXPECTED: 
        """
        pass
