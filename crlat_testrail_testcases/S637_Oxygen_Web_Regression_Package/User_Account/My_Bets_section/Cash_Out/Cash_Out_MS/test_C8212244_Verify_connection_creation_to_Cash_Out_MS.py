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
class Test_C8212244_Verify_connection_creation_to_Cash_Out_MS(Common):
    """
    TR_ID: C8212244
    NAME: Verify connection creation to Cash Out MS
    DESCRIPTION: This test case verifies connection creation to Cash Out MS
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
        EXPECTED: * 'Open Bets' page/tab is opened
        """
        pass

    def test_002_verify_get_bet_details_requestfrom_release_xxxxxverify_websocket_connection_to_cash_out_ms(self):
        """
        DESCRIPTION: Verify GET **bet-details** request
        DESCRIPTION: **From release XXX.XX:**
        DESCRIPTION: Verify websocket connection to Cash Out MS
        EXPECTED: * EventStream connection is created to Cash Out MS
        EXPECTED: * Only ONE active connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS (see EventStream tab of request)
        EXPECTED: * Time of bet placement is in BST in 'event stream' response
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Websocket connection is created to Cash Out MS
        EXPECTED: * Only ONE active connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_003_trigger_loss_of_connection_and_restore_it(self):
        """
        DESCRIPTION: Trigger loss of connection and restore it
        EXPECTED: * Internet connection is restored
        EXPECTED: * Previous connection to Cash Out MS is finished (see Timing tab of request)
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_004_trigger_network_changeeg_switch_from_wi_fi_to_3g_though_lost_connection(self):
        """
        DESCRIPTION: Trigger network change
        DESCRIPTION: e.g switch from Wi-Fi to 3G though lost connection
        EXPECTED: * Network is changed
        EXPECTED: * Previous connection to Cash Out MS is finished (see Timing tab of request)
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_005_perform_partial_cash_out(self):
        """
        DESCRIPTION: Perform partial cash out
        EXPECTED: * Partial Cash Out is successful
        EXPECTED: * Previous EventStream connection is finished (see Timing tab of request)
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        EXPECTED: **From release XXX.XX (or when BMA-53660 will be merged):**
        EXPECTED: * Partial Cash Out is successful
        EXPECTED: * No new connection is created to Cash Out MS
        EXPECTED: * Current connection stays in pending status (not closing)
        EXPECTED: * No getBetDetail call to BPP is sent  after successful partial cashout
        """
        pass

    def test_006_perform_unsuccessful_full_cash_outeg_turn_off_internet_connection_and_tap_cash_out_button(self):
        """
        DESCRIPTION: Perform unsuccessful full cash out
        DESCRIPTION: e.g turn off internet connection and tap 'Cash out' button
        EXPECTED: * Full cash out is unsuccessful
        EXPECTED: * Previous connection to Cash Out MS is finished (see Timing tab of request)
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_007_perform_successful_full_cash_out(self):
        """
        DESCRIPTION: Perform successful full cash out
        EXPECTED: * Full cash out is successful
        EXPECTED: * No new EventStream connection is created
        EXPECTED: * Update with type event:initial is received in same * EventStream connection (eg. price change update)
        EXPECTED: Actual from 103 release for both brands:
        EXPECTED: * Full cash out is successful
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Previous connection to Cash Out MS is finished (see Timing tab of request)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_008_navigate_away_from_open_bets_pagetab(self):
        """
        DESCRIPTION: Navigate away from 'Open Bets' page/tab
        EXPECTED: * Connection to Cash Out MS is finished (see Timing tab of request)
        EXPECTED: * No new connection is created
        """
        pass

    def test_009_navigate_to_cash_out_pagetab_and_repeat_steps_2_8_coral_only(self):
        """
        DESCRIPTION: Navigate to 'Cash out' page/tab and repeat steps 2-8 (Coral only)
        EXPECTED: 
        """
        pass

    def test_010_go_to_edp_of_the_event_that_has_bets_placed_with_cash_out_optionand_repeat_steps_2_8na_on_ladbrokes(self):
        """
        DESCRIPTION: Go to EDP of the event that has bets placed with Cash out option
        DESCRIPTION: and repeat steps #2-8
        DESCRIPTION: N/A on Ladbrokes
        EXPECTED: 
        """
        pass

    def test_011_go_to_edp_of_the_event_that_has_no_bets_placedna_on_ladbrokes(self):
        """
        DESCRIPTION: Go to EDP of the event that has no bets placed
        DESCRIPTION: N/A on Ladbrokes
        EXPECTED: * **bet-details** request is NOT sent
        EXPECTED: * EventStream connection is NOT created to Cash Out MS
        """
        pass
