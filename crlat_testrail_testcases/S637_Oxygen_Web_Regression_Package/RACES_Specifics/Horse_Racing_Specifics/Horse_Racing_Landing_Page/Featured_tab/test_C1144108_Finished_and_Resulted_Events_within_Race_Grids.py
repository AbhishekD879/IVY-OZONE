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
class Test_C1144108_Finished_and_Resulted_Events_within_Race_Grids(Common):
    """
    TR_ID: C1144108
    NAME: Finished and Resulted Events within Race Grids
    DESCRIPTION: This test case verifies how finished and resulted events will be shown within Race Grids
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
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing___featured_tab___uk__ire_race_grid(self):
        """
        DESCRIPTION: Navigate to Horse Racing -> Featured tab -> UK & IRE race grid
        EXPECTED: * Tab for first available day is opened by default
        EXPECTED: * List of Race meeting sections for first day tab is displayed
        """
        pass

    def test_002_verify_event_off_time_for_resulted_event_events_with_attribute_isresulted__true_(self):
        """
        DESCRIPTION: Verify event off time for resulted event (events with attribute: **'isResulted' = true** )
        EXPECTED: Coral: Event off time is greyed and 'Result' icon is displayed near.
        EXPECTED: Ladbrokes: Event off time is NOT greyed and 'Result' icon is displayed under.
        """
        pass

    def test_003_tap_event_off_time_for_verified_event(self):
        """
        DESCRIPTION: Tap event off time for verified event
        EXPECTED: Page redirects to Results tab with current event results.
        EXPECTED: Odds column is populated by odds for each resulted line/winners.
        """
        pass

    def test_004_go_to_current_day_tab(self):
        """
        DESCRIPTION: Go to current day tab
        EXPECTED: 
        """
        pass

    def test_005_verify_event_off_time_for_finished_events_event_with_attributes_isfinishedtrue_andisresulted__true_(self):
        """
        DESCRIPTION: Verify event off time for finished events (event with attributes **isFinished='true'** and **'isResulted' = true** )
        EXPECTED: Coral: Event off time is greyed and 'Result' icon is displayed near.
        EXPECTED: Ladbrokes: Event off time is NOT greyed and 'Result' icon is displayed under.
        """
        pass

    def test_006_tap_event_off_time_for_verified_event(self):
        """
        DESCRIPTION: Tap event off time for verified event
        EXPECTED: Page redirect to Results tab with current event results.
        EXPECTED: Odds column is populated by odds for each resulted line/winners.
        """
        pass

    def test_007_repeat_steps_1_6_for_international_race_grid(self):
        """
        DESCRIPTION: Repeat steps #1-6 for 'International race grid
        EXPECTED: Results are the same
        """
        pass
