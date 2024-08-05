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
class Test_C44870392_Verify_the_market_is_not_available_of_display_for_Bet_inplay_All_Banach_Markets(Common):
    """
    TR_ID: C44870392
    NAME: Verify the market is not available/of display for Bet inplay. ( All Banach Markets)
    DESCRIPTION: 
    PRECONDITIONS: There should be FootBall in-Play matches
    """
    keep_browser_open = True

    def test_001_load_app_and_navigate_to_football___in_play_page(self):
        """
        DESCRIPTION: Load App and navigate to Football  > In-Play page
        EXPECTED: Foot ball in-Play page is loaded
        """
        pass

    def test_002_verify_for_banach_marketscoral__yourcallladbrokes__getaprice(self):
        """
        DESCRIPTION: Verify for Banach Markets
        DESCRIPTION: Coral : #Yourcall
        DESCRIPTION: Ladbrokes : #GETAPRICE
        EXPECTED: User should not see / find any Banach Markets for in-Play events
        """
        pass
