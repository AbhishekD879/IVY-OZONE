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
class Test_C41790452_Verify_connection_creation_to_Cash_Out_MS_without_accountHistory_request(Common):
    """
    TR_ID: C41790452
    NAME: Verify connection creation to Cash Out MS without accountHistory request
    DESCRIPTION: This test case verifies connection creation to Cash Out MS and accountHistory request removed.
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page/tab
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

    def test_001_navigate_to_open_bets_tab__sports_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab > 'Sports' sub-tab
        EXPECTED: * 'Open Bets' tab is opened with 'Sports' sub-tab selected
        """
        pass

    def test_002_verify_get_bet_details_requestfrom_release_xxxxxverify_websocket_connection_to_cashout_ms(self):
        """
        DESCRIPTION: Verify GET **bet-details** request
        DESCRIPTION: **From release XXX.XX:**
        DESCRIPTION: Verify WebSocket connection to Cashout MS
        EXPECTED: * EventStream connection is created to Cash Out MS
        EXPECTED: * Only ONE active connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS (see EventStream tab of request)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WebSocket connection to Cashout MS is created
        EXPECTED: * Only ONE active connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type **event:initial** is received from Cash Out MS
        """
        pass

    def test_003_verify_accounthistory_request(self):
        """
        DESCRIPTION: Verify 'accountHistory' request
        EXPECTED: * 'accountHistory' request is removed from 'Open Bets' tab > 'Sports' sub-tab(this request isn't used anymore for this tab, except /accountHistory/count? which is made for Bet Counter on mobile).
        EXPECTED: * All data is received in EventStream connection to Cash Out MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * 'accountHistory' request is removed from 'Open Bets' tab > 'Sports' sub-tab(this request isn't used anymore for this tab, except /accountHistory/count? which is made for Bet Counter on mobile).
        EXPECTED: * All data is received in WebSocket connection to Cashout MS
        """
        pass

    def test_004_navigate_to_lotto_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Lotto' sub-tab
        EXPECTED: * Connection to Cashout MS is closed
        EXPECTED: * 'accountHistory' request is made with group=LOTTERYBET
        """
        pass

    def test_005_navigate_to_pools_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Pools' sub-tab
        EXPECTED: * 'accountHistory' request is made with group=POOLBET
        """
        pass

    def test_006_navigate_to_sports_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Sports' sub-tab
        EXPECTED: * EventStream connection is created to Cash Out MS
        EXPECTED: * 'accountHistory' request is NOT made (except /accountHistory/count? which is made for Bet Counter on mobile)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WebSocket connection to Cashout MS is created
        EXPECTED: * 'accountHistory' request is NOT made (except /accountHistory/count? which is made for Bet Counter on mobile)
        """
        pass
