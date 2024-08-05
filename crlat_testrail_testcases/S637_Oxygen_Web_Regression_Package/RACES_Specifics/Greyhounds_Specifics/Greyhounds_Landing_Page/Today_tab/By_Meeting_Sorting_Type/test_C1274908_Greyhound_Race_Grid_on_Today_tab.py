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
class Test_C1274908_Greyhound_Race_Grid_on_Today_tab(Common):
    """
    TR_ID: C1274908
    NAME: Greyhound Race Grid on Today tab
    DESCRIPTION: This test case verifies the Race Grid on Greyhounds landing page
    DESCRIPTION: New Design (LADBROKES Desktop) - https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
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
    PRECONDITIONS: **New changes:
    PRECONDITIONS: Added "simpleFilter=class.hasOpenEvent" query to /Class request to receive info only about classes with available events.
    PRECONDITIONS: Removed request /EventToOutcomeForClass/201 on Ladbrokes (Specials Events).
    PRECONDITIONS: Removed simpleFilter=event.categoryId:intersects:21 from request /EventToOutcomeForClass (horse racing category id: 21, greyhound category id: 19)
    PRECONDITIONS: Added to /EventToOutcomeForClass filter &limitRecords=outcome:1, &limitRecords=market:1
    PRECONDITIONS: Date range should be: 1 day (today or tomorrow).
    PRECONDITIONS: Only one WS connection is between switching By Meeting/By time tab (Coral greyhounds).
    PRECONDITIONS: Parameter **startTime** defines event start time (note, this is not a race local time)
    PRECONDITIONS: Load the app
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds landing page
        EXPECTED: **FOR CORAL:**
        EXPECTED: - 'TODAY' tab is opened and the race grid is shown with 'By Meeting' sorting switched on by default
        EXPECTED: - 'TODAY' tab contains 2 sub-tabs - 'BY MEETING' and 'BY TIME'
        EXPECTED: **FOR LADBROKES:**
        EXPECTED: - 'TODAY' tab is opened and the race grid is shown with 'By Meeting' sorting switched on by default
        EXPECTED: - NO sub-tabs available
        """
        pass

    def test_002_verify_race_grid_sections(self):
        """
        DESCRIPTION: Verify race grid sections
        EXPECTED: The following sections are displayed and expanded by default:
        EXPECTED: **FOR CORAL (Mobile/Desktop):**
        EXPECTED: - UK&IRE
        EXPECTED: - VIRTUAL
        EXPECTED: - NEXT RACES
        EXPECTED: **FOR LADBROKES (Mobile/Desktop):**
        EXPECTED: - UK/IRELAND RACES
        EXPECTED: - VIRTUAL RACES
        """
        pass

    def test_003_collapse_and_expand_the_grid_sections_by_tapping_on_the_headers(self):
        """
        DESCRIPTION: Collapse and expand the grid sections by tapping on the headers
        EXPECTED: It is possible to collapse/expand accordions by tapping on the headers
        EXPECTED: **FOR MOBILE (Coral/Ladbrokes) and DESKTOP (Ladbrokes):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: No arrows displayed
        EXPECTED: **FOR DESKTOP (Coral):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: the upward arrow is displayed on the right side
        """
        pass

    def test_004_verify_race_grid_content(self):
        """
        DESCRIPTION: Verify Race Grid content
        EXPECTED: All events from SS response with start time ( **startTime** attribute) corresponding to today's day  are displayed within the corresponding type (race meeting) section
        """
        pass

    def test_005_verify_filtered_out_events(self):
        """
        DESCRIPTION: Verify filtered out events
        EXPECTED: Events that passed "Suspension Time" are not received and shown (**suspendAtTime** attribute)
        """
        pass
