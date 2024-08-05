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
class Test_C160741_Verify_Show_More_option_on_By_Time_filter_tab(Common):
    """
    TR_ID: C160741
    NAME: Verify 'Show More' option on 'By Time' filter tab
    DESCRIPTION: This test case verifies 'Show More' option on 'By Time' filter tab
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

    def test_002_verify_amount_of_events_which_are_displayed_in_the_events_section_on_the_page(self):
        """
        DESCRIPTION: Verify amount of events which are displayed in the 'Events' section on the page
        EXPECTED: - Maximum of 10 events are displayed on the first view
        EXPECTED: - 'Show More' button is displayed in case when more than 10 events are available
        """
        pass

    def test_003_verify_show_more_button_when_10_events_are_displayed_in_the_events_section_on_the_page(self):
        """
        DESCRIPTION: Verify 'Show More' button when 10 events are displayed in the 'Events' section on the page
        EXPECTED: 'Show More' button should not be displayed when 10 events are displayed
        """
        pass

    def test_004_verify_show_more_button_when_more_than_10_events_are_available_in_the_events_section_on_the_page(self):
        """
        DESCRIPTION: Verify 'Show More' button when more than 10 events are available in the 'Events' section on the page
        EXPECTED: 'Show More' button should be displayed when more than 10 events are available
        """
        pass

    def test_005_tap_on_show_more_button(self):
        """
        DESCRIPTION: Tap on 'Show More' button
        EXPECTED: - The further events are displayed (maximum next 10 events are shown)
        EXPECTED: - 'Show More' button should disappears if events are displayed
        """
        pass
