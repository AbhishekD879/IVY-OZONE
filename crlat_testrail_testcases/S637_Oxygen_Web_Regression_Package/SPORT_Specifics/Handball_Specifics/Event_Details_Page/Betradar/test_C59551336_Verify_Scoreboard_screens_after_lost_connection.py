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
class Test_C59551336_Verify_Scoreboard_screens_after_lost_connection(Common):
    """
    TR_ID: C59551336
    NAME: Verify Scoreboard screens after lost connection
    DESCRIPTION: Test Case verifies Scoreboard screens recovery after lost connection and corresponding data updating
    PRECONDITIONS: 1: Navigate to Sports Menu(Handball)/From A-Z all Sports->Handball
    PRECONDITIONS: 2:Handball event(s) are subscribed to Bet radar Scoreboards
    PRECONDITIONS: Event in Prematch state
    PRECONDITIONS: Event in InPlay state
    PRECONDITIONS: 3:Betradar scoreboard configuration in CMS is Enabled.
    PRECONDITIONS: TBD?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    PRECONDITIONS: To trigger lost connection/reconnect:
    PRECONDITIONS: - turn internet off/on
    PRECONDITIONS: - lock/unlock the phone for >5 min
    PRECONDITIONS: - turn flight mode off/on
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_prematch_handball__edp_from_precondition(self):
        """
        DESCRIPTION: Navigate to Prematch Handball  EDP from Precondition
        EXPECTED: It should navigated to Fustal EDP.
        """
        pass

    def test_002_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_003_verify_whether_prematch_data_is_displaying_properly(self):
        """
        DESCRIPTION: Verify whether Prematch data is displaying properly
        EXPECTED: All data is displaying properly (data is available in Local Storage scoreBoards[env, e.g. stage]prematch[EventID]
        EXPECTED: Start Time of event
        EXPECTED: Date
        EXPECTED: Name of Participants Team A vs Team B. (With the Home team first)
        """
        pass

    def test_004_navigate_to_inplay_handball__edp_from_precondition(self):
        """
        DESCRIPTION: Navigate to Inplay Handball  EDP from Precondition
        EXPECTED: It should navigated to Fustal EDP.
        """
        pass

    def test_005_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_006_verify_whether_inplay_data_is_displaying_properly(self):
        """
        DESCRIPTION: Verify whether Inplay data is displaying properly
        EXPECTED: All data is up to date, all Scoreboard events are displayed properly
        """
        pass
