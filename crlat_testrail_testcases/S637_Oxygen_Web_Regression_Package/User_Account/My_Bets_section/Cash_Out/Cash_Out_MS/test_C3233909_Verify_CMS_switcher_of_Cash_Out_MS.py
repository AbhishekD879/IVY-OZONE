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
class Test_C3233909_Verify_CMS_switcher_of_Cash_Out_MS(Common):
    """
    TR_ID: C3233909
    NAME: Verify CMS switcher of Cash Out MS
    DESCRIPTION: This test case verifies CMS switcher of Cash Out MS
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    DESCRIPTION: NB! Should be archived when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets with CashOut available option
    PRECONDITIONS: * Navigate to Cash Out page/widget
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: where token - bpp token
    """
    keep_browser_open = True

    def test_001_switch_off_isv4enabled_switcher_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Switch off 'isV4Enabled' switcher in CMS and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_002_coral_onlyin_oxygen_app_go_to_cash_out_pageor_cash_out_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: In Oxygen app go to Cash Out page
        DESCRIPTION: OR Cash Out widget for **Tablet/Desktop**
        EXPECTED: * GET **getBetDetails** request is sent to bpp to retrieve all cashout bets
        EXPECTED: * No request is made to Cash Out MS
        """
        pass

    def test_003_go_to_open_bets_tab(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab
        EXPECTED: * GET **accountHistory** request is sent to bpp to retrieve all cashout bets
        EXPECTED: * No request is made to Cash Out MS
        """
        pass

    def test_004_coral_onlygo_to_event_detailed_page_with_the_bet_that_has_cash_out_available(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: Go to Event detailed page with the bet that has Cash Out available
        EXPECTED: The next requests are sent to  bpp to retrieve initial cashout bets
        EXPECTED: * GET **getBetDetails** request is sent to CashOut MS to retrieve all bets
        EXPECTED: * GET **getBetsPlaced** request is sent to BPP to retrieve all placed bets
        EXPECTED: * GET **getBetDetail** request is sent to BPP to retrieve all bets for current event by betID
        EXPECTED: * No request is made to Cash Out MS
        """
        pass

    def test_005_switch_on_isv4enabled_switcher_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Switch on 'isV4Enabled' switcher in CMS and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_coral_onlyin_oxygen_app_go_to_cash_out_pageor_cash_out_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: In Oxygen app go to Cash Out page
        DESCRIPTION: OR Cash Out widget for **Tablet/Desktop**
        EXPECTED: The next requests are sent to retrieve initial cashout bets
        EXPECTED: * GET **'bet-details'** request is sent to CashOut MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created
        """
        pass

    def test_007_go_to_open_bets_tab(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab
        EXPECTED: The next requests are sent to retrieve initial cashout bets
        EXPECTED: * GET **'bet-details'** request is sent to CashOut MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created
        """
        pass

    def test_008_coral_onlygo_to_event_detailed_page_with_the_bet_that_has_cash_out_available(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: Go to Event detailed page with the bet that has Cash Out available
        EXPECTED: * GET **getBetDetails** request is sent to BPP to retrieve all cashout bets
        EXPECTED: * GET **getBetsPlaced** request is sent to BPP to retrieve all placed bets
        EXPECTED: * GET **getBetDetail** request is sent to BPP to retrieve all bets for current event by betID
        EXPECTED: * GET **'bet-details'** request is sent to CashOut MS to retrieve all cashout bets
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * GET **getBetDetails** request is sent to BPP to retrieve all cashout bets
        EXPECTED: * GET **getBetsPlaced** request is sent to BPP to retrieve all placed bets
        EXPECTED: * GET **getBetDetail** request is sent to BPP to retrieve all bets for current event by betID
        EXPECTED: * WebSocket connection to Cashout MS is created
        """
        pass
