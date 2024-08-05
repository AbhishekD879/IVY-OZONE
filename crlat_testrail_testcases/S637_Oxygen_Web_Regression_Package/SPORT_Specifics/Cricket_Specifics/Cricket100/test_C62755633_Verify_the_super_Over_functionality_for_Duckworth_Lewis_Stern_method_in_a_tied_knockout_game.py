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
class Test_C62755633_Verify_the_super_Over_functionality_for_Duckworth_Lewis_Stern_method_in_a_tied_knockout_game(Common):
    """
    TR_ID: C62755633
    NAME: Verify the super Over functionality for Duckworth/Lewis/Stern method in a tied knockout game
    DESCRIPTION: This testcase verifies the super over functionality for Duckworth/Lewis/Stern method in a tied knockout game
    PRECONDITIONS: 1.Login to Application.
    PRECONDITIONS: 2.Event should be live.
    PRECONDITIONS: 3. The Scores should be levelled and super over feature comes in
    PRECONDITIONS: 4. On the Scoreboard- it will display the score details as  "SO" with the score related to super over beside the regular score
    PRECONDITIONS: Note:
    PRECONDITIONS: Super over will be Applicable only if match is TIE between two teams when scores are equal, Super over innings is conducted to determine the winner of the match.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket from A-Z sports/ribbon tab/Homepage
        EXPECTED: User should be navigated to cricket.
        EXPECTED: -Matches tab should be  displayed by default
        """
        pass

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to in-play page.
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to_event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to event details page (edp ).
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_scoreboard_in_event_details_page_edp_(self):
        """
        DESCRIPTION: Verify displaying of scoreboard in event details page (edp) .
        EXPECTED: Scoreboard should be displayed on event details page.
        """
        pass

    def test_005_the_1st_innings_must_be_completed_and_the_2nd_innings_team_must_score_the_same_runs_as_that_of_1st_team(self):
        """
        DESCRIPTION: The 1st innings must be completed and the 2nd innings team must score the same runs as that of 1st team
        EXPECTED: Both the team's score should be levelled and then the super over feature should be enabled
        """
        pass

    def test_006_verify_the_rule_for_duckworthlewisstern_method_in_a_tied_knockout_game(self):
        """
        DESCRIPTION: verify the rule for Duckworth/Lewis/Stern method in a tied knockout game
        EXPECTED: 'Super Five' will be played - effectively a five-ball Super Over.
        EXPECTED: If the Super Five is tied, then the team with the higher score after four balls, three balls and so on will be declared the winner.
        EXPECTED: If it is not possible to complete a Super Five due to the weather, a bowl-out will be used, potentially to be held indoors
        """
        pass
