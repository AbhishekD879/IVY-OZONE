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
class Test_C59551039_Verify_the_visualization_and_scoreboard_soon_after_the_event_is_finished_Best_of_3_games(Common):
    """
    TR_ID: C59551039
    NAME: Verify the visualization and scoreboard soon after the event is finished : Best of 3 games
    DESCRIPTION: Test case verifies visualization and scoreboard after the event is finished for the event singles with best of 3 games
    PRECONDITIONS: 1. Table Tennis event(s) should subscribe to Betradar Scoreboards
    PRECONDITIONS: 2. Event should be in InPlay state
    PRECONDITIONS: To trigger event finished
    PRECONDITIONS: XXXX[TBD]
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_inplay_table_tennis_edp_froma_z_menu_table_tennis___inplayorhome___table_tennis___inplay(self):
        """
        DESCRIPTION: Navigate to Inplay Table Tennis EDP from
        DESCRIPTION: A-Z menu table tennis - inplay
        DESCRIPTION: Or
        DESCRIPTION: Home - table tennis - inplay
        EXPECTED: Event details page should open
        """
        pass

    def test_002_trigger_event_finish_scenario_from_the_precondition(self):
        """
        DESCRIPTION: Trigger event finish scenario from the precondition
        EXPECTED: TBD
        """
        pass

    def test_003_verify_ui_of_match_finish_event(self):
        """
        DESCRIPTION: Verify UI of match finish event
        EXPECTED: Following details should display
        EXPECTED: 1. Top left corner : Back button with back navigation symbol
        EXPECTED: 2. Top right corner : bet slip
        EXPECTED: 3. Beside to bet slip left : user icon and balance
        EXPECTED: 4. Header : Table tennis league
        EXPECTED: 5. below to header teams should display at left and right side
        EXPECTED: Left being home and right is away
        EXPECTED: 6. Middle : Ended Label with games own
        EXPECTED: - Possible Outcome
        EXPECTED: - 2:0 or 0:2
        EXPECTED: - 1:2 or 2:1
        EXPECTED: 7 : Each games details scores of each team eg in set 1 team A scores 4 and Team B scores 11 all the details should display in table format
        EXPECTED: 8. Table tennis pitch should display
        EXPECTED: 9. On top of net Label : Match and set won details should display
        EXPECTED: 10 : current set number should display on left side to the net
        EXPECTED: 11. Match won Label should display at the side of winning team
        EXPECTED: 12. On the pitch home and away team names with player names should display opp sides
        EXPECTED: 13 : default tab should be highlighted
        EXPECTED: 14 : Timer should display at last game
        """
        pass

    def test_004_repeat_above_step_for_the_event_doubles_with_best_of_3_games(self):
        """
        DESCRIPTION: repeat above step for the event doubles with best of 3 games
        EXPECTED: 
        """
        pass
