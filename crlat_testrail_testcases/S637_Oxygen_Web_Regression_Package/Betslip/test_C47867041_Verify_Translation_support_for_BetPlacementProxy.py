import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C47867041_Verify_Translation_support_for_BetPlacementProxy(Common):
    """
    TR_ID: C47867041
    NAME: Verify Translation support for BetPlacementProxy
    DESCRIPTION: This test case verifies translations presence in outcomeDetails response
    PRECONDITIONS: - Oxygen app is loaded
    PRECONDITIONS: - TI is loaded
    """
    keep_browser_open = True

    def test_001_open_oxygens_home_page(self):
        """
        DESCRIPTION: Open Oxygen's home page
        EXPECTED: Home page is loaded, list of events is displayed
        EXPECTED: (may be tested from sport landing page or from any other place where User can add selection to BetSlip)
        """
        pass

    def test_002_open_chrome_devtools_and_apply_network___all_filtering(self):
        """
        DESCRIPTION: Open Chrome DevTools and apply Network - All filtering
        EXPECTED: DevTools window is displayed, filter is applied
        """
        pass

    def test_003_filter_requests_by_buildbet(self):
        """
        DESCRIPTION: Filter requests by <buildBet>
        EXPECTED: List of requests is empty
        """
        pass

    def test_004_click_on_any_selection(self):
        """
        DESCRIPTION: Click on any selection
        EXPECTED: Selection is added to BetSlip
        """
        pass

    def test_005_verify_buildbet_request(self):
        """
        DESCRIPTION: Verify <buildBet> request
        EXPECTED: buildBet request is in the requests list with next branches:
        EXPECTED: - legs
        EXPECTED: - bets
        EXPECTED: - outcomeDetails
        """
        pass

    def test_006_expand_outcomedetails_branch(self):
        """
        DESCRIPTION: Expand outcomeDetails branch
        EXPECTED: Next attributes with values are displayed with translations(for example):
        EXPECTED: eventDesc: "ArsenalTest vs Cologne"
        EXPECTED: marketDesc: "Match Betting"
        EXPECTED: name: "Draw"
        """
        pass
