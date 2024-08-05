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
class Test_C59551281_Verify_visualization_and_scoreboard_when_event_moved_from_pre_play_to_inplay(Common):
    """
    TR_ID: C59551281
    NAME: Verify visualization and scoreboard when event moved from pre-play to inplay
    DESCRIPTION: test case verifies visualization and scoreboard when event moved from pre-play to inplay
    PRECONDITIONS: 1. Prematch Ice Hockey event is available
    PRECONDITIONS: 2. Prematch Ice Hockey event is subscribed to betradar Scoreboard
    PRECONDITIONS: 3. Prematch Ice Hockey event is about to be moved into Inplay state
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    PRECONDITIONS: to trigger event move from pre play to inplay
    PRECONDITIONS: - change event time current time
    PRECONDITIONS: - set is off flag to yes in OB event level
    PRECONDITIONS: - check be in lay list check box in OB event level
    """
    keep_browser_open = True

    def test_001_navigate_to_ice_hockey_events_landing_page_fromhome___ice_hockey___matches(self):
        """
        DESCRIPTION: Navigate to Ice Hockey events landing page from
        DESCRIPTION: Home - Ice Hockey - matches
        EXPECTED: today tab should display with all the today's events
        """
        pass

    def test_002_move_any_pre_match_event_to_inplay_from_pre_conditions(self):
        """
        DESCRIPTION: move any pre match event to inplay from pre conditions
        EXPECTED: Inplay event should display with fall back scoreboard
        EXPECTED: 1. Fallback scoreboard should display
        EXPECTED: 2. Scoreboard should updated as per results
        EXPECTED: 3. default market should display with respective odds
        EXPECTED: 4. # of other markets with clickable icon should display
        """
        pass

    def test_003_click_on_event_and_verify_betradar_scoreboard(self):
        """
        DESCRIPTION: click on event and verify betradar scoreboard
        EXPECTED: EDP should display betradar scoreboard with visualization
        """
        pass
