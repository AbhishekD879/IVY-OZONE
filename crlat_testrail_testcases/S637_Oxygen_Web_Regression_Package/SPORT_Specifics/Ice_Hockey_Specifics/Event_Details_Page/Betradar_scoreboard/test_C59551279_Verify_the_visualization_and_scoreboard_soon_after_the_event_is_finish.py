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
class Test_C59551279_Verify_the_visualization_and_scoreboard_soon_after_the_event_is_finish(Common):
    """
    TR_ID: C59551279
    NAME: Verify the visualization and scoreboard soon after the event is finish
    DESCRIPTION: Test case verifies visualization and scoreboard after the event is finished
    PRECONDITIONS: 1. Ice Hockey event(s) should subscribe to Betradar Scoreboards.
    PRECONDITIONS: 2. Event should be finished
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_ice_hockey_edp_froma_z_menu_ice_hockey___inplayorhome___ice_hockey___inplay(self):
        """
        DESCRIPTION: Navigate to Ice Hockey EDP from
        DESCRIPTION: A-Z menu Ice Hockey - inplay
        DESCRIPTION: Or
        DESCRIPTION: Home - Ice Hockey - inplay
        EXPECTED: Event details page should open
        """
        pass

    def test_002_trigger_or_open_any_event_which_is_finished(self):
        """
        DESCRIPTION: Trigger or open any event which is finished
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
        EXPECTED: 4. Header : Ice Hockey league
        EXPECTED: 5. below the header teams, Home team should display at left and Away team at right side
        EXPECTED: 6. Middle : Ended Label with Match won status on corresponding side of team
        EXPECTED: 7. Ice Hockey pitch should display
        EXPECTED: 8. Match won Label should display at the side of winning team
        EXPECTED: 9. On the pitch, home and away team names should display opp sides
        """
        pass
