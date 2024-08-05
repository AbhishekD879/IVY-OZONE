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
class Test_C9607563_Verify_bet_placement_from_the_Surface_Bets(Common):
    """
    TR_ID: C9607563
    NAME: Verify bet placement from the Surface Bets
    DESCRIPTION: Test case verifies possibility to place bet from the Surface Bet
    DESCRIPTION: AUTOTEST: [C9770723]
    PRECONDITIONS: 1. There are a few Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_place_the_bet_using_price_button_of_the_surface_bet_from_the_betslip_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the Betslip. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_002_place_the_bet_using_price_button_of_the_surface_bet_from_the_quickbet_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the QuickBet. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        pass
