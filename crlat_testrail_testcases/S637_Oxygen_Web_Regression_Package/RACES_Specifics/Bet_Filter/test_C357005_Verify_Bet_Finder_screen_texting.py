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
class Test_C357005_Verify_Bet_Finder_screen_texting(Common):
    """
    TR_ID: C357005
    NAME: Verify Bet Finder screen texting
    DESCRIPTION: This test case verifies info messages present at the Bet Finder page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
    PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
    PRECONDITIONS: BMA-37013 Horse Racing : Bet Filter
    PRECONDITIONS: Use:
    PRECONDITIONS: https://connect-app-tst1.coral.co.uk/#/bet-finder (Connect app)
    PRECONDITIONS: https://connect-invictus.coral.co.uk/#/bet-finder (Oxygen)
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

    def test_003_navigate_to_any_horse_racing_event_details_page(self):
        """
        DESCRIPTION: Navigate to any Horse racing event details page
        EXPECTED: **For Mobile:**
        EXPECTED: 'Bet Filter' link is present in the header in the right
        EXPECTED: **For Desktop:**
        EXPECTED: 'Bet Filter' link is present in the header to the left of 'Meeting' selector
        """
        pass

    def test_004_tap_bet_filter(self):
        """
        DESCRIPTION: Tap 'Bet Filter'
        EXPECTED: * Bet finder page is opened
        """
        pass

    def test_005_verify_header(self):
        """
        DESCRIPTION: Verify header
        EXPECTED: Header contains:
        EXPECTED: * back button (redirects user to previously visited page)
        EXPECTED: * 'BET FILTER' text
        EXPECTED: * 'Reset' button ('Reset Filters' for Ladbrokes only)
        """
        pass

    def test_006_verify_the_texting_above_the_filters(self):
        """
        DESCRIPTION: Verify the texting above the filters
        EXPECTED: [Connect] / [Oxygen]
        EXPECTED: * Top text block should read:
        EXPECTED: BET FILTER
        EXPECTED: Use filters or Coral's Digital Tipster to find your best bets, also save your selection for future use.
        EXPECTED: Create your search below:
        """
        pass

    def test_007_verify_the_find_bets_bar_is_sticky_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Verify the 'Find Bets' bar is sticky to the bottom of the page
        EXPECTED: - The bar should never be hidden while user scrolls up/down
        """
        pass
