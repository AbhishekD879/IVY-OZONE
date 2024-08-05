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
class Test_C44870395_Verify_betplacements_on_banach_market_selection_with_Freebets(Common):
    """
    TR_ID: C44870395
    NAME: Verify betplacements on banach market selection with Freebets
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_bet_on_a_banache_market_using_a_free_bet(self):
        """
        DESCRIPTION: Place a bet on a Banache market using a free bet
        EXPECTED: You should have placed a bet on a Banache market using a free bet
        """
        pass
