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
class Test_C28803_Verify_Finished_and_Resulted_Events_on_Greyhounds_Landing_Page(Common):
    """
    TR_ID: C28803
    NAME: Verify Finished and Resulted Events on Greyhounds Landing Page
    DESCRIPTION: This test case verifies how finished and resulted events will be shown on Greyhounds landing page
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
    PRECONDITIONS: **isFinished = 'true'** on event level - to check whether the event is finished
    PRECONDITIONS: **isResulted='true'** on event level - to check whether the event is resulted
    PRECONDITIONS: Load the app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default
    PRECONDITIONS: Finished/Resulted events should be present
    """
    keep_browser_open = True

    def test_001_verify_event_off_time_for_resulted_event_events_with_attributeisresulted__true(self):
        """
        DESCRIPTION: Verify event off time for resulted event (events with attribute:** 'isResulted' = true**)
        EXPECTED: **FOR CORAL**
        EXPECTED: Event off time is greyed and red 'Resulted' icon is displayed under the time
        EXPECTED: ![](index.php?/attachments/get/36688)
        EXPECTED: **FOR LADBROKES**
        EXPECTED: Event off time stayed bold and black 'Resulted' icon with text 'RESULT' is displayed under the time
        EXPECTED: ![](index.php?/attachments/get/36688)
        """
        pass

    def test_002_tap_event_off_time_for_the_resulted_event(self):
        """
        DESCRIPTION: Tap event off time for the resulted event
        EXPECTED: Corresponding Event details page with settled race results is opened
        """
        pass

    def test_003_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Greyhound Landing page is opened
        EXPECTED: 'TODAY' tab is opened by default
        """
        pass

    def test_004_verify_event_off_time_for_finished_events_event_with_attributes_isfinishedtrue_andisresulted__true(self):
        """
        DESCRIPTION: Verify event off time for finished events (event with attributes** isFinished='true'** and **'isResulted' = true**)
        EXPECTED: **FOR CORAL**
        EXPECTED: Event off time is greyed and red 'Resulted' icon is displayed under the time
        EXPECTED: ![](index.php?/attachments/get/36688)
        EXPECTED: **FOR LADBROKES**
        EXPECTED: Event off time stayed bold and black 'Resulted' icon with text 'RESULT' is displayed under the time
        EXPECTED: ![](index.php?/attachments/get/36688)
        """
        pass

    def test_005_tap_event_off_time__for_the_resulted_event(self):
        """
        DESCRIPTION: Tap event off time  for the resulted event
        EXPECTED: Corresponding Event details page with settled race results is opened
        """
        pass
