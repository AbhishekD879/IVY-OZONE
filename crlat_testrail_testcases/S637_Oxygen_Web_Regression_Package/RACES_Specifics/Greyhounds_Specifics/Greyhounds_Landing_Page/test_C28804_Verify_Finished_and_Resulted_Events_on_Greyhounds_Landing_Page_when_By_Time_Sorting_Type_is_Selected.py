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
class Test_C28804_Verify_Finished_and_Resulted_Events_on_Greyhounds_Landing_Page_when_By_Time_Sorting_Type_is_Selected(Common):
    """
    TR_ID: C28804
    NAME: Verify Finished and Resulted Events on Greyhounds Landing Page when 'By Time' Sorting Type is Selected
    DESCRIPTION: This test case verifies how finished and resulted events will be shown on <Race> landing page when 'By Time' sorting type is selected (ONLY CORAL brand)
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
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: **isFinished = 'true'** on event level - to check whether event is finished
    PRECONDITIONS: **isResulted='true'** on event level - to check whether event is resulted
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed  according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load the app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    PRECONDITIONS: Finished/Resulted events should be present
    """
    keep_browser_open = True

    def test_001_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Select **'BY TIME'** sorting type
        EXPECTED: 'BY TIME' sorting type is selected
        """
        pass

    def test_002_verify_resulted_event_events_with_attributeisresulted__true(self):
        """
        DESCRIPTION: Verify resulted event (events with attribute:** 'isResulted' = true**)
        EXPECTED: Event name is greyed and 'Resulted' icon is displayed in the center of the event
        EXPECTED: ![](index.php?/attachments/get/36765)
        """
        pass

    def test_003_tap_on_resulted_event(self):
        """
        DESCRIPTION: Tap on resulted event
        EXPECTED: Corresponding Event details page with settled race results is opened
        """
        pass

    def test_004_verify_finished_events_event_with_attributes_isfinishedtrue_and_isresultedtrue_in_the_list_of_events(self):
        """
        DESCRIPTION: Verify finished events (event with attributes **isFinished='true'** and **isResulted='true'**) in the list of events
        EXPECTED: Event name is greyed and 'Resulted' icon is displayed in the center of the event
        EXPECTED: ![](index.php?/attachments/get/36766)
        """
        pass

    def test_005_tap_event_off_time_for_verified_event(self):
        """
        DESCRIPTION: Tap event off time for verified event
        EXPECTED: Corresponding Event details page with settled race results is opened
        """
        pass
