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
class Test_C9240618_Verify_connection_creation_to_Cash_Out_MS_for_Tablet_Desktop(Common):
    """
    TR_ID: C9240618
    NAME: Verify connection creation to Cash Out MS for Tablet/Desktop
    DESCRIPTION: This test case verifies connection creation to Cash Out MS for Tablet/Desktop
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WS connection to Cashout MS is created when user lands on myBets page
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: NB! CMS config will be removed when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    PRECONDITIONS: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Navigate to Cash Out page
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: where token - bpp token
    """
    keep_browser_open = True

    def test_001_go_to_betslip_widget_and_click_on_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Go to Betslip widget and click on 'My bets' > 'Open Bets' tab
        EXPECTED: * 'Open Bets' tab is opened
        EXPECTED: * EventStream connection is created to Cash Out MS (GET **bet-details** request)
        EXPECTED: * Only ONE active connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)(see Timing tab)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS (see EventStream tab of request)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * 'Open Bets' tab is opened
        EXPECTED: * WebSocket connection to Cashout MS is created
        EXPECTED: * Only ONE active connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)(see Timing tab)
        EXPECTED: * Update with type **event:initial** is received in websocket from Cash Out MS
        """
        pass

    def test_002_navigate_to_open_bets_pageclick_on_user_icon__history__betting_history(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' page
        DESCRIPTION: (click on User icon > History > Betting History)
        EXPECTED: * Previous connection is finished (see Timing tab of request)
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_003_perform_any_of_successful_partial_cash_out_unsuccessful_partial_cash_outon_open_bets_page_or_tab(self):
        """
        DESCRIPTION: Perform any of
        DESCRIPTION: * successful partial cash out
        DESCRIPTION: * unsuccessful partial cash out
        DESCRIPTION: on 'Open Bets' page or tab
        EXPECTED: * Both Cash out page and tab are updated
        EXPECTED: * Previous of EventStream connection is finished (see Timing tab of request)
        EXPECTED: * One more EventStream connection is created
        EXPECTED: * Update with type **event:initial** is received
        EXPECTED: **From release XXX.XX (or when BMA-53660 will be merged):**
        EXPECTED: * Both 'Open Bets' page and tab are updated
        EXPECTED: * No new connection is created to Cash Out MS
        EXPECTED: * Current connection stays in pending status: not closing
        EXPECTED: * Bet Update about new stake is received in cashoutBet call
        """
        pass

    def test_004_perform_any_of_successful_full_cash_out_unsuccessful_full_cash_outon_open_bets_page_or_tab(self):
        """
        DESCRIPTION: Perform any of
        DESCRIPTION: * successful full cash out
        DESCRIPTION: * unsuccessful full cash out
        DESCRIPTION: on 'Open Bets' page or tab
        EXPECTED: * Both Cash out page and tab are updated
        EXPECTED: * No new EventStream connection is created
        EXPECTED: * Update with type **event:initial** is received in same EventStream connection (eg. price change update)
        EXPECTED: Actual from 103 release for both brands:
        EXPECTED: * Full cash out is successful
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Previous EventStream connection is finished (see Timing tab of request)
        EXPECTED: * Update with type event:initial is received from Cash Out MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Full cash out is successful
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Previous websocket connection is finished (see Timing tab of request)
        EXPECTED: * Update with type event:initial is received from Cash Out MS
        """
        pass

    def test_005_trigger_any_of_loss_of_connection_and_restore_it_network_change(self):
        """
        DESCRIPTION: Trigger any of
        DESCRIPTION: * loss of connection and restore it
        DESCRIPTION: * network change
        EXPECTED: * Previous of EventStream connection is finished (see Timing tab of request)
        EXPECTED: * One more EventStream connection is created
        EXPECTED: * Connections stay in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Previous websocket connection is finished (see Timing tab of request)
        EXPECTED: * New websocket connection is created
        EXPECTED: * Connections stay in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received
        """
        pass

    def test_006_navigate_away_from_open_bets_page(self):
        """
        DESCRIPTION: Navigate away from 'Open Bets' page
        EXPECTED: * The EventStream connection stays active
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * The websocket connection is closed
        """
        pass

    def test_007_coral_onlynavigate_to_edp_of_the_event_that_has_bets_placed_with_cash_out_option(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: Navigate to EDP of the event that has bets placed with Cash out option
        EXPECTED: * EDP is opened
        EXPECTED: * Previous of EventStream connection is finished (see Timing tab of request)
        EXPECTED: * One more EventStream connection is created
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS (see EventStream tab of request)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * EDP is opened
        EXPECTED: * Previous websocket connection is finished (see Timing tab of request)
        EXPECTED: * New websocket connection is created
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_008_repeat_step_4_5(self):
        """
        DESCRIPTION: Repeat step #4-5
        EXPECTED: 
        """
        pass

    def test_009_navigate_away_from_open_bets_tab_on_betslip_widget(self):
        """
        DESCRIPTION: Navigate away from 'Open Bets' tab on Betslip widget
        EXPECTED: * The EventStream connection stays active
        EXPECTED: **From release XXX.XX:**
        EXPECTED: Websocket connection is closed
        """
        pass

    def test_010_navigate_away_from_edp(self):
        """
        DESCRIPTION: Navigate away from EDP
        EXPECTED: * EventStream connection is finished (see Timing tab of request)
        EXPECTED: * No new connection is created
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Websocket connection is finished (see Timing tab of request)
        EXPECTED: * No new connection is created
        """
        pass

    def test_011_coral_onlyrepeat_all_steps_for_cash_out_tabpage(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: Repeat all steps for 'Cash out' tab/page
        EXPECTED: 
        """
        pass
