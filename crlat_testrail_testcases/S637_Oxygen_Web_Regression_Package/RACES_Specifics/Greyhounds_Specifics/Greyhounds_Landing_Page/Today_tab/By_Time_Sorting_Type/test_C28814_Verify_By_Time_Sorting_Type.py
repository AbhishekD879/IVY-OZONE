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
class Test_C28814_Verify_By_Time_Sorting_Type(Common):
    """
    TR_ID: C28814
    NAME: Verify 'By Time' Sorting Type
    DESCRIPTION: This test case verifies 'Today' tab when 'BY TIME' sorting type is selected
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
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    keep_browser_open = True

    def test_001_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Select 'BY TIME' sorting type
        EXPECTED: 'BY TIME' sorting type is selected
        """
        pass

    def test_002_check_race_events_sections(self):
        """
        DESCRIPTION: Check Race Events sections
        EXPECTED: * Race Event section 'Events' is displayed and expanded by default
        EXPECTED: **FOR Mobile** 'NEXT RACES' section is displayed and expanded by default
        EXPECTED: **FOR Desktop** 'Next races' widget is displayed and expanded by default
        """
        pass

    def test_003_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: List of events for today's date is shown
        """
        pass

    def test_004_check_event_section(self):
        """
        DESCRIPTION: Check event section
        EXPECTED: * Each event is in a separate block
        EXPECTED: * Event name corresponds to the **'name' **attribute from the Featured WS featured_structure_changed message (it includes race local time and event name)
        EXPECTED: * 'Go To Race Card' link is displayed on the right side
        EXPECTED: of the event block
        """
        pass

    def test_005_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: * Stream icon is displayed under the event name
        EXPECTED: * Stream icon is displayed for event where the stream is available
        """
        pass
