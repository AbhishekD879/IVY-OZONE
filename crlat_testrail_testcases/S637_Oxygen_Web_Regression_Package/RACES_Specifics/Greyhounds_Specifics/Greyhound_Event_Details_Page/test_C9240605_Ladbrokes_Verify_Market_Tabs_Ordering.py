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
class Test_C9240605_Ladbrokes_Verify_Market_Tabs_Ordering(Common):
    """
    TR_ID: C9240605
    NAME: [Ladbrokes] Verify Market Tabs Ordering
    DESCRIPTION: This test case verifie markets tabs ordering
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 Racecard Layout Update - Markets and Selections area
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_go_to_the_greyhounds_event_details_page(self):
        """
        DESCRIPTION: Go to the greyhounds event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_verify_market_tabs_ordering(self):
        """
        DESCRIPTION: Verify market tabs ordering
        EXPECTED: The tabs are sorted in following order:
        EXPECTED: *   'Win Or E/W' tab
        EXPECTED: *   'Forecast' and 'Tricast' tabs if available
        EXPECTED: *   'Win Only' tab
        EXPECTED: *   'Betting WO' markets split into separate tabs
        EXPECTED: *   All other markets split into separate tabs
        """
        pass
