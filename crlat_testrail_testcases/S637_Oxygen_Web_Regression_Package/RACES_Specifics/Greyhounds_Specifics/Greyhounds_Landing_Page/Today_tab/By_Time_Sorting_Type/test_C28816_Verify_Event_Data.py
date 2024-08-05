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
class Test_C28816_Verify_Event_Data(Common):
    """
    TR_ID: C28816
    NAME: Verify Event Data
    DESCRIPTION: This test case verifies whether data about events is displayed correctly
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
        DESCRIPTION: Select 'BY TIME' sorting type
        EXPECTED: 'BY TIME' sorting type is opened
        EXPECTED: 'Events' section is visible
        """
        pass

    def test_002_verify_events_which_are_shown(self):
        """
        DESCRIPTION: Verify events which are shown
        EXPECTED: The same events which are shown on 'By Meeting' sorting type -> are also displayed on 'By Time' sorting type
        """
        pass

    def test_003_verify_event_name_and_local_time(self):
        """
        DESCRIPTION: Verify Event name and local time
        EXPECTED: *   Event name corresponds to the **'name' **attribute
        EXPECTED: *   Event name is hyperlinked
        EXPECTED: *   Event name is shown in 'HH:MM EventName' format
        EXPECTED: *   Events off times with LP prices are displayed in bold if **'priceTypeCodes="LP,"'** attribute is available for **'Win or Each way'** market only
        """
        pass

    def test_004_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: If event has stream available -> 'Stream' icon will be shown under the event name
        EXPECTED: ![](index.php?/attachments/get/36789)
        """
        pass

    def test_005_tap_event_name(self):
        """
        DESCRIPTION: Tap event name
        EXPECTED: Event landing page is opened
        """
        pass

    def test_006_verify_by_time_sorting_type_when_there_are_no_events_to_show(self):
        """
        DESCRIPTION: Verify 'By Time' sorting type when there are no events to show
        EXPECTED: * Events section is not displayed
        EXPECTED: * Message is visible 'No events found'
        """
        pass
