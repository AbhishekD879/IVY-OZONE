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
class Test_C60068804_Verify_new_remotebetslip_connection_opens_after_25_min_of_inactivity_and_new_subscribe_message_received_for_event(Common):
    """
    TR_ID: C60068804
    NAME: Verify new remotebetslip connection opens after 25 min of inactivity and new subscribe message received for event
    DESCRIPTION: This test case verifies new remotebetslip connection opens after 25 min of inactivity and new subscribe message received for event
    PRECONDITIONS: 1. QuickBet should be enabled in CMS > System Configuration > quickBet
    PRECONDITIONS: NOTE: remotebetslip connection open when app is loaded
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

    def test_002_lock_device_for_25min_should_be_any_time_thats_more_than_20minin_ti_update_price_for_same_selection(self):
        """
        DESCRIPTION: Lock device for ~25min (should be any time that's more than 20min)
        DESCRIPTION: In TI update price for same selection
        EXPECTED: 
        """
        pass

    def test_003_unlock_device_after_25_min_and_verify_ws_connection(self):
        """
        DESCRIPTION: Unlock device after 25 min and verify WS connection
        EXPECTED: * New WS connection created
        EXPECTED: * New subscription message received
        EXPECTED: * Selection added with updated price
        """
        pass
