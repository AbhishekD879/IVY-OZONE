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
class Test_C874342_Streaming__Perform(Common):
    """
    TR_ID: C874342
    NAME: Streaming - Perform
    DESCRIPTION: UPD: Should be separated for Sports, Horse races (iFrame and rules)
    DESCRIPTION: Video Streaming - Verify that the customer can see an Perform Sport video stream for the Live <Sport>/<Race> event
    PRECONDITIONS: Following Sports/Races are applicable for Peform streaming: Basketball, Soccer/Football, Tennis, Horse Racing, Greyhounds Racing
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. Navigate to Backoffice > Admin > Media Content > Map Perform Streams
    PRECONDITIONS: 2. Search for streams by clicking on "Show events"
    PRECONDITIONS: 3. Check that a Perform stream is available and mapped to an event ( __'typeFlagCodes'__ = 'PVA , ... ' AND __'drilldownTagNames'__ ='EVFLAG_PVM' flags should be set)
    PRECONDITIONS: 4. User is logged in into Oxygen app
    PRECONDITIONS: 5. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: for <Race> events:
    PRECONDITIONS: *   isStarted = "false"; it should be less than 2 minutes left before event Start Time.
    PRECONDITIONS: for <Sport> events:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: **NOTE:** Test case should be run twice - once for <Sport>/<Race> event, excluding Horse Racing UK, and second time for Horse Racing UK <Race> event.
    PRECONDITIONS: For Horse racing UK next preparations should be made:
    PRECONDITIONS: 2.1. In CMS-System C88onfiguration - Structure two next properties should be added:
    PRECONDITIONS: * **CSBIframeEnabled** with checkbox checked
    PRECONDITIONS: * **CSBIframeSportIds** with category ID as value (e.g. 21 for Horse Racing)
    PRECONDITIONS: __Notice:__
    PRECONDITIONS: How to find requests in dev tools? Take the event id from the address bar > open dev tools > Network > in Search enter event ID > find in searched results request that is started with "Optin"
    PRECONDITIONS: **NOTE: If by any circumstances you have no way of verifying this case on <Sport> events, please verify it on <Race> events and leave a corresponding comment as a result of a test case run.**
    PRECONDITIONS: ![](index.php?/attachments/get/65165632)
    """
    keep_browser_open = True

    def test_001_navigate_to_in_playwatchlive_page(self):
        """
        DESCRIPTION: Navigate to '/in-play/watchlive' page
        EXPECTED: Content for the 'WATCH LIVE' tab of the 'IN-PLAY' page is opened
        EXPECTED: Live Now sub tab is selected by default
        """
        pass

    def test_002_tapclick_on_the_watch_live_icon_for_in_play_event_where_perform_stream_is_mapped(self):
        """
        DESCRIPTION: Tap/click on the 'Watch Live' icon for In-Play event where Perform stream is mapped
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
        EXPECTED: **for <Sport>/<Race> event, excluding Horse Racing UK**
        EXPECTED: - The Video player is shown above market tabs
        EXPECTED: - The Video stream is shown within the player
        """
        pass

    def test_005_open_event_details_page_of_any_race_eventhorsegreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Horse/Greyhounds Racing) which satisfies Preconditions
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
        EXPECTED: **for <Sport>/<Race> event, excluding Horse Racing UK**
        EXPECTED: - The Video player is shown above market tabs
        EXPECTED: - The Video stream is shown within the player
        EXPECTED: **for Horse Racing UK <Race> event**
        EXPECTED: iFrame is displayed, stream is launched
        EXPECTED: ![](index.php?/attachments/get/104494307)
        EXPECTED: (Ladbrokes)
        EXPECTED: - Stream button changes from 'Watch' to 'Done'
        EXPECTED: (Coral)
        EXPECTED: - Stream button remains 'Live Stream' when clicked on.
        EXPECTED: XHR - optin response contains Perform 'priorityProviderCode'
        EXPECTED: ![](index.php?/attachments/get/62232950)
        """
        pass
