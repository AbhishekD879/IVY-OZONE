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
class Test_C896432_Verify_Quick_Bet_Websockets_connection_establishing(Common):
    """
    TR_ID: C896432
    NAME: Verify Quick Bet Websockets connection establishing
    DESCRIPTION: This test case verifies that Websocket connection is set only after selection was added to Quick Bet and session id is received and saved in Session Storage
    PRECONDITIONS: 1. Open Development tool > Network> WS > enter 'quickbet' in filter
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_and_check_websockets(self):
        """
        DESCRIPTION: Load Oxygen app and check Websockets
        EXPECTED: Connection with QuickBet microservice is not set in Websockets
        """
        pass

    def test_002_add_selection_to_betslip_and_check_websockets(self):
        """
        DESCRIPTION: Add selection to betslip and check Websockets
        EXPECTED: Connection with QuickBet microservice is establiched
        """
        pass

    def test_003_check_session_id_is_received_in_30000_notification(self):
        """
        DESCRIPTION: Check session id is received in 30000 notification
        EXPECTED: ID is present
        """
        pass

    def test_004_verify_id_is_set_in_session_storage_development_tool__application_session_storage__oxygen_app(self):
        """
        DESCRIPTION: Verify ID is set in session storage (Development tool > Application> Session storage > Oxygen app)
        EXPECTED: Session id is set in session storage and it's validation is set to 24 hours
        """
        pass

    def test_005_refresh_the_page_and_check_websockets(self):
        """
        DESCRIPTION: Refresh the page and check Websockets
        EXPECTED: * Connection with QuickBet microservice is establiched and session id is present in Request Header
        EXPECTED: ( e.g. wss://betslip-dev0.symphony-solutions.eu/quickbet/?id=52a99188-9b9c-4bb9-af26-3d685fd05b84&EIO=3&transport=websocket)
        EXPECTED: * 30000 notification is not received
        EXPECTED: * Quick Bet Menu is opened
        """
        pass

    def test_006_change_session_id_in_session_storage_and_refresh_the_page(self):
        """
        DESCRIPTION: Change session id in Session storage and refresh the page
        EXPECTED: * Page is refreshed
        EXPECTED: * Quick Bet Menu is closed and selection is unselected
        EXPECTED: * Session id is removed from Session storage
        """
        pass

    def test_007_check_websockets_connection(self):
        """
        DESCRIPTION: Check Websockets connection
        EXPECTED: * Error is received in QuickBet microservice WS connection with message: "Session not found"
        """
        pass

    def test_008_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is opened
        EXPECTED: * Connection with QuickBet microservice is establiched in a new WS connection
        """
        pass

    def test_009_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps #3-5
        EXPECTED: 
        """
        pass

    def test_010_log_in_and_repeat_steps_1_9(self):
        """
        DESCRIPTION: Log In and repeat steps #1-9
        EXPECTED: Results are the same
        """
        pass
