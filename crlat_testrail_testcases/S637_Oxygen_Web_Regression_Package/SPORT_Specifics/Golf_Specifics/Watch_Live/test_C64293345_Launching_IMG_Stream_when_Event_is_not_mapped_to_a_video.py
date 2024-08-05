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
class Test_C64293345_Launching_IMG_Stream_when_Event_is_not_mapped_to_a_video(Common):
    """
    TR_ID: C64293345
    NAME: Launching IMG Stream when Event is not mapped to a video
    DESCRIPTION: User is trying to launch a stream for an event which is not mapped to a video
    DESCRIPTION: Applies to Golf events
    PRECONDITIONS: Attribute 'drilldownTagNames'='EVFLAG_IVM' should be set for event, however NO real stream should be mapped through BACKOFFICE -> ADMIN
    PRECONDITIONS: Event should be started.
    PRECONDITIONS: User is logged in and has a positive balance
    PRECONDITIONS: Endpoints of Optin MS:
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    """
    keep_browser_open = True

    def test_001_open_event_details_page_for_the_golf_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page for the golf event which satisfies Preconditions
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

    def test_002_for_desktop_onlyverify_that_warning_message_is_shown_on_edp_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Verify that warning message is shown on EDP (if no stream buttons are shown)
        EXPECTED: Warning message with following text is shown above the market tabs lane: 'The Stream for this event is currently not available'
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: [ Coral desktop / Ladbrokes desktop]: Message is displayed: 'The Stream for this event is currently not available'.
        EXPECTED: [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message 'The Stream for this event is currently not available'.
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider, with a following response:
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_004_for_desktop_onlynavigate_to_in_play_and_live_stream_section_on_homepage_and_switch_to_live_stream(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Navigate to 'IN-PLAY AND LIVE STREAM' section on Homepage and switch to 'LIVE STREAM'
        EXPECTED: Stream of 1st event on a list is launched automatically
        EXPECTED: Stream is shown in the player frame below 'In-Play' and 'Live Stream' tabs
        """
        pass

    def test_005_for_desktop_onlymake_the_event_from_step_2_appear_at_the_topas_first_one_of_the_live_stream_events_list_and_refresh_the_page(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Make the event from step 2 appear at the top(as first one) of the Live Stream events list and refresh the page
        EXPECTED: Message is displayed: 'The Stream for this event is currently not available'.
        EXPECTED: User is not able to watch the stream
        """
        pass
