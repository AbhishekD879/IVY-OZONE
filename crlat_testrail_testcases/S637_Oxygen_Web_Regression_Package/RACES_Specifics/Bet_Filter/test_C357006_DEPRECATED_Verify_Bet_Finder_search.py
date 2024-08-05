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
class Test_C357006_DEPRECATED_Verify_Bet_Finder_search(Common):
    """
    TR_ID: C357006
    NAME: (DEPRECATED) Verify Bet Finder search
    DESCRIPTION: This test case verifies search at the Bet Finder page
    PRECONDITIONS: Jira tickets:
    PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
    PRECONDITIONS: - HMN-2438 - Web: Filtering Logic for Bet Finder
    PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
    PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
    PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
    PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
    """
    keep_browser_open = True

    def test_001_notesearch_is_removed_from_bet_filter_see_story_hmn_2833the_test_case_is_still_kept_since_the_functionality_will_be_just_moved_to_some_other_section(self):
        """
        DESCRIPTION: NOTE:
        DESCRIPTION: SEARCH is removed from Bet Filter (see story HMN-2833).
        DESCRIPTION: The test case is still kept, since the functionality will be just moved to some other section.
        EXPECTED: 
        """
        pass

    def test_002_load_the_app(self):
        """
        DESCRIPTION: Load the app
        EXPECTED: User is at Home screen
        """
        pass

    def test_003_sports__horse_racing__bet_finder(self):
        """
        DESCRIPTION: Sports > Horse racing > Bet Finder
        EXPECTED: 
        """
        pass

    def test_004_verify_search_bar_label(self):
        """
        DESCRIPTION: Verify Search bar label
        EXPECTED: * Search by horse, trainer or jockey
        """
        pass

    def test_005_verify_virtual_keyboard_openingclosing(self):
        """
        DESCRIPTION: Verify virtual keyboard opening/closing
        EXPECTED: * keyboard should open on focus put into the search bar
        EXPECTED: * keyboard should close on the "Go" tapped / focus changed to another field
        """
        pass

    def test_006_verify_search_by_horseenter_the_horse_name__tap_find_bets(self):
        """
        DESCRIPTION: Verify Search by Horse.
        DESCRIPTION: Enter the Horse name > tap 'Find Bets'
        EXPECTED: * After the name was entered verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from
        EXPECTED: http://api.racemodlr.com/cypher/coralTest1/0/ -- {horseName} param
        """
        pass

    def test_007_verify_search_by_trainerenter_the_trainer_name__tap_find_bets(self):
        """
        DESCRIPTION: Verify Search by Trainer.
        DESCRIPTION: Enter the Trainer name > tap 'Find Bets'
        EXPECTED: * After the name was entered verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from
        EXPECTED: http://api.racemodlr.com/cypher/coralTest1/0/ -- {trainerName} param
        """
        pass

    def test_008_verify_search_by_jockeyenter_the_jockey_name__tap_find_bets(self):
        """
        DESCRIPTION: Verify Search by Jockey.
        DESCRIPTION: Enter the Jockey name > tap 'Find Bets'
        EXPECTED: * After the name was entered verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from
        EXPECTED: http://api.racemodlr.com/cypher/coralTest1/0/ -- {jockeyName} param
        """
        pass

    def test_009_verify_search_gives_no_resultsenter_some_search_input_that_would_give_no_results(self):
        """
        DESCRIPTION: Verify Search gives no results.
        DESCRIPTION: Enter some search input that would give no results
        EXPECTED: * After the name was entered verify the proper ResultCount at 'Find Bets' button. Button should read "NO SELECTIONS FOUND" (beneath its label)
        EXPECTED: * 'FIND BETS' button is disabled
        """
        pass

    def test_010_verify_search_string_plus_refreshre_navigationenter_some_search_input___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify Search string + refresh/re-navigation:
        DESCRIPTION: Enter some search input -> tap 'Save selection' button
        EXPECTED: - Search input should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_011_verify_search_string_plus_reset(self):
        """
        DESCRIPTION: Verify Search string + Reset
        EXPECTED: * Search bar should clear on Reset
        """
        pass
