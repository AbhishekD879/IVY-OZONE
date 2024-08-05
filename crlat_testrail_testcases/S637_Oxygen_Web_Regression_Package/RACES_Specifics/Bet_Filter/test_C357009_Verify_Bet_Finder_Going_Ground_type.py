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
class Test_C357009_Verify_Bet_Finder_Going_Ground_type(Common):
    """
    TR_ID: C357009
    NAME: Verify Bet Finder Going (Ground type)
    DESCRIPTION: This test case verifies Going parameter the Bet Finder page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
    PRECONDITIONS: - HMN-2437 - Web: Filtering Logic for Bet Finder
    PRECONDITIONS: - BMA-37013 Horse Racing : Bet Filter
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

    def test_003_verify_going_ground_type_proven_on_the_ground_on_ladbrokes(self):
        """
        DESCRIPTION: Verify Going (ground type) ('Proven on the Ground' on Ladbrokes)
        EXPECTED: Has the only option 'Proven'
        """
        pass

    def test_004_verify_going_onoff(self):
        """
        DESCRIPTION: Verify Going ON/OFF
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"provenGoing": "Y"} param / {"provenGoing": "N"} param
        """
        pass

    def test_005_verify_filtering_plus_refreshre_navigationselect_filters___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify filtering + refresh/re-navigation:
        DESCRIPTION: Select filters -> tap 'Save selection' button
        EXPECTED: - Filtering should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_006_verify_filtering_plus_reset(self):
        """
        DESCRIPTION: Verify Filtering + Reset
        EXPECTED: - Filtering should clear on Reset
        """
        pass
