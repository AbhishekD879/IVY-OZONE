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
class Test_C59551278_Verify_scoreboard_screens_after_lost_connection(Common):
    """
    TR_ID: C59551278
    NAME: Verify scoreboard screens after lost connection
    DESCRIPTION: Test case verifies scoreboard screens recovery after lost connection and corresponding data updating
    PRECONDITIONS: 1. Ice Hockey event(s) should subscribe to Betradar Scoreboards
    PRECONDITIONS: 2. Event should be in InPlay state
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    PRECONDITIONS: To trigger lost connection/reconnect:
    PRECONDITIONS: - turn internet off/on
    PRECONDITIONS: - lock/unlock the phone for >5 min
    PRECONDITIONS: - turn flight mode off/on
    """
    keep_browser_open = True

    def test_001_navigate_to_in_play_ice_hockey_edp_froma_z_menu_ice_hockey___in_playorhome___ice_hockey___in_play(self):
        """
        DESCRIPTION: Navigate to In play Ice Hockey EDP from
        DESCRIPTION: A-Z menu Ice Hockey - in play
        DESCRIPTION: Or
        DESCRIPTION: Home - Ice Hockey - in play
        EXPECTED: Event details page should display
        """
        pass

    def test_002_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_003_verify_whether_inplay_data_is_displaying_properly(self):
        """
        DESCRIPTION: Verify whether Inplay data is displaying properly
        EXPECTED: All data should be up to date, all Scoreboard events should display properly
        """
        pass
