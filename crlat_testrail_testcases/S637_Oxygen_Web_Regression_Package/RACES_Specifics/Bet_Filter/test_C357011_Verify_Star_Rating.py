import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C357011_Verify_Star_Rating(Common):
    """
    TR_ID: C357011
    NAME: Verify Star Rating
    DESCRIPTION: This test case verifies Star Rating at Bet Finder page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
    PRECONDITIONS: - HMN-2437 - Web: Filtering Logic for Bet Finder
    PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
    PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
    PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
    PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
    """
    keep_browser_open = True

    def test_001_load_the_app(self):
        """
        DESCRIPTION: Load the app
        EXPECTED: User is at Home screen
        """
        pass

    def test_002_sports__horse_racing__bet_filter(self):
        """
        DESCRIPTION: Sports > Horse racing > Bet Filter
        EXPECTED: 
        """
        pass

    def test_003_verify_select_star_rating_control(self):
        """
        DESCRIPTION: Verify Select Star Rating control
        EXPECTED: - 5 starts (unselected by default);
        EXPECTED: - Turn blue once selected;
        """
        pass

    def test_004_verify_select_star_rating_plus_refreshre_navigationselect_oneseveral_stars___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify Select Star Rating + refresh/re-navigation:
        DESCRIPTION: Select one/several stars -> tap 'Save selection' button
        EXPECTED: - Select Star Rating should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_005_1_select_some_star_rating2_click_the_same_star_just_repeat_step_51(self):
        """
        DESCRIPTION: 1. Select some star rating.
        DESCRIPTION: 2. Click the same star (just repeat step 5.1)
        EXPECTED: 1. Corresponding number of stars become active
        EXPECTED: 2. Select Star Rating should clear
        """
        pass

    def test_006_verify_select_star_rating_plus_reset(self):
        """
        DESCRIPTION: Verify Select Star Rating + Reset
        EXPECTED: - Select Star Rating should clear on Reset
        """
        pass
