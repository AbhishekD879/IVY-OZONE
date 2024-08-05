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
class Test_C141215_Launching_Stream_when_Streaming_is_finished(Common):
    """
    TR_ID: C141215
    NAME: Launching Stream when Streaming is finished
    DESCRIPTION: User is trying to launch the streaming when it is finished.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming ('drilldownTagNames' ='EVFLAG_GVM' and 'typeFlagCodes'='GVA' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 3. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: *   isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: __Notice:__
    PRECONDITIONS: How to find requests in dev tools? Take the event id from the address bar > open dev tools > Network > in Search enter event ID > find in searched results request that is started with "Optin"
    PRECONDITIONS: ![](index.php?/attachments/get/65165630)
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_greyhounds_racing_event_which_satisfies_preconditionsduring_the_period_of_stream_from__start_time_to_start_time_plus_1_min(self):
        """
        DESCRIPTION: Open Event Details page of any <Greyhounds Racing> event which satisfies Preconditions
        DESCRIPTION: (During the period of Stream from  'Start Time' to 'Start Time + 1 Min')
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_clicktap_live_stream__watch_button_while_stream_is_still_activeevent_end_time_is_not_due_yet(self):
        """
        DESCRIPTION: Click/Tap 'Live Stream' / 'Watch' button while stream is still active(event end time is not due yet)
        EXPECTED: Player frame appears below the clicked/tapped button.
        EXPECTED: Player starts the playback - stream is launched.
        """
        pass

    def test_003_view_the_stream_till_eventsstreams_actual_ending_time_comes_due(self):
        """
        DESCRIPTION: View the stream till event's(stream's) actual ending time comes due
        EXPECTED: 'Stream has ended' message is shown within the player frame in a form of white text.
        EXPECTED: (NOTE: This response is received from a Streaming provider GVM)
        EXPECTED: Player remains opened
        """
        pass

    def test_004_refresh_the_event_details_page_and_clicktap_live_stream__watch_button_for_the_same_stream_that_has_just_ended(self):
        """
        DESCRIPTION: Refresh the event details page and Click/Tap 'Live Stream' / 'Watch' button for the same stream that has just ended
        EXPECTED: [ Coral desktop / Ladbrokes desktop]: Message is displayed: 'The Stream for this event is currently not available.'
        EXPECTED: [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message 'The Stream for this event is currently not available.'
        """
        pass
