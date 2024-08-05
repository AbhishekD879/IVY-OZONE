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
class Test_C2296993_Verify_In_shop_Bets_tab_view_without_any_coupons(Common):
    """
    TR_ID: C2296993
    NAME: Verify In-shop Bets tab view without any coupons
    DESCRIPTION: This test case verifies Bet History mode on Bet Tracker: In-shop Bets tab with added coupons
    DESCRIPTION: User story: BMA-30953 Bet History mode on Bet Tracker
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Log in
    """
    keep_browser_open = True

    def test_001_open_bet_history(self):
        """
        DESCRIPTION: Open Bet History
        EXPECTED: 
        """
        pass

    def test_002_verify_in_shop_bets_tabs_presence(self):
        """
        DESCRIPTION: Verify 'IN-SHOP BETS tabs presence
        EXPECTED: IN-SHOP BETS tab is displayed (the last one)
        """
        pass

    def test_003_verify_in_shop_bets_tab_when_no_coupons_are_available(self):
        """
        DESCRIPTION: Verify IN-SHOP BETS tab when no coupons are available
        EXPECTED: * '!' icon
        EXPECTED: * Text message says "You have no In-Shop bets history."
        """
        pass

    def test_004__open_browser_dev_toll___network___select_connect_requestand_verify_in_shop_bets_tab_shows_data_according_to_retail_bpp_response(self):
        """
        DESCRIPTION: * Open browser dev toll -> Network -> select 'connect' request
        DESCRIPTION: and verify IN-SHOP BETS tab shows data according to Retail-BPP response
        EXPECTED: * Retail-BPP (https://retail-bpp-stg.coral.co.uk/rcomb/v7/connect) returns 0 open bets and 0 settled bet:
        EXPECTED: open: {total: 0}
        EXPECTED: settled: {total: 0}
        """
        pass
