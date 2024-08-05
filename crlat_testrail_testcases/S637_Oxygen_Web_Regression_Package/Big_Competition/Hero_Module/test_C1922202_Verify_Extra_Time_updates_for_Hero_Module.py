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
class Test_C1922202_Verify_Extra_Time_updates_for_Hero_Module(Common):
    """
    TR_ID: C1922202
    NAME: Verify Extra Time updates for Hero Module
    DESCRIPTION: This test case verifies Extra Time updates for Hero Module
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * Event should be In Play and have Live Scores available
    PRECONDITIONS: * How to generate Live Scores: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: * First/Second time should be finished for the particular event
    PRECONDITIONS: * In order to have extra time scores for both team should be equal (e.g. 1-1;2-2)
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

    def test_004_set_extra_time_first_half_option_in_amelco_inplay_tool(self):
        """
        DESCRIPTION: Set 'Extra Time first half' option in Amelco Inplay tool
        EXPECTED: 
        """
        pass

    def test_005_refresh_the_page_and_verify_event_in_extra_time(self):
        """
        DESCRIPTION: Refresh the page and verify event in Extra time
        EXPECTED: * Primary market is subsituted to market with tempate 'Extra Time Result' automatically
        EXPECTED: * Market name is changed to 'Extra Time Result' automatically
        EXPECTED: * 'ET' label apprears above market name and '+n markets' link
        EXPECTED: * Live Score for Home and Away team remains the same
        """
        pass

    def test_006_verify_match_time_in_extra_time_period(self):
        """
        DESCRIPTION: Verify Match Time in Extra Time period
        EXPECTED: * Match Time is reset to 0:00 when Extra Time period is set
        """
        pass

    def test_007_update_live_score_for_home_team(self):
        """
        DESCRIPTION: Update Live Score for Home team
        EXPECTED: * Live Score for Home team is changed automatically
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.CURRENT.value** where **role_code=HOME**
        """
        pass

    def test_008_update_live_score_for_away_team(self):
        """
        DESCRIPTION: Update Live Score for Away team
        EXPECTED: * Live Score for Away team is changed automatically
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.CURRENT.value** where **role_code=AWAY**
        """
        pass

    def test_009_set_extra_time_half_time_option_in_amelco_inplay_tool(self):
        """
        DESCRIPTION: Set 'Extra Time half time' option in Amelco Inplay tool
        EXPECTED: 
        """
        pass

    def test_010_verify_match_time_in_extra_time_half_time_period(self):
        """
        DESCRIPTION: Verify Match Time in Extra Time half time period
        EXPECTED: * 'HT' label is shown instead of Match Time
        EXPECTED: * Half Time is present when **[i].initClock.state=R** on **periodcode="EXTRA_TIME_HALF_TIME"** in WS response
        EXPECTED: where
        EXPECTED: i - the number of events returned for type
        """
        pass

    def test_011_set_extra_time_second_half_option_in_amelco_inplay_tool(self):
        """
        DESCRIPTION: Set 'Extra Time second half' option in Amelco Inplay tool
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_7_8(self):
        """
        DESCRIPTION: Repeat steps #7-8
        EXPECTED: 
        """
        pass
