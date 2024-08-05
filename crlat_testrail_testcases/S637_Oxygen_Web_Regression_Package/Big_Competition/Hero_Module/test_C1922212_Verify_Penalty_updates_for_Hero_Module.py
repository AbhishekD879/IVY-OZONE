import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1922212_Verify_Penalty_updates_for_Hero_Module(Common):
    """
    TR_ID: C1922212
    NAME: Verify Penalty updates for Hero Module
    DESCRIPTION: This test case verifies Penalty updates for Hero Module
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * Event should be In Play and have Live Scores available
    PRECONDITIONS: * How to generate Live Scores: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: * Extra Time First half/ Extra Time Second half should be finished for the particular event
    PRECONDITIONS: * In order to have penalties scores for both team should be equal after Extra Time First half/ Extra Time Second half (e.g. 1-1;2-2)
    PRECONDITIONS: * In order to check live updates open Dev Tools -> Network -> WS -> select request to InPlay MS 'wss://{domain}/websocket/?EIO=3&transport=websocket' -> Frames
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

    def test_004_set_penalties_option_in_amelco_inplay_tool(self):
        """
        DESCRIPTION: Set 'Penalties' option in Amelco Inplay tool
        EXPECTED: 
        """
        pass

    def test_005_verify_match_time_in_penalty_period(self):
        """
        DESCRIPTION: Verify Match Time in Penalty period
        EXPECTED: * 'PENS' label is displayed when **'state=R'** is received on **'period_code=PENALTIES'** in **'type=CLOCK'** update in WS
        EXPECTED: * 'PENS' label appears automatically instead of Match Time between Scores
        """
        pass

    def test_006_refresh_the_page_and_verify_event_in_penalty_period(self):
        """
        DESCRIPTION: Refresh the page and verify event in Penalty period
        EXPECTED: * 'AET' label appears above market name and '+n markets' link
        EXPECTED: * Live Scores for Home and Away team from Extra Time period remain the same
        EXPECTED: * Penalty Live Scores appear instead of Live Scores for Home and Away team from Extra Time period
        EXPECTED: * Live Scores appear bellow Penalty Live Scores for Home and Away team from Extra Time period
        """
        pass

    def test_007_verify_penalty_live_scores_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify Penalty Live Scores correctness for each team
        EXPECTED: * Penalty Live Score correspond to **[i].comments.teams.home.penaltyScore** attribute for Home team
        EXPECTED: * Penalty Live Score correspond to **[i].comments.teams.away.penaltyScore** attribute for Away team
        EXPECTED: from GET
        EXPECTED: "IN_PLAY_SPORT_TYPE::{categoryID}::LIVE_EVENT::{typeID}" response for particular event
        EXPECTED: where
        EXPECTED: i - the number of events received for particular type
        EXPECTED: categoryID - Openbet category ID
        EXPECTED: typeID - Openbet type ID
        """
        pass

    def test_008_update_penalty_live_score_for_home_team(self):
        """
        DESCRIPTION: Update Penalty Live Score for Home team
        EXPECTED: * Penalty Live Score for Home team is changed automatically
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.CURRENT.value** where **role_code=HOME**
        """
        pass

    def test_009_update_penalty_live_score_for_away_team(self):
        """
        DESCRIPTION: Update Penalty Live Score for Away team
        EXPECTED: * Penalty Live Score for Away team is changed automatically
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.CURRENT.value** where **role_code=AWAY**
        """
        pass
