import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2554307_Verify_lazy_loading_of_Pools_bets_in_Settled_Bets(Common):
    """
    TR_ID: C2554307
    NAME: Verify lazy loading of Pools bets in Settled Bets
    DESCRIPTION: This test case verifies lazy loading of Pools bets in Settled Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed more than 41 UK Tote bets NOTE The bets are already Settled
    """
    keep_browser_open = True

    def test_001_open_settled_bets_pools(self):
        """
        DESCRIPTION: Open Settled Bets->Pools
        EXPECTED: 20 bets are displayed on the page
        """
        pass

    def test_002_scroll_down_the_list(self):
        """
        DESCRIPTION: Scroll down the list
        EXPECTED: *  New bets are displayed
        EXPECTED: *  Lazy loading displays results in increments of 20 bets
        """
        pass
