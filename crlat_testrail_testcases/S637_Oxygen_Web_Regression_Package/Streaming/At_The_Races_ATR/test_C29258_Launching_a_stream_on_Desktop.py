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
class Test_C29258_Launching_a_stream_on_Desktop(Common):
    """
    TR_ID: C29258
    NAME: Launching a stream on Desktop
    DESCRIPTION: This test case verifies ATR stream launching on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (Chrome) and Mac OS (Safari).
    PRECONDITIONS: 1. SiteServer event should be configured to support ATR streaming ('drilldownTagNames'='EVFLAG_AVA' flag should be set) and should be mapped to ATR stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: * isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: or
    PRECONDITIONS: * isStarted = "false", but there are less than 2 minutes before the stream 'start time'
    PRECONDITIONS: * isMarketBetInRun = "true"
    PRECONDITIONS: 3. Desktop browser view is opened
    PRECONDITIONS: 4. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event which satisfies Preconditions
        EXPECTED: (Coral) 'Live Stream' ![](index.php?/attachments/get/3050952) button is shown below the event name line
        EXPECTED: (Ladbrokes) 'Watch' ![](index.php?/attachments/get/3050953) button is shown below the event name line
        """
        pass

    def test_002_when_event_is_started_click_on_live_stream_button(self):
        """
        DESCRIPTION: When event is started click on 'Live Stream' button
        EXPECTED: Video is launched successfully
        """
        pass

    def test_003_try_to_turn_on_full_mode_for_desktop_video_player(self):
        """
        DESCRIPTION: Try to turn on full mode for desktop video player
        EXPECTED: There is no full mode for desktop video player
        """
        pass
