import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C9272896_To_edit_Verify_UNAUTHORIZED_ACCESS_error_handling_from_Cash_Out_MS(Common):
    """
    TR_ID: C9272896
    NAME: [To edit] Verify 'UNAUTHORIZED_ACCESS' error handling from Cash Out MS
    DESCRIPTION: !!!Endpoint was removed at ox105 https://{domain}/Proxy/auth/invalidateSession!!!!
    DESCRIPTION: This test case verifies 'UNAUTHORIZED_ACCESS' error handling from Cash Out MS on Cash Out page/widget
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Suspend event from the bet so that cashout is not available for this bet
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: where token - bpp token
    PRECONDITIONS: To trigger situation when BPP token is wrong or expired
    PRECONDITIONS: * Open Postman
    PRECONDITIONS: * Send DELETE request to bpp with a valid username and token in 'Request Header':
    PRECONDITIONS: https://{domain}/Proxy/auth/invalidateSession -H token: user_token
    PRECONDITIONS: where 'domain' may be
    PRECONDITIONS: * bpp-dev1.coralsports.dev.cloud.ladbrokescoral.com - dev1
    PRECONDITIONS: * bpp-dev0.coralsports.dev.cloud.ladbrokescoral.com - dev0
    PRECONDITIONS: e.g. ![](index.php?/attachments/get/27916)
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_page_or_cash_out_tab_on_betslip_widget_on_desktop_or_tablet(self):
        """
        DESCRIPTION: Go to Cash Out page or Cash Out tab on Betslip widget on Desktop or Tablet
        EXPECTED: * Cash Out page/tab is opened
        EXPECTED: * EventStream connection to Cash Out MS is set up
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cash Out page/tab is opened
        EXPECTED: * WebSocket connection to Cashout MS is created
        """
        pass

    def test_002___trigger_situation_when_bpp_token_is_wrong_or_expired__trigger_update_for_cash_out_bet_eg_unsuspend_event_from_preconditions(self):
        """
        DESCRIPTION: - Trigger situation when BPP token is wrong or expired
        DESCRIPTION: - Trigger update for Cash out bet (e.g unsuspend event from preconditions)
        EXPECTED: * The next error is received from Cash Out MS in **betUpdate** OR **initial** models
        EXPECTED: {"error":{"code":"UNAUTHORIZED_ACCESS"}}
        EXPECTED: * Current connection to MS is closed
        """
        pass

    def test_003__open_network_tab___all_tab___set_log_filter_check_new_temporary_token(self):
        """
        DESCRIPTION: * Open Network tab -> All tab -> set 'log' filter
        DESCRIPTION: * Check new temporary token
        EXPECTED: * **GetTemporaryAuthenticationToken** request is sent to get temporary token
        EXPECTED: * Session token is received in response and corresponds to **sessionToken.sessionToken** attribute
        """
        pass

    def test_004__open_network_tab___xhr_tab___set_bpp_filter_check_user_request(self):
        """
        DESCRIPTION: * Open Network tab -> XHR tab -> set 'bpp' filter
        DESCRIPTION: * Check **user** request
        EXPECTED: * **user** request is sent to BPP
        EXPECTED: * The same as on step #3 temporary session token is sent 'Request Payload' section of **user** request
        EXPECTED: * New BPP token is received in response and corresponds to **token** attribute
        """
        pass

    def test_005_verify_open_betscash_out_page(self):
        """
        DESCRIPTION: Verify Open bets/Cash Out page
        EXPECTED: * New EventStream connection is created to Cash Out MS with updated **token** in the query
        EXPECTED: * Only ONE connection is created to Cash Out MS
        EXPECTED: * No errors appear on Cash Out page/widget
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * New WebSocket connection is created to Cash Out MS with updated **token** in the query
        EXPECTED: * Only ONE connection is created to Cash Out MS
        EXPECTED: * No errors appear on Cash Out page/widget
        """
        pass

    def test_006_trigger_any_live_update_for_cash_out_beteg_price_changesuspension(self):
        """
        DESCRIPTION: Trigger any Live update for Cash out bet
        DESCRIPTION: e.g price change/suspension
        EXPECTED: * Update is received from Cash Out MS
        EXPECTED: * Cash Out bet is updated
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cashout MS will send cashoutUpdate with new cashoutValue
        EXPECTED: * Cash Out bet is updated
        """
        pass

    def test_007_make_partialfull_cash_out(self):
        """
        DESCRIPTION: Make partial/full cash out
        EXPECTED: * Partial/full cash out is successfully made
        EXPECTED: * No error is present
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Partial/full cash out is successfully made
        EXPECTED: * No error is present
        EXPECTED: * Cashout MS will send betUpdate message with an updated bet
        """
        pass

    def test_008_repeat_steps_2_4_and_trigger_that_new_bpp_token_is_wrong_or_expired_from_the_second_trynote_block_bpp_and_temporarytoken_requests_ex_httpsbpp_dev0coralsportsdevcloudladbrokescoralcomproxyauthuserhttpsfantom5_invictuscoralcoukencoralsportsapitemporarytoken_(self):
        """
        DESCRIPTION: Repeat steps #2-4 and trigger that new BPP token is wrong or expired from the second try
        DESCRIPTION: Note: block BPP and temporarytoken requests (ex. https://bpp-dev0.coralsports.dev.cloud.ladbrokescoral.com/Proxy/auth/user
        DESCRIPTION: https://fantom5-invictus.coral.co.uk/en/coralsports/api/temporarytoken?_)
        EXPECTED: 
        """
        pass

    def test_009_verify_open_betscash_out_pagewidget(self):
        """
        DESCRIPTION: Verify Open bets/Cash Out page/widget
        EXPECTED: * 'Cash out service unavailable' pop-up is displayed:
        EXPECTED: 'We're sorry. Cash Out service is currently unavailable, please try again later. If this problem persists, contact our Customer Service Department' error message is shown on the page
        EXPECTED: * 'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened) is available
        EXPECTED: * 'Reload' button to refresh the page is shown on 'Cash Out' page/widget under pop-up
        EXPECTED: * No new connection is created to Cash Out MS
        EXPECTED: **From OX100.3 Ladbrokes (Coral version TBC)**
        EXPECTED: *   'Oops! We are having trouble loading this page. Please check your connection' error message is shown on the page
        EXPECTED: *   'Try Again' button to refresh the page
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Pop-up is displayed
        EXPECTED: * 'Cash Out unsuccessful, please try again' message is displayed under pop-up
        EXPECTED: * No new connection is created to Cash Out MS
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/118935557)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/118935559)
        """
        pass

    def test_010_go_to_edp_with_placed_bets_on_cash_out_option_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Go to EDP with placed bets on Cash out option and repeat steps #2-5
        EXPECTED: 
        """
        pass
