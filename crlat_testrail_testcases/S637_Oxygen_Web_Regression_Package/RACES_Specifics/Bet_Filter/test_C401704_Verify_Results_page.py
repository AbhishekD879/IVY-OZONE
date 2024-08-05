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
class Test_C401704_Verify_Results_page(Common):
    """
    TR_ID: C401704
    NAME: Verify Results page
    DESCRIPTION: This test case verifies Bet Finder Results page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2439 - Web: Results page
    PRECONDITIONS: - BMA-37013 Horse Racing : Bet Filter
    PRECONDITIONS: Use
    PRECONDITIONS: Connect app:
    PRECONDITIONS: https://connect-app-tst1.coral.co.uk/#/bet-finder
    PRECONDITIONS: for testing in desktop browser
    PRECONDITIONS: Sportsbook/Coral:
    PRECONDITIONS: https://connect-invictus.coral.co.uk/#/bet-finder/
    """
    keep_browser_open = True

    def test_001_load_httpsconnect_app_tst1coralcoukbet_finder(self):
        """
        DESCRIPTION: Load https://connect-app-tst1.coral.co.uk/#/bet-finder
        EXPECTED: Bet Finder page is loaded.
        """
        pass

    def test_002_apply_some_filtering_tap_find_bets_button(self):
        """
        DESCRIPTION: Apply some filtering. Tap 'Find bets' button
        EXPECTED: - User is redirected to Bet Filter Results screen;
        EXPECTED: - 'Back' button with 'Horse Racing / Bet Filter Results ' text are shown in header;
        EXPECTED: - Filtering [Sort by TIME/ODDS] is present in header on the right (for Sportsbook version only);
        EXPECTED: - Verify "# Results" label is shown beneath the header;
        EXPECTED: - Correct # of the results is shown;
        EXPECTED: - Results match the filtering parameters applied.
        """
        pass

    def test_003_verify_the_proper_details_are_shown_for_the_result_items(self):
        """
        DESCRIPTION: Verify the proper details are shown for the result items
        EXPECTED: The following details should be provided:
        EXPECTED: - Jockey
        EXPECTED: - Trainer
        EXPECTED: - Form
        EXPECTED: - Price
        EXPECTED: - Silks
        EXPECTED: - Time selection is running
        EXPECTED: - Runner Number
        EXPECTED: - Draw (for Sportsbook version only)
        """
        pass

    def test_004_verify_results_sorting_sportsbook_version_only(self):
        """
        DESCRIPTION: Verify results sorting (Sportsbook version only)
        EXPECTED: - Results order default to by time;
        EXPECTED: - Select odds and it sorts them by shortest price > longest price if there's a price that's the same we display the next off higher
        """
        pass

    def test_005_valid_only_for_ladbrokesclick_on_horse_racing_on_horse_racing__bet_filter_results__on_header(self):
        """
        DESCRIPTION: VALID ONLY FOR LADBROKES:
        DESCRIPTION: Click on Horse Racing on 'Horse Racing / Bet Filter Results ' on header
        EXPECTED: - Horse Racing landing page is opened
        """
        pass
