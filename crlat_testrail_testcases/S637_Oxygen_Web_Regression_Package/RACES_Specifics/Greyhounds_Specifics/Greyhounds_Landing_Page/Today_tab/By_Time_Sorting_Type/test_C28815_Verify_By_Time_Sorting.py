import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28815_Verify_By_Time_Sorting(Common):
    """
    TR_ID: C28815
    NAME: Verify 'By Time' Sorting
    DESCRIPTION: This test case verifies 'By Time' sorting of events
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
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    keep_browser_open = True

    def test_001_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Select 'By Time' sorting type
        EXPECTED: - 'By Time' sorting type is opened
        EXPECTED: - 'Events' section is visible
        EXPECTED: - 'Next Races' section is visible
        """
        pass

    def test_002_check_events_section(self):
        """
        DESCRIPTION: Check 'Events' section
        EXPECTED: Section header is entitled 'Events'
        EXPECTED: 'Events' section is expanded by default
        EXPECTED: It is possible to collapse/expand the 'Events' section
        """
        pass

    def test_003_check_next_races_section(self):
        """
        DESCRIPTION: Check 'Next races' section
        EXPECTED: Section header is entitled 'Next races'
        EXPECTED: **FOR Mobile** 'NEXT RACES' section is displayed and expanded by default
        EXPECTED: **FOR Desktop** 'Next Races' widget is displayed and expanded by default
        EXPECTED: It is possible to collapse/expand the 'Next races' sections
        """
        pass

    def test_004_verify_by_time_sorting(self):
        """
        DESCRIPTION: Verify 'By Time' sorting
        EXPECTED: Events are sorted in the following order:
        EXPECTED: 1)** **chronologically **by race** **local time** order in the first instance
        EXPECTED: 2) alphabetically by **name** in ascending order if event start times are the same
        """
        pass
