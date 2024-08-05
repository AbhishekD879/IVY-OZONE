import pytest
import tests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.pages.shared import get_device
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from json import JSONDecodeError


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create event in prod
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C3233909_Verify_CMS_switcher_of_Cash_Out_MS(BaseBetSlipTest):
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

    def get_cashout_connection(self):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                payload = entry[1]['message']['message']['params']['response']['payloadData']
                if 'initial' in payload:
                    return payload.split('42/0,')[0]
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_switch_off_isv4enabled_switcher_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Switch off 'isV4Enabled' switcher in CMS and save changes
        EXPECTED: Changes are saved successfully
        """
        # Verify CashOut tab configuration in CMS
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if not self.is_cashout_tab_enabled:
            raise CmsClientException('CashOut tab is not enabled in CMS')
        event1 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        selection_id1 = list(event1.selection_ids.values())[0]
        self.__class__.eventID1 = event1.event_id
        event2 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        selection_id2 = list(event2.selection_ids.values())[0]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[selection_id1, selection_id2])
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_coral_onlyin_oxygen_app_go_to_cash_out_pageor_cash_out_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: **Coral only:**
        DESCRIPTION: In Oxygen app go to Cash Out page
        DESCRIPTION: OR Cash Out widget for **Tablet/Desktop**
        EXPECTED: * GET **getBetDetails** request is sent to bpp to retrieve all cashout bets
        EXPECTED: * No request is made to Cash Out MS
        """
        # Manual team confirmed that disabling and verifying not needed as "isV4Enabled" is out of scope

    def test_003_go_to_open_bets_tab(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab
        EXPECTED: * GET **accountHistory** request is sent to bpp to retrieve all cashout bets
        EXPECTED: * No request is made to Cash Out MS
        """
        # Manual team confirmed that disabling and verifying not needed as "isV4Enabled" is out of scope

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
        # Manual team confirmed that disabling and verifying not needed as "isV4Enabled" is out of scope

    def test_005_switch_on_isv4enabled_switcher_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Switch on 'isV4Enabled' switcher in CMS and save changes
        EXPECTED: Changes are saved successfully
        """
        # Manual team confirmed that disabling and verifying not needed as "isV4Enabled" is out of scope

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
        self.site.open_my_bets_cashout()
        self.site.wait_content_state_changed()
        websocket_conn = self.get_cashout_connection()
        self.assertTrue(websocket_conn, msg='WebSocket connection is not sent to Cashout MS')

    def test_007_go_to_open_bets_tab(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab
        EXPECTED: The next requests are sent to retrieve initial cashout bets
        EXPECTED: * GET **'bet-details'** request is sent to CashOut MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created
        """
        self.site.open_my_bets_open_bets()
        self.site.wait_content_state_changed()
        websocket_conn = self.get_cashout_connection()
        self.assertTrue(websocket_conn, msg='WebSocket connection is not sent to Cashout MS')

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
        if self.brand == 'bma':
            self.navigate_to_edp(event_id=self.eventID1)
            self.site.wait_content_state_changed(timeout=10)
            url = f'{tests.settings.bpp}getBetDetails'
            getBetDetails_request = self.get_response_url(url=url)
            self.assertTrue(getBetDetails_request,
                            msg='No "getBetDetails" request is sent to CashOut MS to retrieve all bets')
            url = f'{tests.settings.bpp}getBetsPlaced'
            getBetsPlaced_request = self.get_response_url(url=url)
            self.assertTrue(getBetsPlaced_request,
                            msg='No "getBetsPlaced" request is sent to BPP to retrieve all placed bets')
            url = f'{tests.settings.bpp}getBetDetail?'
            getBetdetail_request = self.get_response_url(url=url)
            self.assertTrue(getBetdetail_request,
                            msg='No "getBetDetail" request is sent to BPP to retrieve all bets '
                                'for current event by betID')
            websocket_conn = self.get_cashout_connection()
            self.assertTrue(websocket_conn, msg='WebSocket connection is not sent to Cashout MS')
