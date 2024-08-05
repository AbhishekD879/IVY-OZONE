import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.streaming
@vtest
class Test_C2064715_Streaming__IGameMedia(Common):
    """
    TR_ID: C2064715
    NAME: Streaming - IGameMedia
    DESCRIPTION: Video Streaming - Verify that the customer can see an IGameMedia Sport video stream for the Live <Sport>/<Race> event
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. Navigate to Backoffice > Admin > Media Content > Map IGMedia Streams
    PRECONDITIONS: 2. Search for streams by clicking on 'Show events'
    PRECONDITIONS: 3. Check that an IGM stream is available and mapped to an event
    PRECONDITIONS: (SiteServer event should be configured to support IGM streaming ( 'drilldownTagNames' ='EVFLAG_GVM' flag should be set) and should be mapped to IGM stream event
    PRECONDITIONS: 4. User is logged in into Oxygen app
    PRECONDITIONS: 5. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: for <Race> events:
    PRECONDITIONS: *   isStarted = "false"; it should be less than 2 minutes left before event Start Time.
    PRECONDITIONS: for <Sport> events:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: The following parameters should be received in response to possibility play IGM stream on:
    PRECONDITIONS: mobile: HLS-HIGH, HLS-LOW, HLS-WEB;
    PRECONDITIONS: desktop: HLS-WEB, DASH, RTMP-HIGH;
    PRECONDITIONS: wrappers: RAW (video URL link is available and native player works as expected, in another case - error that stream is not available is displayed);
    PRECONDITIONS: __Notice:__
    PRECONDITIONS: How to find requests in dev tools? Take the event id from the address bar > open dev tools > Network > in Search enter event ID > find in searched results request that is started with "Optin"
    PRECONDITIONS: **NOTE: If by any circumstances you have no way of verifying this case on <Sport> events, please verify it on <Race> events and leave a corresponding comment as a result of a test case run.**
    PRECONDITIONS: ![](index.php?/attachments/get/65165630)
    """
    keep_browser_open = True

    def test_001_navigate_to_in_playwatchlive_page(self):
        """
        DESCRIPTION: Navigate to '/in-play/watchlive' page
        EXPECTED: Content for the 'WATCH LIVE' tab of the 'IN-PLAY' page is opened
        EXPECTED: Live Now sub tab is selected by default
        """
        pass

    def test_002_tapclick_on_the_watch_live_icon_for_in_play_basketball_event_where_igamemedia_stream_is_mapped(self):
        """
        DESCRIPTION: Tap/click on the 'Watch Live' icon for In-Play 'Basketball' event where IGameMedia stream is mapped
        EXPECTED: The event details page(EDP) is loaded
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'Watch Live' button is displayed when Visualization/Scoreboard is mapped
        EXPECTED: * 'Watch' button is displayed when Visualization/Scoreboard is NOT mapped
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Watch Live' button is displayed when Visualization/Scoreboard is mapped
        EXPECTED: * No stream buttons are shown if Stream is available WITHOUT mapped Visualization/Scoreboard
        """
        pass

    def test_003_for_desktop_only_skip_this_step_if_stream_buttons_are_shownverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:** (skip this step if stream buttons are shown)
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: - The Video player is shown above market tabs
        EXPECTED: - The Video stream is shown within the player
        EXPECTED: No stream buttons appear for the player
        """
        pass

    def test_004_clicktap_on_watch_livewatch_button(self):
        """
        DESCRIPTION: Click/Tap on 'Watch Live'/'Watch' button
        EXPECTED: - The Video player is shown above market tabs
        EXPECTED: - The Video stream is shown within the player
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: - Stream button changes from 'Watch' to 'Done'
        EXPECTED: - Stream button changes from 'Watch Live' to 'Stop'
        EXPECTED: XHR - optin response contains iGameMedia 'priorityProviderCode'
        EXPECTED: ![](index.php?/attachments/get/11918131)
        """
        pass

    def test_005_open_event_details_page_of_any_race_eventgreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Greyhounds Racing) which satisfies Preconditions
        EXPECTED: The event details page(EDP) is loaded
        EXPECTED: Desktop:
        EXPECTED: 'Live Stream' (Coral) / 'Watch' (Ladbrokes) button is shown below the event name line
        EXPECTED: Mobile/Tablet:
        EXPECTED: 'Live Stream' (Coral) / 'Watch' (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_006_place_a_minimum_sum_of_1_15_15_on_1_or_many_selections_within_the_tested_event(self):
        """
        DESCRIPTION: Place a minimum sum of 1£ (1.5$, 1.5Є) on 1 or many selections within the tested event
        EXPECTED: 
        """
        pass

    def test_007_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices:**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: - The Video player is shown above market tabs
        EXPECTED: - The Video stream is shown within the player
        EXPECTED: (Ladbrokes)
        EXPECTED: - Stream button changes from 'Watch' to 'Done'
        EXPECTED: (Coral)
        EXPECTED: - Stream button remains 'Live Stream' when clicked on.
        EXPECTED: XHR - optin response contains iGameMedia 'priorityProviderCode'
        EXPECTED: ![](index.php?/attachments/get/11918131)
        """
        pass
