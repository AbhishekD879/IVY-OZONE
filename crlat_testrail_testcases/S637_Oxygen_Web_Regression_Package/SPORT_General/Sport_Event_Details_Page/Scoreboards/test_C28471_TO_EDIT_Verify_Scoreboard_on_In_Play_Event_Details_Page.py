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
class Test_C28471_TO_EDIT_Verify_Scoreboard_on_In_Play_Event_Details_Page(Common):
    """
    TR_ID: C28471
    NAME: TO EDIT Verify Scoreboard on In-Play Event Details Page
    DESCRIPTION: This test case verifies Scoreboard presence on In-Play Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. To retrieve Event's specific data use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. Event is **In-Play **(live) when:
    PRECONDITIONS: **rawlsOffCode = "Y"** OR** (rawlsOffCode="-" **AND  **isStarted==true)**
    PRECONDITIONS: **URLs:**
    PRECONDITIONS: *   CI-TEST2: scoreboards-tst2.coral.co.uk/getWidget/0/XXXX/scoreboard
    PRECONDITIONS: *   CI-STAGE: scoreboards-stg2.coral.co.uk/getWidget/0/XXXX/scoreboard
    PRECONDITIONS: *   CI-PROD: scoreboards.coral.co.uk/getWidget/0/XXXX/scoreboard
    PRECONDITIONS: XXXX - event ID.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Landing page
        EXPECTED: <Sports> Landing Page is opened
        """
        pass

    def test_003_open_in_play_event_details_page(self):
        """
        DESCRIPTION: Open In-Play Event Details page
        EXPECTED: <Sports> Event Details page is opened
        """
        pass

    def test_004_verify_in_play_scoreboard(self):
        """
        DESCRIPTION: Verify In-Play Scoreboard
        EXPECTED: *   The GrandParade scoreboard placeholder is present at the top of <Sport> In-Play Event Details Page
        EXPECTED: *   The scoreboard is ONLY shown if the event is In-Play (in order to determine live event use data in Preconditions)
        EXPECTED: Scoreboard is not shown in case of:
        EXPECTED: *   The event is not yet In-Play
        EXPECTED: *   The relevant services cannot be contacted (tech issues). Can be verified via URL's from Preconditions
        """
        pass
