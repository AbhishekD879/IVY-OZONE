import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870386_About_Ladbrokes_Affiliates_developersInvestor_CenterQuick_Links_Shop_Locator_other_ways_to_bet_The_Grid(Common):
    """
    TR_ID: C44870386
    NAME: About Ladbrokes-Affiliates-developers,Investor Center,Quick Links-Shop Locator-other ways to bet-The Grid,
    DESCRIPTION: About Ladbrokes
    DESCRIPTION: Quick Links
    DESCRIPTION: Customer Support
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened
        """
        pass

    def test_002_navigate_to_footer_and_verifyabout_ladbrokesaffiliates_investor_center_restricted_territoriesquick_linksshop_locator_other_ways_to_bet_the_grid_telephone_betting(self):
        """
        DESCRIPTION: Navigate to footer and Verify
        DESCRIPTION: About Ladbrokes
        DESCRIPTION: Affiliates-Investor Center-Restricted Territories,
        DESCRIPTION: Quick Links
        DESCRIPTION: Shop Locator-other ways to bet-The Grid-Telephone Betting
        EXPECTED: When clicked on
        EXPECTED: About Ladbrokes
        EXPECTED: Affiliates-Investor Center-Restricted Territories,
        EXPECTED: Quick Links
        EXPECTED: Shop Locator-other ways to bet-The Grid-Telephone Betting
        EXPECTED: User is navigated to appropriate links.
        """
        pass
