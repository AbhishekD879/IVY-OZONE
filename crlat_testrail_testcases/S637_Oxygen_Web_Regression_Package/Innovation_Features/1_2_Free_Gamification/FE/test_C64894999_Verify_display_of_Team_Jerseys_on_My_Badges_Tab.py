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
class Test_C64894999_Verify_display_of_Team_Jerseys_on_My_Badges_Tab(Common):
    """
    TR_ID: C64894999
    NAME: Verify display of Team Jerseys on My Badges Tab
    DESCRIPTION: This test case verifies display of Team Jerseys on My Badges Tab
    PRECONDITIONS: My Badges and Season should be configured in CMS
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: User should be navigated to 1-2 Free page
        """
        pass

    def test_003_verify_display_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify display of 'My Badges' tab
        EXPECTED: User should be able to view 'My Badges' tab
        """
        pass

    def test_004_click_on_my_badges_tab(self):
        """
        DESCRIPTION: Click on 'My Badges' tab
        EXPECTED: User should be able to view team jerseys
        """
        pass

    def test_005_verify_the_state_of_team_jerseys_when_no_predictions_are_made_for_the_teams(self):
        """
        DESCRIPTION: Verify the state of team jerseys when no predictions are made for the teams
        EXPECTED: Team jerseys should display in disabled state
        """
        pass

    def test_006_predict_teams_score_in_this_week_tab_and_submit(self):
        """
        DESCRIPTION: Predict team’s score in 'This week' tab and submit
        EXPECTED: Predicted teams scores should be updated successfully
        """
        pass

    def test_007_click_on_my_badges_tab_and_observe_the_state_of_team_jerseys(self):
        """
        DESCRIPTION: Click on 'My Badges' tab and observe the state of team jerseys
        EXPECTED: Predicted team jerseys should display as lit up
        EXPECTED: Note:
        EXPECTED: Badges awarded details will be updated once in a day based the timings jerseys will lit up
        """
        pass
