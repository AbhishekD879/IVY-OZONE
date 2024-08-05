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
class Test_C29254_Watching_a_At_The_Races_ATR_Stream(Common):
    """
    TR_ID: C29254
    NAME: Watching a At The Races (ATR) Stream
    DESCRIPTION: User is doing video adjustments while watching a stream.
    DESCRIPTION: Need to run the test case on Mobile/Tablet.
    PRECONDITIONS: 1. SiteServer event should be configured to support ATR streaming (**'drilldownTagNames'**='EVFLAG_AVA' flag should be set) and should be mapped to ATR stream event
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

    def test_002_login_with_credentials_with_positive_balance(self):
        """
        DESCRIPTION: Login with credentials with positive balance
        EXPECTED: User is logged in
        """
        pass

    def test_003_open_event_details_page_of_any_racetote_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race>/<Tote> for the event which satisfies Preconditions
        EXPECTED: 'Live Stream' button is displayed
        """
        pass

    def test_004_tap_live_stream_button(self):
        """
        DESCRIPTION: Tap 'Live Stream' button
        EXPECTED: Player frame appears below the clicked/tapped button.
        EXPECTED: Player starts the playback - stream is launched. (Mobile/Tablet IOS devices will put the Stream on pause)
        """
        pass

    def test_005_only_mobiletablet_for_desktop_icon_is_missingtap_on_full_screen_icon(self):
        """
        DESCRIPTION: (Only Mobile/Tablet, for Desktop icon is missing)Tap on 'Full Screen' icon
        EXPECTED: Stream is resized full screen according to a view(portrait) the device is in and playing correctly.
        """
        pass

    def test_006_adjust_volume_with_a_device_volume_buttons(self):
        """
        DESCRIPTION: Adjust volume with a device volume buttons
        EXPECTED: Volume can be increased/decreased
        """
        pass

    def test_007_rotate_the_device_into_a_landscape_view(self):
        """
        DESCRIPTION: Rotate the device into a Landscape view
        EXPECTED: Stream is resized full screen according to a view(landscape) the device is in and playing correctly.
        """
        pass

    def test_008_tap_on_speaker_icon_twice(self):
        """
        DESCRIPTION: Tap on 'Speaker' icon twice
        EXPECTED: Icon changes to 'Crossed out Speaker' on a first tap, muting the sound completely
        EXPECTED: Icon changes back to 'Speaker' on a second tap, unmuting the sound of the stream
        """
        pass

    def test_009_tap_on_exit_full_screen_icon(self):
        """
        DESCRIPTION: Tap on 'Exit Full Screen' icon
        EXPECTED: Player frame is shown in the portrait view as in expected result of the Step #4.
        EXPECTED: Player stops the playback - stream is paused.
        """
        pass
