import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C8212240_Verify_cashoutUpdate_model_from_Cash_out_MS(Common):
    """
    TR_ID: C8212240
    NAME: Verify 'cashoutUpdate' model from Cash out MS
    DESCRIPTION: This test case verifies updates received in 'cashoutUpdate' model from Cash out MS on Cash Out page
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page/tab (Screenshots to be updated)
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: NB! CMS config will be removed when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    PRECONDITIONS: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: In the app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: * https://cashout-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/bet-details?token={token} - beta
    PRECONDITIONS: where token - bpp token
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_pagetab(self):
        """
        DESCRIPTION: Navigate to 'Open bets' page/tab
        EXPECTED: * EventStream connection is created to Cash Out MS
        EXPECTED: ![](index.php?/attachments/get/38795)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created
        """
        pass

    def test_002_go_to_single_cash_out_bet(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet
        EXPECTED: 
        """
        pass

    def test_003_trigger_cash_out_value_increase_in_openbet_tiie_make_price_change(self):
        """
        DESCRIPTION: Trigger Cash out value increase in Openbet TI
        DESCRIPTION: (i.e. make price change)
        EXPECTED: * 'cashoutUpdate' record with new **'cashoutValue'** is received from MS
        EXPECTED: ![](index.php?/attachments/get/38796)
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * 'CASH OUT' button immediately displays new cash out value
        """
        pass

    def test_004_trigger_cash_out_value_decrease_in_openbet_ti(self):
        """
        DESCRIPTION: Trigger Cash out value decrease in Openbet TI
        EXPECTED: * 'cashoutUpdate' record with new **'cashoutValue'** is received from MS
        EXPECTED: ![](index.php?/attachments/get/38797)
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * 'CASH OUT' button immediately displays new cash out value
        """
        pass

    def test_005_trigger_cash_out_value__0_in_openbet_tiie_set_price_to_9001(self):
        """
        DESCRIPTION: Trigger Cash out value = 0 in Openbet TI
        DESCRIPTION: (i.e. set price to 900/1)
        EXPECTED: * 'cashoutUpdate' record with **'cashoutValue=0'** value is received from MS
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * 'Cash Out is unavailable because the offer is less than 0.00' message is shown on grey background instead of cashout button
        EXPECTED: ![](index.php?/attachments/get/38798)
        """
        pass

    def test_006_trigger_some_update_different_than_price_change_in_openbet_tieg_minbet_maxbet_change(self):
        """
        DESCRIPTION: Trigger some update different than price change in Openbet TI
        DESCRIPTION: e.g. minBet, maxBet change
        EXPECTED: * 'cashoutUpdate' record is NOT received from MS
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        """
        pass

    def test_007_go_to_multiple_cash_out_bet_and_repeat_steps_3_6(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet and repeat steps #3-6
        EXPECTED: 
        """
        pass

    def test_008_coral_onlygo_to_event_details_page_of_one_of_the_events_on_which_previous_bets_singlemultiple_were_placed_with_cash_out_option_available(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: Go to Event Details Page of one of the events on which previous bets (Single/Multiple) were placed with Cash Out option available
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_7(self):
        """
        DESCRIPTION: Repeat steps #2-7
        EXPECTED: 
        """
        pass

    def test_010_coral_onlynavigate_to_cash_out_tabpage_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: Navigate to 'Cash out' tab/page and repeat steps #2-7
        EXPECTED: 
        """
        pass
