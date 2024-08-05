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
class Test_C9607564_Verify_Surface_Bets_live_updates(Common):
    """
    TR_ID: C9607564
    NAME: Verify Surface Bets live updates
    DESCRIPTION: Test case verifies price live updates of the Surface Bet
    DESCRIPTION: AUTUTEST: [C9776078]
    PRECONDITIONS: 1. There is a are Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_ti_increase_the_price_for_the_selection_of_some_surface_bet(self):
        """
        DESCRIPTION: In TI increase the price for the selection of some Surface Bet
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_verify_the_price_within_the_price_button_gets_changed_in_live_without_page_refresh(self):
        """
        DESCRIPTION: In the application verify the price within the Price button gets changed in live, without page refresh
        EXPECTED: Corresponding Price button on the Surface Bet card displays new price
        EXPECTED: Price button becomes red for a second
        """
        pass

    def test_003_in_ti_decrease_the_price_for_the_selection_of_some_surface_bet(self):
        """
        DESCRIPTION: In TI decrease the price for the selection of some Surface Bet
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_verify_the_price_within_the_price_button_gets_changed_in_live_without_page_refresh(self):
        """
        DESCRIPTION: in the application verify the price within the Price button gets changed in live, without page refresh
        EXPECTED: Corresponding Price button on the Surface Bet card displays new price
        EXPECTED: Price button becomes blue for a second
        """
        pass
