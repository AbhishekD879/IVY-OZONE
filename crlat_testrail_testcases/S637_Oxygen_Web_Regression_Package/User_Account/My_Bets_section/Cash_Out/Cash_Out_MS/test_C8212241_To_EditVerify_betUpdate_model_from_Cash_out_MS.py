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
class Test_C8212241_To_EditVerify_betUpdate_model_from_Cash_out_MS(Common):
    """
    TR_ID: C8212241
    NAME: [To Edit]Verify 'betUpdate' model from Cash out MS
    DESCRIPTION: This test case verifies updates received in 'betUpdate' model from Cash out MS
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WS connection to Cashout MS is created when user lands on myBets page
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: NB! CMS config will be removed when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    PRECONDITIONS: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: In the app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Place a bet on a selection with handicap value available
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
        DESCRIPTION: Navigate to 'Open Bets' page/tab
        EXPECTED: * EventStream connection is created to Cash Out MS
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

    def test_003_trigger_suspension_in_openbet_ti_for_event_market_selection(self):
        """
        DESCRIPTION: Trigger suspension in Openbet TI for
        DESCRIPTION: * event
        DESCRIPTION: * market
        DESCRIPTION: * selection
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS **cashoutValue: "CASHOUT**_**SELN**_**SUSPENDED**" and **cashoutStatus:"Cashout unavailable: Selections are not active**
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet is shown as suspended on 'Open Bets' page
        """
        pass

    def test_004_trigger_unsuspension_in_openbet_ti_for_event_market_selection(self):
        """
        DESCRIPTION: Trigger unsuspension in Openbet TI for
        DESCRIPTION: * event
        DESCRIPTION: * market
        DESCRIPTION: * selection
        EXPECTED: * Update with type **event:cashoutUpdate** or **event:betUpdate** on EDP is received from Cash Out MS with **cashoutValue:{value}** and **cashoutStatus:""**
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet is shown as active on 'Open Bets' page
        """
        pass

    def test_005_trigger_undispaying_in_openbet_ti_for_event_market_selection(self):
        """
        DESCRIPTION: Trigger undispaying in Openbet TI for
        DESCRIPTION: * event
        DESCRIPTION: * market
        DESCRIPTION: * selection
        EXPECTED: * betUpdate undisplay update is not present in the getBetDetail requests
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet is shown as active on 'Open Bets' page
        """
        pass

    def test_006_trigger_dispaying_in_openbet_ti_for_event_market_selection(self):
        """
        DESCRIPTION: Trigger dispaying in Openbet TI for
        DESCRIPTION: * event
        DESCRIPTION: * market
        DESCRIPTION: * selection
        EXPECTED: * betUpdate display update is not present in the getBetDetail requests
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet is shown as active on 'Open Bets' page
        """
        pass

    def test_007_trigger_handicap_value_change_in_openbet_ti_for_market(self):
        """
        DESCRIPTION: Trigger handicap value change in Openbet TI for
        DESCRIPTION: * market
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS with **cashoutValue: CASHOUT**_**HCAP**_**CHANGED** and **cashoutStatus:Cashout unavailable: Selections are not available for cashout**
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet remains shown on 'Open Bets' page but without 'Cash out' button
        """
        pass

    def test_008_trigger_setting_result_in_openbet_ti_for_event_market_selection(self):
        """
        DESCRIPTION: Trigger setting result in Openbet TI for
        DESCRIPTION: * event
        DESCRIPTION: * market
        DESCRIPTION: * selection
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet disappers from 'Open Bets' page
        """
        pass

    def test_009_trigger_some_update_different_than_suspension_display_handicap_change_in_openbet_tieg_disporder_ew_change(self):
        """
        DESCRIPTION: Trigger some update different than suspension, display, handicap change in Openbet TI
        DESCRIPTION: e.g. dispOrder, E/W change
        EXPECTED: * Update with type **event:betUpdate** is NOT received from Cash Out MS
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        """
        pass

    def test_010_go_to_multiple_cash_out_bet_and_repeat_steps_3_9(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet and repeat steps #3-9
        EXPECTED: 
        """
        pass

    def test_011_go_to_edp_this_bets_placed_on_cash_out_option_available_coral_only(self):
        """
        DESCRIPTION: Go to EDP this bets placed on Cash Out option available (CORAL ONLY)
        EXPECTED: NOTE! For step 8 (regarding setting results) the expected result is:
        EXPECTED: * Bet disappears from EDP after page refresh
        """
        pass

    def test_012_repeat_steps_2_10(self):
        """
        DESCRIPTION: Repeat steps #2-10
        EXPECTED: 
        """
        pass

    def test_013_go_to_cash_out_tabpage_and_repeat_steps_2_10_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash Out' tab/page and repeat steps #2-10 (CORAL ONLY)
        EXPECTED: NOTE! For step 7 (regarding Handicap value change) the expected result is:
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS with **cashoutValue: CASHOUT**_**HCAP**_**CHANGED** and **cashoutStatus:Cashout unavailable: Selections are not available for cashout**
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * Bet is removed from 'Cash out' page/tab
        """
        pass
