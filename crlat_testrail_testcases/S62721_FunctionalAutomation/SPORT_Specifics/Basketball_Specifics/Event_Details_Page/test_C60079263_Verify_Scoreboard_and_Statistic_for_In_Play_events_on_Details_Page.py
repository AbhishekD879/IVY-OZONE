import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60079263_Verify_Scoreboard_and_Statistic_for_In_Play_events_on_Details_Page(Common):
    """
    TR_ID: C60079263
    NAME: Verify Scoreboard and Statistic for In Play events on Details Page
    DESCRIPTION: This test case verifies Scoreboard for In Play Basketball events on Details Page
    PRECONDITIONS: 1) In order to have a Scoreboard Basketball event should be BIP and should have the next attributes in SS:
    PRECONDITIONS: *    ( **isStarted="true"** AND **rawlsOffCode="-"**) OR **rawlsOffCode = "Y"** on event level
    PRECONDITIONS: *    **isMarketBetInRun="true"** on market level
    PRECONDITIONS: 2) Use the next link to get the response from SS:
    PRECONDITIONS: https://{domain}/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: * XXX - event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: * STG domain: ss-aka-ori-stg2.coral.co.uk
    PRECONDITIONS: * PROD domain: ss-aka-ori.coral.co.uk
    PRECONDITIONS: 3) Scoreboard should be allowed for Basketball in CMS -> Menus -> Sport Categories -> Basketball sport -> 'Show Scoreboard' checkbox should be selected
    PRECONDITIONS: 4) Scoreboard should be allowed for all Sports in CMS -> System-Configuration -> Scoreboard section -> showScoreboard = Yes
    PRECONDITIONS: 5) In order to check Scoreboard correctness use the links:
    PRECONDITIONS: * STG: https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/page/ladbrokescoral/basketballscorecentre?eventId=XXXXXXX
    PRECONDITIONS: * PROD: https://ladbrokescoral.betstream.betgenius.com/betstream-view/page/coral/basketballscorecentre?eventId=XXXXXXX
    PRECONDITIONS: where XXXXXXX - event ID
    PRECONDITIONS: 6) List of all available events with Scoreboard:
    PRECONDITIONS: * STG: https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/getMappedFixtures/v1/product/ladbrokescoralbasketballscorecentre/sport/basketball
    PRECONDITIONS: * PROD: https://ladbrokescoral.betstream.betgenius.com/betstream-view/getMappedFixtures/v1/product/ladbrokescoralbasketballscorecentre/sport/basketball
    PRECONDITIONS: 7) To verify data correctness use Dev Tools-> Network -> XHR -> scoreboard request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_basketball_landing_page_select_in_play_tab(self):
        """
        DESCRIPTION: Go to Basketball landing page, select 'In Play' tab
        EXPECTED: * 'In Play' page is loaded
        EXPECTED: * 'Live Now' sorting filter is opened by default
        """
        pass

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details Page
        EXPECTED: * Event Details page is opened
        EXPECTED: * Request to Betgenius is sent with correct event ID (see preconditions)
        """
        pass

    def test_004_verify_scoreboard_and_statistic(self):
        """
        DESCRIPTION: Verify Scoreboard and Statistic
        EXPECTED: * Scoreboard is located between 'Basketball' header and Market content
        EXPECTED: * Event name, date and 'Live' label are NOT displayed
        EXPECTED: * All data for Scoreboard and Statistic tabs is taken from Betgenius response (see preconditions)
        """
        pass

    def test_005_verify_scoreboard_and_statistic_when_there_is_error_during_loadingeg_enter_invalid_event_id_to_retrieve_scoreboard(self):
        """
        DESCRIPTION: Verify Scoreboard and Statistic when there is error during loading
        DESCRIPTION: (e.g. enter invalid event ID to retrieve Scoreboard)
        EXPECTED: * App behaves correctly, it's not crashed
        EXPECTED: * Scoreboard is NOT displayed
        EXPECTED: * Event name, date and 'Live' label are displayed instead
        """
        pass

    def test_006_go_to_event_details_page_of_pre_match_event(self):
        """
        DESCRIPTION: Go to Event Details page of Pre Match event
        EXPECTED: * Scoreboard request is NOT sent
        EXPECTED: * Scoreboard is NOT displayed for Pre Match event
        """
        pass

    def test_007_go_to_event_details_page_of_in_play_event_that_is_not_started_yet_eg_select_event_from_upcoming_sorting_filter(self):
        """
        DESCRIPTION: Go to Event Details page of In Play event that is not started yet (e.g. select event from 'Upcoming' sorting filter)
        EXPECTED: * Scoreboard request is NOT sent
        EXPECTED: * Scoreboard is NOT displayed for In Play event that is not started yet
        """
        pass
