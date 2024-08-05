import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C357008_Verify_Bet_Finder_Form(Common):
    """
    TR_ID: C357008
    NAME: Verify Bet Finder Form
    DESCRIPTION: This test case verifies Form section at Bet Finder page
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

    def test_003_verify_form_section_check_boxes(self):
        """
        DESCRIPTION: Verify Form section check-boxes
        EXPECTED: Expected items:
        EXPECTED: - Course and Distance Winner (long button, as compared to the rest Form buttons that are 1/2 of this)
        EXPECTED: - Course Winner
        EXPECTED: - Winner Last Time
        EXPECTED: - Placed Last Time
        EXPECTED: - Distance Winner
        EXPECTED: - Winner Within Last 3
        EXPECTED: - Placed Within Last 3
        """
        pass

    def test_004_verify_filtering_by_course_and_distance_winnercheck_off_course_and_distance_winner__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Course and Distance Winner.
        DESCRIPTION: Check off 'Course and Distance Winner' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"courseDistanceWinner": "Y"} param
        """
        pass

    def test_005_verify_filtering_by_course_winnercheck_off_course_winner__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Course Winner.
        DESCRIPTION: Check off 'Course Winner' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"courseWinner": "Y"} param
        """
        pass

    def test_006_verify_filtering_by_winner_last_timecheck_off_winner_last_time__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Winner Last Time.
        DESCRIPTION: Check off 'Winner Last Time' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"winnerLastTime": "Y"} param
        """
        pass

    def test_007_verify_filtering_by_placed_last_timecheck_off_placed_last_time__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Placed Last Time.
        DESCRIPTION: Check off 'Placed Last Time' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"placedLastTime": "Y"} param
        """
        pass

    def test_008_verify_filtering_by_distance_winnercheck_off_distance_winner__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Distance Winner.
        DESCRIPTION: Check off 'Distance Winner' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"distanceWinner": "Y"} param
        """
        pass

    def test_009_verify_filtering_by_winner_within_last_3check_off_winner_within_last_3__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Winner Within Last 3.
        DESCRIPTION: Check off 'Winner Within Last 3' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"winnerLast3Starts": "Y"} param
        """
        pass

    def test_010_verify_filtering_by_placed_within_last_3check_off_placed_within_last_3__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Placed Within Last 3.
        DESCRIPTION: Check off 'Placed Within Last 3' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"placedLast3Starts": "Y"} param
        """
        pass

    def test_011_verify_filtering_by_several_parameters(self):
        """
        DESCRIPTION: Verify filtering by several parameters
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button
        EXPECTED: - Verify Bet finder results by several parameters
        """
        pass

    def test_012_verify_filtering_plus_refreshre_navigationselect_oneseveral_filters___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify filtering + refresh/re-navigation:
        DESCRIPTION: Select one/several filters -> tap 'Save selection' button
        EXPECTED: - Filtering should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_013_verify_filtering_plus_reset(self):
        """
        DESCRIPTION: Verify filtering + Reset
        EXPECTED: - Filtering should clear on Reset
        """
        pass
