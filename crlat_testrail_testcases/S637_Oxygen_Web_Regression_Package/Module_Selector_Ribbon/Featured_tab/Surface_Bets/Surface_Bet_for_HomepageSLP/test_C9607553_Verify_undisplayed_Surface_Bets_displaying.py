import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9607553_Verify_undisplayed_Surface_Bets_displaying(Common):
    """
    TR_ID: C9607553
    NAME: Verify "undisplayed" Surface Bets displaying
    DESCRIPTION: Test case verifies that undisplayed Surface Bet isn't shown
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_ti_mark_the_selection_from_the_surface_bet_as_not_displayed(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as not displayed
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_the_category_pagehomepage(self):
        """
        DESCRIPTION: In the application refresh the category page/homepage
        EXPECTED: Surface Bet with the undisplayed selection isn't shown
        """
        pass

    def test_003_in_the_ti_mark_the_selection_from_the_surface_bet_as_displayed(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as displayed
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_refresh_the_category_pagehomepage(self):
        """
        DESCRIPTION: In the application refresh the category page/homepage
        EXPECTED: Surface Bet is shown
        """
        pass

    def test_005_pass_1_4_steps_with_undisplaying_on_market_and_event_levels(self):
        """
        DESCRIPTION: Pass 1-4 steps with undisplaying on market and event levels
        EXPECTED: 
        """
        pass
