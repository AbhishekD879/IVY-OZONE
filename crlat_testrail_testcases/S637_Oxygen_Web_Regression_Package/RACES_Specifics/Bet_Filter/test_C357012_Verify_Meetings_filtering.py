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
class Test_C357012_Verify_Meetings_filtering(Common):
    """
    TR_ID: C357012
    NAME: Verify Meetings filtering
    DESCRIPTION: This test case verifies Meetings filtering at Bet Finder page
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

    def test_003_verify_meetings_filter(self):
        """
        DESCRIPTION: Verify Meetings filter
        EXPECTED: - goes above the other filters
        EXPECTED: - combobox with 'All meetings' value selected by default
        """
        pass

    def test_004_verify_filtering_by_some_combobox_value(self):
        """
        DESCRIPTION: Verify filtering by some combobox value
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"course": "combobox_value"} param
        """
        pass

    def test_005_verify_filtering_plus_refreshre_navigationselect_any_meeting___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify filtering + refresh/re-navigation:
        DESCRIPTION: Select any meeting -> tap 'Save selection' button
        EXPECTED: - Selected filters should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_006_verify_filtering_plus_reset(self):
        """
        DESCRIPTION: Verify filtering + Reset
        EXPECTED: - Selected filters should clear on Reset
        """
        pass
