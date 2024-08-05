import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C60068803_Verify_new_price_is_displayed_in_QB_when_user_re_adds_selection_after_20_min_and_price_update(Common):
    """
    TR_ID: C60068803
    NAME: Verify new price is displayed in QB when user re-adds selection after 20 min and price update
    DESCRIPTION: This test case verifies new price is displayed in QB when user re-adds selection after 20 min and price update
    PRECONDITIONS: 1. QuickBet should be enabled in CMS > System Configuration > quickBet
    PRECONDITIONS: **NOTE:** remotebetslip connection open when app is loaded
    """
    keep_browser_open = True

    def test_001_add_selection_to_quickbet(self):
        """
        DESCRIPTION: Add selection to QuickBet
        EXPECTED: * Quick Bet opens
        EXPECTED: * Subscribe message sent
        EXPECTED: * Selection is added with current price
        """
        pass

    def test_002_close_quick_bet_and_de_select_selection(self):
        """
        DESCRIPTION: Close Quick Bet and de-select selection
        EXPECTED: * Quick Bet closed
        EXPECTED: * No unsubscribe message received
        EXPECTED: * Remotebetslip connection remains open
        """
        pass

    def test_003_wait_for_20_minin_ti_change_price_for_same_selection(self):
        """
        DESCRIPTION: Wait for 20 min.
        DESCRIPTION: In TI change price for same selection
        EXPECTED: 
        """
        pass

    def test_004_add_same_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add same selection to Quick Bet
        EXPECTED: * Quick bet opens with selection added
        EXPECTED: * New subscribe message received
        EXPECTED: * New price displayed in Quick Bet
        """
        pass
