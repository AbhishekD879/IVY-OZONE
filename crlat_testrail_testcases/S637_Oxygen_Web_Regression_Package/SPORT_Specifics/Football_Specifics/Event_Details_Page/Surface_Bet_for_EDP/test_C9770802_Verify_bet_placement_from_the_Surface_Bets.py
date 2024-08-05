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
class Test_C9770802_Verify_bet_placement_from_the_Surface_Bets(Common):
    """
    TR_ID: C9770802
    NAME: Verify bet placement from the Surface Bets
    DESCRIPTION: Test case verifies possibility to place bet from the Surface Bet
    DESCRIPTION: AUTOTEST: [C12600641]
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
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
