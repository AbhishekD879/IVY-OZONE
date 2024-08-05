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
class Test_C64895002_Verify_the_Badge_allocation_process(Common):
    """
    TR_ID: C64895002
    NAME: Verify the Badge allocation process
    DESCRIPTION: This test case verifies the Badge allocation process in 'My Badges' tab og 1-2 Free Page
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

    def test_004_week1___predictionpredict_scores_for_3_matches_and_click_on_submitexchelsea_v_aston_villa__3_1arsenal_v_manchester_city_0_2west_ham_v_wolves_0_2(self):
        """
        DESCRIPTION: Week1 - Prediction
        DESCRIPTION: Predict scores for 3 Matches and click on submit
        DESCRIPTION: Ex:
        DESCRIPTION: Chelsea v Aston Villa – **(3-1)
        DESCRIPTION: Arsenal v Manchester City **(0-2)
        DESCRIPTION: West Ham v Wolves **(0-2)
        EXPECTED: Predicted scores should be updated successfully
        """
        pass

    def test_005_click_on_my_badges_tab(self):
        """
        DESCRIPTION: Click on 'My Badges' tab
        EXPECTED: User should be navigated to 'My Badges' page
        """
        pass

    def test_006_verify_the_earned_badges_by_the_user(self):
        """
        DESCRIPTION: Verify the earned badges by the user
        EXPECTED: User should see 6 Prediction/Primary badges lit up in 'My Badges' page for each team
        """
        pass

    def test_007_week1___resultsconsider_user_prediction_for_chelsea_v_aston_villa_match_is_correct(self):
        """
        DESCRIPTION: Week1 - Results
        DESCRIPTION: Consider user prediction for Chelsea v Aston Villa match is correct
        EXPECTED: 
        """
        pass

    def test_008_verify_the_state_of_badges_for_chelsea_and_aston_villa_teams(self):
        """
        DESCRIPTION: Verify the state of badges for Chelsea and Aston Villa teams
        EXPECTED: * User should see secondary/Correct badges for Chelsea and Aston Villa
        EXPECTED: * Chelsea and Aston Villa team jerseys should display as lit up with green tick mark
        """
        pass

    def test_009_verify_the_total_number_of_earned_badges_for_week1(self):
        """
        DESCRIPTION: Verify the total number of earned badges for Week1
        EXPECTED: User should get the below primary and secondary badges
        EXPECTED: Primary Badges - 6
        EXPECTED: Secondary Badges - 2
        """
        pass

    def test_010_week2___prediction_with_same_userpredict_scores_for_3_matches_and_click_on_submitexliverpool_v_brentford_2_0southampton_v_arsenal_1_0tottenham_v_chelsea_0_3notemake_sure_2_teams_from_week1_and_week2_should_be_same(self):
        """
        DESCRIPTION: Week2 - Prediction with same user
        DESCRIPTION: Predict scores for 3 Matches and click on submit
        DESCRIPTION: Ex:
        DESCRIPTION: Liverpool v Brentford (2-0)
        DESCRIPTION: Southampton v Arsenal (1-0)
        DESCRIPTION: Tottenham v Chelsea (0-3)
        DESCRIPTION: Note:
        DESCRIPTION: Make sure 2 teams from week1 and week2 should be same
        EXPECTED: Predicted scores should be updated successfully
        """
        pass

    def test_011_click_on_my_badges_tab(self):
        """
        DESCRIPTION: Click on 'My Badges' tab
        EXPECTED: User should be navigated to 'My Badges' page
        """
        pass

    def test_012_verify_the_earned_badges_by_the_user(self):
        """
        DESCRIPTION: Verify the earned badges by the user
        EXPECTED: User should see new 4 primary badges instead of 6 as 2 teams has already predicted in week1
        """
        pass

    def test_013_verify_the_total_number_of_primarypredicted_badges(self):
        """
        DESCRIPTION: Verify the total number of primary/predicted badges
        EXPECTED: User should be able to see 10 primary/predicted badges (6 from weeek1 and 4 from week2)
        """
        pass

    def test_014_week2___resultsconsider_user_prediction_for_southampton__arsenal_andtottenham__chelsea_are_correct(self):
        """
        DESCRIPTION: Week2 - Results
        DESCRIPTION: Consider user prediction for Southampton & Arsenal and
        DESCRIPTION: Tottenham & Chelsea are correct
        EXPECTED: 
        """
        pass

    def test_015_verify_the_state_of_badges_forsouthampton___arsenal_andtottenham___chelsea(self):
        """
        DESCRIPTION: Verify the state of badges for
        DESCRIPTION: Southampton - Arsenal and
        DESCRIPTION: Tottenham - Chelsea
        EXPECTED: * User should see secondary/Correct badges for Southampton ,Arsenal and Tottenham
        EXPECTED: * Southampton ,Arsenal and Tottenham team jerseys should display as lit up with green tick mark
        EXPECTED: Note:
        EXPECTED: user has already earned secondary badge for Chelsea in week1 so there will be no change for Chelsea team badge
        """
        pass

    def test_016_verify_the_total_number_of_earned_badges(self):
        """
        DESCRIPTION: Verify the total number of earned badges
        EXPECTED: User should get the below primary and secondary badges
        EXPECTED: Primary Badges - 10
        EXPECTED: Secondary Badges - 5
        """
        pass
