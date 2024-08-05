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
class Test_C874341_Streaming__IMG(Common):
    """
    TR_ID: C874341
    NAME: Streaming - IMG
    DESCRIPTION: Video Streaming - Verify that the customer can see an IMG Sport video stream for the Live <Sport> event
    PRECONDITIONS: Following Sports are applicable for IMG streaming: Tennis, Football/Soccer, Snooker
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. Navigate to Backoffice>Admin>Media Content>Map IMG Streams
    PRECONDITIONS: 2. Search for streams by clicking on "Show events"
    PRECONDITIONS: 3. Check that an IMG stream is available and mapped to an event(**'drilldownTagNames'**='EVFLAG_IVM' flags should be set)
    PRECONDITIONS: 4. User is logged in into Oxygen app
    PRECONDITIONS: 5. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: __Notice:__
    PRECONDITIONS: How to find requests in dev tools? Take the event id from the address bar > open dev tools > Network > in Search enter event ID > find in searched results request that is started with "Optin"
    PRECONDITIONS: ![](index.php?/attachments/get/65165631)
    """
    keep_browser_open = True

    def test_001_navigate_to_in_playwatchlive_page(self):
        """
        DESCRIPTION: Navigate to '/in-play/watchlive' page
        EXPECTED: Content for the 'WATCH LIVE' tab of the 'IN-PLAY' page is opened
        EXPECTED: Live Now sub tab is selected by default
        """
        pass

    def test_002_tapclick_on_the_watch_live_icon_for_in_play_event_where_img_stream_is_mapped(self):
        """
        DESCRIPTION: Tap/click on the 'Watch Live' icon for In-Play event where IMG stream is mapped
        EXPECTED: The event details page is loaded
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
        EXPECTED: XHR - optin response contains IMG 'priorityProviderCode'
        EXPECTED: ![](index.php?/attachments/get/12251564)
        """
        pass

    def test_005_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_switch_to_live_stream(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and switch to 'Live Stream'
        EXPECTED: Stream of 1st event on a list is launched automatically
        EXPECTED: Stream is shown in the player frame below 'In-Play' and 'Live Stream' tabs
        """
        pass

    def test_006_make_the_event_from_step_2_appear_at_the_topas_first_one_of_the_live_stream_events_list_and_refresh_the_page(self):
        """
        DESCRIPTION: Make the event from step 2 appear at the top(as first one) of the Live Stream events list and refresh the page
        EXPECTED: Expected Results match those, described in step 5
        """
        pass
