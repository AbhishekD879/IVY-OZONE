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
class Test_C357007_Verify_Bet_Finder_Odds(Common):
    """
    TR_ID: C357007
    NAME: Verify Bet Finder Odds
    DESCRIPTION: This test case verifies Odds range at Bet Finder page
    PRECONDITIONS: Jira tickets:
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

    def test_003_verify_odds_section_view_odds_range_on_ladbrokes(self):
        """
        DESCRIPTION: Verify Odds section view ('Odds Range' on Ladbrokes)
        EXPECTED: The next check-boxes labeled as:
        EXPECTED: - Odds On
        EXPECTED: - Evens - 7/2
        EXPECTED: - 4/1 - 15/2
        EXPECTED: - 8/1 - 14/1
        EXPECTED: - 16/1 - 28/1
        EXPECTED: - 33/1 or Bigger
        """
        pass

    def test_004_verify_default_value(self):
        """
        DESCRIPTION: Verify default value
        EXPECTED: * None of the Odds check-boxes is checked
        """
        pass

    def test_005_verify_1_odds_selection_do_this_for_all_filters(self):
        """
        DESCRIPTION: Verify 1 odds selection (do this for all filters)
        EXPECTED: * Verify proper "selection found" value is shown
        """
        pass

    def test_006_verify_multiple_odds_selections(self):
        """
        DESCRIPTION: Verify multiple odds selections
        EXPECTED: * Verify proper "selection found" value is shown
        """
        pass

    def test_007_verify_selections_found_on_range_changed(self):
        """
        DESCRIPTION: Verify selections found on Range_changed
        EXPECTED: * Verify "selections found" value changes as one changes the check-boxes selection
        """
        pass

    def test_008_verify_odds_selection_plus_refreshre_navigationselect_oneseveral_filters_try_different_combinations___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify odds selection + refresh/re-navigation:
        DESCRIPTION: Select one/several filters (try different combinations) -> tap 'Save selection' button
        EXPECTED: * Selection should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_009_verify_selection_plus_reset(self):
        """
        DESCRIPTION: Verify selection + Reset
        EXPECTED: * Selection should get cleared on Reset
        """
        pass
