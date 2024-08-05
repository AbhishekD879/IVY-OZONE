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
class Test_C357010_Verify_Digital_Tipster_Filters(Common):
    """
    TR_ID: C357010
    NAME: Verify Digital Tipster Filters
    DESCRIPTION: This test case verifies Supercomputer filters at Bet Finder page
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

    def test_003_verify_digital_tipster_filters_values(self):
        """
        DESCRIPTION: Verify Digital Tipster Filters values
        EXPECTED: The next values should be present:
        EXPECTED: - Selection
        EXPECTED: - Alternative
        EXPECTED: - Each-Way
        """
        pass

    def test_004_verify_filtering_by_selectioncheck_off_selection__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by selection.
        DESCRIPTION: Check off 'selection' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "S"} param
        """
        pass

    def test_005_verify_filtering_by_alternativecheck_off_alternative__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by alternative.
        DESCRIPTION: Check off 'alternative' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "A"} param
        """
        pass

    def test_006_verify_filtering_by_each_waycheck_off_each_way__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by each-way.
        DESCRIPTION: Check off 'each-way' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "E"} param
        """
        pass

    def test_007_verify_the_supercomputer_filters_work_as_radio_buttons(self):
        """
        DESCRIPTION: Verify the supercomputer filters work as radio buttons
        EXPECTED: - Once clicked > option is selected. One more click on the same option de-selects it.
        EXPECTED: - Once clicked on option A, then click on option B selects option B and auto-deselects option A.
        """
        pass

    def test_008_verify_supercomputer_filters_plus_refreshre_navigationselect_any_filter___tap_save_selection_button(self):
        """
        DESCRIPTION: Verify Supercomputer filters + refresh/re-navigation:
        DESCRIPTION: Select any filter -> tap 'Save selection' button
        EXPECTED: - Supercomputer filters selected value should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass

    def test_009_verify_supercomputer_filters_plus_reset(self):
        """
        DESCRIPTION: Verify Supercomputer filters + Reset
        EXPECTED: - Supercomputer filters value should clear on Reset
        """
        pass
