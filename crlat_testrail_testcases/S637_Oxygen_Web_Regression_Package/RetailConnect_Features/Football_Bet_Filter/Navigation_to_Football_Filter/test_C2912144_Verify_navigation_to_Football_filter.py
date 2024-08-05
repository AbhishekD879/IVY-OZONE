import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2912144_Verify_navigation_to_Football_filter(Common):
    """
    TR_ID: C2912144
    NAME: Verify navigation to Football filter
    DESCRIPTION: This test case verifies navigation to Football Bet Filter from all possible places except Homepage -> Football -> Coupons tab (this verification is done in [C2496181]
    PRECONDITIONS: Make sure Football Bet Filter feature is turned on in CMS: System configuration -> Connect -> football Filter
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Following API returns events for applying Football filters on (After navigating to Football Filter search in console: retailCoupon):
    PRECONDITIONS: **Online betting:**
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LAD0cc93c420eeb433aaf57a1ca299ed93c
    PRECONDITIONS: **In-Shop betting:**
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADe196db0611e240d7a8ea3fc67135c37c
    """
    keep_browser_open = True

    def test_001_open_connect_landing_page(self):
        """
        DESCRIPTION: Open Connect landing page
        EXPECTED: 
        """
        pass

    def test_002_select_football_bet_filter(self):
        """
        DESCRIPTION: Select Football Bet Filter
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * API for in-shop betting returns events
        """
        pass

    def test_003_open_right_hand_menu(self):
        """
        DESCRIPTION: Open Right-hand menu
        EXPECTED: 
        """
        pass

    def test_004_select_football_bet_filter(self):
        """
        DESCRIPTION: Select Football Bet Filter
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * API for in-shop betting returns events
        """
        pass

    def test_005_open_a_z_all_sports_page(self):
        """
        DESCRIPTION: Open 'A-Z' ('All sports') page
        EXPECTED: 
        """
        pass

    def test_006_select_football_bet_filter(self):
        """
        DESCRIPTION: Select Football Bet Filter
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * API for in-shop betting returns events
        """
        pass
