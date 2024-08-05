import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1274909_Greyhound_Race_Meetings_on_Today_tab(Common):
    """
    TR_ID: C1274909
    NAME: Greyhound Race Meetings on Today tab
    DESCRIPTION: This test case verifies Race Meetings displaying within Greyhound Race Grid
    DESCRIPTION: New design (Ladbrokes Desktop): https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: To get the UK/Irish/International daily races events check modules (modules name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of event structure:
    PRECONDITIONS: **flag:** "UK",
    PRECONDITIONS: **data:** [{
    PRECONDITIONS: **id:** "230549330",
    PRECONDITIONS: **categoryId:** "21",
    PRECONDITIONS: **categoryName:** "Horse Racing",
    PRECONDITIONS: **className:** "Horse Racing - Live",
    PRECONDITIONS: **name:** "Southwell",
    PRECONDITIONS: **typeName:** "Southwell",
    PRECONDITIONS: **startTime:** 1593614400000,
    PRECONDITIONS: **classId:** "285",
    PRECONDITIONS: **cashoutAvail:** "Y",
    PRECONDITIONS: **poolTypes:**  ["UPLP", "UQDP"],
    PRECONDITIONS: **liveStreamAvailable:** true,
    PRECONDITIONS: **isResulted:** false,
    PRECONDITIONS: **isStarted:** false,
    PRECONDITIONS: **eventIsLive:** false,
    PRECONDITIONS: **isFinished:** false,
    PRECONDITIONS: **isBogAvailable:** false,
    PRECONDITIONS: **isLpAvailable:** false,
    PRECONDITIONS: **drilldownTagNames:** "EVFLAG_BL,EVFLAG_AVA,",
    PRECONDITIONS: **localTime:** "15:40"
    PRECONDITIONS: **markets:** [{
    PRECONDITIONS: **drilldownTagNames:** 'MKTFLAG_EPR',
    PRECONDITIONS: **eachWayFactorNum:** 1,
    PRECONDITIONS: **eachWayFactorDen:** 2,
    PRECONDITIONS: **eachWayPlaces:** 3,
    PRECONDITIONS: **isEachWayAvailable:** true
    PRECONDITIONS: Parameter  **'typeName'**  defines 'Race Meetings' name
    PRECONDITIONS: Parameter **'startTime'** defines event start time (note, this is not a race local time)
    PRECONDITIONS: **New changes:
    PRECONDITIONS: Added "simpleFilter=class.hasOpenEvent" query to /Class request to receive info only about classes with available events.
    PRECONDITIONS: Removed request /EventToOutcomeForClass/201 on Ladbrokes (Specials Events).
    PRECONDITIONS: Removed simpleFilter=event.categoryId:intersects:21 from request /EventToOutcomeForClass (horse racing category id: 21, greyhound category id: 19)
    PRECONDITIONS: Added to /EventToOutcomeForClass filter &limitRecords=outcome:1, &limitRecords=market:1
    PRECONDITIONS: Date range should be: 1 day (today or tomorrow).
    PRECONDITIONS: Only one WS connection is between switching By Meeting/By time tab (Coral greyhounds).
    PRECONDITIONS: **REMOVED FUNCTIONALITY:**
    PRECONDITIONS: GH Statuses are received in the push updates:
    PRECONDITIONS: 'race_stage'='A' correspond to 'Parading' status
    PRECONDITIONS: 'race_stage'='F' correspond to 'Approaching Traps' status
    PRECONDITIONS: 'race_stage'='G' correspond to 'Going into Traps' status
    PRECONDITIONS: 'race_stage'='R' correspond to 'Hare' status
    PRECONDITIONS: 'race_stage'='W' correspond to 'Awaiting Result' status
    PRECONDITIONS: 'race_stage'='O' correspond to 'Race is Off' status
    PRECONDITIONS: NOTE that not all statuses are received from SS
    PRECONDITIONS: Cashout icons are removed for LADBROKES within the story BMA-39817
    PRECONDITIONS: - Load the app
    PRECONDITIONS: - Navigate to the Greyhound landing page -> 'TODAY'tab is selected by default
    """
    keep_browser_open = True

    def test_001_check_the_order_of_race_meetings_inside_the_race_grid_sections_egukireland_races_virtual_races(self):
        """
        DESCRIPTION: Check the order of race meetings inside the race grid sections (e.g.UK/IRELAND RACES, VIRTUAL RACES)
        EXPECTED: Race meetings are ordered in ascending alphabetical order (A-Z)
        """
        pass

    def test_002_verify_race_meeting_sections_content(self):
        """
        DESCRIPTION: Verify Race meeting sections content
        EXPECTED: * Race meeting header
        EXPECTED: * Row of events start time
        EXPECTED: * Race status (RESULT, RACE OFF)
        """
        pass

    def test_003_verify_race_meeting_header_line_content(self):
        """
        DESCRIPTION: Verify Race meeting header line content
        EXPECTED: * Race meeting name on the left
        EXPECTED: * Each race meeting name corresponds to the '**typeName'** parameter from the Site Server response
        EXPECTED: * Race meeting name is NOT clickable
        EXPECTED: * 'Live Stream' icon (if available) on the right
        """
        pass

    def test_004_only_coral_verify_cash_out_icon_displaying(self):
        """
        DESCRIPTION: Only Coral: Verify 'Cash Out' icon displaying
        EXPECTED: **FOR CORAL Only**
        EXPECTED: 'CASH OUT' icon is shown if at least one of it's events has cashoutAvail="Y" and on all higher levels cashoutAvail="Y"
        """
        pass

    def test_005_verify_live_stream_icon(self):
        """
        DESCRIPTION: Verify 'Live Stream' icon
        EXPECTED: * Stream icon is displayed (if available)
        EXPECTED: * **FOR CORAL** Play icon for races with live stream (if available) on the right
        EXPECTED: * **FOR LADBROKES** WATCH icon for races with live stream (if available) on the right
        EXPECTED: * Stream icon is shown for event type where at least 1 event has a stream available on event level ("mediaTypeCodes" parameter is available in SS response)
        EXPECTED: * Stream icon is for informational purpose only (not clickable)
        """
        pass

    def test_006_verify_row_of_events_displaying(self):
        """
        DESCRIPTION: Verify row of events displaying
        EXPECTED: * Event off times are displayed horizontally across the page
        EXPECTED: * **FOR CORAL** Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        EXPECTED: * **FOR LADBROKES** ALL events off times are displayed in bold no matter if it is 'LP' or 'SP' prices
        EXPECTED: * Ladbrokes: Race Statuses displayed for started or resulted events:
        EXPECTED: - Race Off - event has 'isOff=Yes'
        EXPECTED: - Live - event has 'isOff=Yes'and at least one of markets has 'betInRunning=true'
        EXPECTED: - Resulted - event has 'isResulted=true' + 'isFinished=true'
        EXPECTED: * Coral:  Signposting icons are displayed next to event off time (if available)
        EXPECTED: Ladbrokes: Signposting icons are NOT displayed next to event off time
        """
        pass

    def test_007_verify_event_off_times(self):
        """
        DESCRIPTION: Verify event off times
        EXPECTED: Event off times corresponds to the race local time from the **'name'** attribute from the Site Server
        """
        pass

    def test_008_verify_scrolling_between_event_off_times(self):
        """
        DESCRIPTION: Verify scrolling between event off times
        EXPECTED: On **Mobile/Tablet** ability to scroll left and right is available via swiping
        EXPECTED: On **Desktop** Race meeting with too many event off times to be shown in one line has arrows which appear on hover to scroll horizontally
        EXPECTED: Events off times are scrolled one by one after click arrows
        """
        pass

    def test_009_tap_on_event_off_time(self):
        """
        DESCRIPTION: Tap on event off time
        EXPECTED: Corresponding Event details page is opened
        """
        pass

    def test_010_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Greyhound Landing page is opened
        """
        pass
