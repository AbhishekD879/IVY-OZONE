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
class Test_C1107969_Race_Grid(Common):
    """
    TR_ID: C1107969
    NAME: Race Grid
    DESCRIPTION: This test case verifies Race grid on Featured tab for Horse Racing
    PRECONDITIONS: * App is loaded
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
    PRECONDITIONS: The display order of 'UK & IRE', 'International' etc section can be set here:
    PRECONDITIONS: CMS/Sports Pages/Sport Categories/Horse Racing
    """
    keep_browser_open = True

    def test_001_navigate_to_hr___featured_tab(self):
        """
        DESCRIPTION: Navigate to HR -> Featured tab
        EXPECTED: Race Grid accordions (expanded by default) are displayed in the following order (CMS configurable):
        EXPECTED: * UK & IRE (events with typeFlagCodes 'UK' or 'IE')
        EXPECTED: * Ladbrokes/Coral Legends (quantum leap events from new 'Ladbrokes Legend' class with 'Virtual Racing' flag set)
        EXPECTED: * International events divided into corresponding Country accordions (events with typeFlagCodes 'US,ZA,AE,CL,IN,AU,FR,INT')
        EXPECTED: * Virtual (events with typeFlagCodes 'VR')
        EXPECTED: In case there are no events with these flags -  corresponding accordion is NOT displayed
        EXPECTED: Events without attribute 'typeFlagCodes': UK, IRE,S,ZA,AE,CL,IN,AU,FR, INT or VR are not displayed
        EXPECTED: It is possible to collapse/expand accordions by tapping section header
        EXPECTED: On **Mobile, Tablet**:
        EXPECTED: - downward facing chevron on the right indicates collapsed state of accordion
        EXPECTED: **Desktop** (screen width starting from 970 px ) race grid accordion has
        EXPECTED: - downward facing chevron on the right indicates collapsed state of accordion
        EXPECTED: - upward facing chevron on the right indicates expanded state of accordion
        """
        pass

    def test_002_verify_race_grid_accordions_content(self):
        """
        DESCRIPTION: Verify Race Grid accordions content
        EXPECTED: * Day tabs
        EXPECTED: * List of Race meeting sections for first day tab
        """
        pass

    def test_003_verify_day_tabs(self):
        """
        DESCRIPTION: Verify day tabs
        EXPECTED: * Day tab name is day of the week
        EXPECTED: * when up to 3 days tabs available complete days name are displayed (ex. WEDNESDAY, THURSDAY)
        EXPECTED: * ***Coral***: when more than 3 days tabs available abbreviations for the days are displayed (ex. WED, THU, FRI..)
        EXPECTED: * ***Ladbrokes***: when more than 3 tabs - complete days name (according to https://app.zeplin.io/project/5c35cf920695502973380b86/screen/5c3cb9a10695502973712579)
        EXPECTED: * Day tabs are sorted chronologically
        EXPECTED: * If there are no events for day tab, tab is not shown
        EXPECTED: * First day tab (corresponding to the earliest day) is opened by default
        """
        pass

    def test_004_verify_amount_of_tabs(self):
        """
        DESCRIPTION: Verify amount of tabs
        EXPECTED: * UK & IRE and International: up to 6 next day tabs are present if available
        EXPECTED: * Virtual: up to 2 day tabs corresponding to Today and Tomorrow days are present if available
        """
        pass

    def test_005_verify_content_for_first_day_tab(self):
        """
        DESCRIPTION: Verify content for first day tab
        EXPECTED: * All events from SS response with start time (**startTime** attribute) corresponding to selected day tab are displayed within corresponding type (race meeting) section
        """
        pass

    def test_006_verify_filtered_out_events(self):
        """
        DESCRIPTION: Verify filtered out events
        EXPECTED: * Antepost events are not received and are not shown (drilldownTagNames:"EVFLAG_AP)
        EXPECTED: * Events that passed "Suspension Time" are not received and shown ("suspendAtTime" attribute)
        """
        pass

    def test_007_click_successively_on_all_other_future_day_tabs_and_repeat_steps_5_6(self):
        """
        DESCRIPTION: Click successively on all other future day tabs and repeat steps #5-6
        EXPECTED: Result is the same
        """
        pass
