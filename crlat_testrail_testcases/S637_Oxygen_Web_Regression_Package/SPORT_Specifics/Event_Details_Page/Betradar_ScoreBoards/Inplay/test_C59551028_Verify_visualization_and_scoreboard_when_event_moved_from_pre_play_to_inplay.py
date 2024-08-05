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
class Test_C59551028_Verify_visualization_and_scoreboard_when_event_moved_from_pre_play_to_inplay(Common):
    """
    TR_ID: C59551028
    NAME: Verify visualization and scoreboard when event moved from pre-play to inplay
    DESCRIPTION: test case verifies visualization and scoreboard when event moved from pre-play to inplay
    PRECONDITIONS: 1. Prematch table tennis event is available
    PRECONDITIONS: 2. Prematch table tennis event is subscribed to betradar Scoreboard
    PRECONDITIONS: 3. Prematch table tennis event is about to be moved into Inplay state
    PRECONDITIONS: to trigger event move from pre play to inplay
    PRECONDITIONS: - change event time current time
    PRECONDITIONS: - set is off flag to yes in OB event level
    PRECONDITIONS: - check bet in play list check box in OB event level
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_table_tennis_events_landing_page_fromhome___table_tennis___matches(self):
        """
        DESCRIPTION: Navigate to table tennis events landing page from
        DESCRIPTION: Home - table tennis - matches
        EXPECTED: today tab should display with all the today's events
        """
        pass

    def test_002_move_any_pre_match_event_to_inplay_from_pre_conditions(self):
        """
        DESCRIPTION: move any pre match event to inplay from pre conditions
        EXPECTED: Event should display under live now tab with scores and should not display under to days tab.
        """
        pass

    def test_003_click_on_event_and_verify_betradar_scoreboard(self):
        """
        DESCRIPTION: click on event and verify betradar scoreboard
        EXPECTED: EDP should display bet radar scoreboard with visualization (if available other wise fall back should be display)
        """
        pass
