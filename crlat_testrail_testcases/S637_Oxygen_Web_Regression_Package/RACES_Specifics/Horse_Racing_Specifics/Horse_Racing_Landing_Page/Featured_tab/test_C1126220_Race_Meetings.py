import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C1126220_Race_Meetings(Common):
    """
    TR_ID: C1126220
    NAME: Race Meetings
    DESCRIPTION: This test verifies Race Meetings displaying within Race Grids sections
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
    PRECONDITIONS: Parameter **typeName** defines 'Race Meetings' name
    PRECONDITIONS: Parameter 'startTime' defines event start time (note, this is not a race local time)
    PRECONDITIONS: To set the sort order of such sections as 'UK and Irish Races',  'International Tote Carousel', 'International Races', 'Virtual Race Carousel', 'Ladbrokes/Coral Legends' can be set in CMS by drag and drop:
    PRECONDITIONS: CMS/Sport Pages/Sport Categories/Horse Racing
    PRECONDITIONS: REMOVED FUNCTIONALITY:
    PRECONDITIONS: (Not related to BETA)
    PRECONDITIONS: List of HR Statuses:
    PRECONDITIONS: 'race_stage'='**D**' correspond to 'Delayed' badge
    PRECONDITIONS: 'race_stage'='**B**' correspond to 'Going Down' badge
    PRECONDITIONS: 'race_stage'='**C**' correspond to 'At the Post' badge
    PRECONDITIONS: 'race_stage'='**E**' correspond to 'Going Behind' badge
    PRECONDITIONS: 'race_stage'='**O**' correspond to 'Off' badge
    PRECONDITIONS: 'race_stage'='**W**' correspond to 'Awaiting Result' badge
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_sport_page___featured_tab___uk__ire_race_grid(self):
        """
        DESCRIPTION: Navigate to Horse Racing sport page -> Featured tab -> UK & IRE race grid
        EXPECTED: * Tab for first available day is opened by default
        EXPECTED: * List of Race meeting sections for first day tab is displayed
        """
        pass

    def test_002_check_order_of_race_meetings(self):
        """
        DESCRIPTION: Check order of race meetings
        EXPECTED: Race meetings are ordered according to "Disporder" parameter from TI tool for appropriate racing type (Open TI for Horses and check the order of displayed race stadiums)
        EXPECTED: Note: Race sections order can be set in CMS as described in Preconditions
        """
        pass

    def test_003_verify_race_meeting_sections_contentchose_any_horse_racing_stadium_name_section(self):
        """
        DESCRIPTION: Verify Race meeting sections content:
        DESCRIPTION: (Chose any Horse racing stadium name section)
        EXPECTED: * Race meeting header line - Horse racing stadium name;
        EXPECTED: * Row of events start time - list of times when races will start;
        """
        pass

    def test_004_verify_race_meeting_header_line_content(self):
        """
        DESCRIPTION: Verify Race meeting header line content
        EXPECTED: * Race race meeting name on the left
        EXPECTED: * Each race meeting name corresponds to the '**typeName'** parameter from the Site Server response
        EXPECTED: * Race meeting name is NOT clickable
        EXPECTED: * Cash Out / Live Stream icon (if available) on the right
        """
        pass

    def test_005_verify_next_race_section_statuses_displaying(self):
        """
        DESCRIPTION: Verify "Next Race" section statuses displaying
        EXPECTED: * Race status badges are not displayed
        EXPECTED: REMOVED FUNCTIONALITY: Next Race status is displayed (if available) for the most recent available event from corresponding meeting grid (if received from push update or SiteServe response) in next format:
        EXPECTED: * 'Next Race' label
        EXPECTED: * Status badge ('Going Down', 'At the Post', 'Going Behind', 'Off', 'Awaiting Result')
        EXPECTED: Next Race status is NOT displayed for resulted event
        """
        pass

    def test_006_verify_cash_out_icon_displaying(self):
        """
        DESCRIPTION: Verify 'Cash Out' icon displaying
        EXPECTED: Coral: 'CASH OUT' icon is shown if at least one of it's events has cashoutAvail="Y" and on all higher levels cashoutAvail="Y"
        EXPECTED: Ladbrokes: 'CASH OUT' icon is NOT displayed anywhere on the grid
        """
        pass

    def test_007_verify_live_stream_coralwatch_ladbrokes_icon(self):
        """
        DESCRIPTION: Verify 'Live Stream' (Coral)/'Watch' (Ladbrokes) icon
        EXPECTED: * Stream icon is displayed (if available) next to Cash Out icon (if available)
        EXPECTED: * Stream icon is shown for event type where at least 1 event has stream available on event level ("mediaTypeCodes" parameter is available in SS response)
        EXPECTED: * Stream icon is for informational purpose only
        """
        pass

    def test_008_verify_row_of_events_displaying(self):
        """
        DESCRIPTION: Verify row of events displaying
        EXPECTED: * Event off times are displayed horizontally across the page
        EXPECTED: * Coral: Signposting icons are displayed next to event off time (if available)
        EXPECTED: Ladbrokes: Signposting icons are NOT displayed next to event off time
        EXPECTED: * CORAL ONLY (BMA-46618) Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        EXPECTED: * **Ladbrokes**:  ALL events off times are displayed in bold no matter if it is 'LP' or 'SP' prices
        EXPECTED: * **Ladbrokes**: Race Statuses displayed for started or resulted events:
        EXPECTED: - Race Off - event has 'isOff=Yes'
        EXPECTED: - Live - event has 'isOff=Yes'and at least one of markets has 'betInRunning=true'
        EXPECTED: - Resulted - event has 'isResulted=true' + 'isFinished=true'
        """
        pass

    def test_009_verify_event_off_times(self):
        """
        DESCRIPTION: Verify event off times
        EXPECTED: Event off times corresponds to the race local time from the '**name'** attribute from the Site Server
        """
        pass

    def test_010_verify_scrolling_between_event_off_times(self):
        """
        DESCRIPTION: Verify scrolling between event off times
        EXPECTED: On **Mobile/Tablet** ability to scroll left and right is available via swiping
        EXPECTED: On **Desktop** (width starting from 970 px) race meeting with too many event off times to be shown in one line has arrows which appear on hover to scroll horizontally.
        EXPECTED: Events off times are scrolled one by one after click arrows
        """
        pass

    def test_011_tap_on_event_off_time(self):
        """
        DESCRIPTION: Tap on event off time
        EXPECTED: Corresponding Event details page is opened
        """
        pass

    def test_012_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Horse Races Landing page is opened
        """
        pass

    def test_013_repeat_steps_1_11_for_any_international_race_grid(self):
        """
        DESCRIPTION: Repeat steps #1-11 for any International race grid
        EXPECTED: Results are the same
        """
        pass

    def test_014_repeat_steps_1_11_for_virtual_race_grid(self):
        """
        DESCRIPTION: Repeat steps #1-11 for 'VIRTUAL' race grid
        EXPECTED: Results are the same
        """
        pass

    def test_015_repeat_steps_1_11_for_ladbrokescoral_legends_race_grid(self):
        """
        DESCRIPTION: Repeat steps #1-11 for 'Ladbrokes/Coral Legends' race grid
        EXPECTED: 
        """
        pass
