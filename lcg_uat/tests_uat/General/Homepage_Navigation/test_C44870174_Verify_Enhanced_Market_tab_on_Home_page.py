import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C44870174_Verify_Enhanced_Market_tab_on_Home_page(Common):
    """
    TR_ID: C44870174
    NAME: Verify Enhanced Market tab on Home page
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should have Private markets
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: App is loaded User is on home page with 'YOUR ENHANCED MARKETS' tab expanded
        """
        pass

    def test_002_click_on_price_selection_of_the_enhanced_market(self):
        """
        DESCRIPTION: click on Price selection of the Enhanced market
        EXPECTED: Mobile : Selection will be added to Quick bet
        EXPECTED: Tablet & Desktop : Selection will be added to bet slip
        """
        pass

    def test_003_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Bet is placed successfully and this private market will disappear from YOUR ENHANCED MARKETS. If this happens to be only private market available to the user, then YOUR ENHANCED MARKETS tab will disappear from the home page once user places the bet.
        """
        pass
