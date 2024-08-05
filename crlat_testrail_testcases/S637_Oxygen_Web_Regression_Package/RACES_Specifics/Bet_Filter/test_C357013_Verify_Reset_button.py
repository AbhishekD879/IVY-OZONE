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
class Test_C357013_Verify_Reset_button(Common):
    """
    TR_ID: C357013
    NAME: Verify Reset button
    DESCRIPTION: This test case verifies Reset button at Bet Finder page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
    PRECONDITIONS: - HMN-2437 - Web: Filtering Logic for Bet Finder
    PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
    PRECONDITIONS: - BMA-37013 Horse Racing : Bet Filter
    PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
    PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
    PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
    """
    keep_browser_open = True

    def test_001_load_the_app(self):
        """
        DESCRIPTION: Load the app
        EXPECTED: Home page opens
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse racing landing page
        EXPECTED: 'Bet Filter' link is present in the header in the right
        """
        pass

    def test_003_tap_bet_filter(self):
        """
        DESCRIPTION: Tap 'Bet Filter'
        EXPECTED: Bet finder page opens
        """
        pass

    def test_004_verify_reset_button_reset_filters_for_ladbrokes_only(self):
        """
        DESCRIPTION: Verify 'Reset' button ('Reset Filters' for Ladbrokes only)
        EXPECTED: 'Reset' button is displayed in header ('Reset Filters' for Ladbrokes only)
        """
        pass

    def test_005_make_some_selections_and_clicktap_reset_reset_filters_for_ladbrokes_only(self):
        """
        DESCRIPTION: Make some selections and click/tap 'Reset' ('Reset Filters' for Ladbrokes only)
        EXPECTED: - All the filters are at their default state;
        EXPECTED: - Bet finder results should show ALL the data from http://api.racemodlr.com/cypher/coralTest1/0/
        """
        pass
