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
class Test_C1493962_Verify_Live_Scores_updates_for_Hero_Module(Common):
    """
    TR_ID: C1493962
    NAME: Verify Live Scores updates for Hero Module
    DESCRIPTION: This test case verifies Live Scores updates for Hero Module
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * To check data correctness and update from In Play and Live Serve MS open Dev Tools -> Network tab -> WS -> select '?EIO=3&transport=websocket' request
    PRECONDITIONS: **NOTE** Currently Live Scores are implemented for Football ONLY
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_hero_module_next_events_module_for_live_events___event_with_live_score_available(self):
        """
        DESCRIPTION: Go to Hero Module (Next Events Module for Live Events) -> event with Live Score available
        EXPECTED: Event with Live Score is present within Hero Module
        """
        pass

    def test_004_verify_live_scores_correctness_for_home_team(self):
        """
        DESCRIPTION: Verify Live Scores correctness for home team
        EXPECTED: Live Scores for Home team corresponds to **[i].comments.teams.home.score** attribute from GET
        EXPECTED: "IN_PLAY_SPORT_TYPE::{categoryID}::LIVE_EVENT::{typeID}" response for particular event
        EXPECTED: where
        EXPECTED: i - the number of events received for particular type
        EXPECTED: categoryID - Openbet category ID
        EXPECTED: typeID - Openbet type ID
        """
        pass

    def test_005_verify_live_scores_correctness_for_away_team(self):
        """
        DESCRIPTION: Verify Live Scores correctness for away team
        EXPECTED: Live Scores for Away team corresponds to **[i].comments.teams.away.score** attribute from GET
        EXPECTED: "IN_PLAY_SPORT_TYPE::{categoryID}::LIVE_EVENT::{typeID}" response for particular event
        EXPECTED: where
        EXPECTED: i - the number of events received for particular type
        EXPECTED: categoryID - Openbet category ID
        EXPECTED: typeID - Openbet type ID
        """
        pass

    def test_006_update_live_score_for_home_team(self):
        """
        DESCRIPTION: Update Live Score for home team
        EXPECTED: * Live Score for home team is changed immediately
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.ALL.value** where **role_code=HOME**
        """
        pass

    def test_007_update_live_score_for_away_team(self):
        """
        DESCRIPTION: Update Live Score for away team
        EXPECTED: * Live Score for away team is changed immediately
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.ALL.value** where **role_code=AWAY**
        """
        pass

    def test_008_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown between team flags and abbriviations
        """
        pass
