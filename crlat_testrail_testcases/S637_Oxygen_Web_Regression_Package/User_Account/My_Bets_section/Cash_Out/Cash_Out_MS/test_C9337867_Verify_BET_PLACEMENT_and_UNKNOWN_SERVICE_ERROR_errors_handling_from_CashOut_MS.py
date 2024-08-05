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
class Test_C9337867_Verify_BET_PLACEMENT_and_UNKNOWN_SERVICE_ERROR_errors_handling_from_CashOut_MS(Common):
    """
    TR_ID: C9337867
    NAME: Verify 'BET_PLACEMENT' and 'UNKNOWN_SERVICE_ERROR' errors handling from CashOut MS
    DESCRIPTION: This test case verifies 'BET_PLACEMENT' and 'UNKNOWN_SERVICE_ERROR' errors handling from Cash Out MS on Cash Out page/widget
    DESCRIPTION: TO UPDATE according to BMA-50940
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: In order to trigger 'BET_PLACEMENT' and 'UNKNOWN_SERVICE_ERROR' errors assistance from developer`s side is needed
    """
    keep_browser_open = True

    def test_001_trigger_bet_placement_error_on_cash_out_ms(self):
        """
        DESCRIPTION: Trigger 'BET_PLACEMENT' error on Cash Out MS
        EXPECTED: 
        """
        pass

    def test_002_go_to_cash_out_pagewidget(self):
        """
        DESCRIPTION: Go to Cash Out page/widget
        EXPECTED: * Cash Out page/widget is opened
        EXPECTED: * EventStream connection to Cash Out MS is set up
        EXPECTED: * The next error is received in **event:initial** response
        EXPECTED: data:{"error":{"code":"BET_PLACEMENT"}}
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cash Out page/widget is opened
        EXPECTED: * WebSocket connection to Cash Out MS is set up
        EXPECTED: * The next error is received in **event:initial** response
        EXPECTED: data:{"error":{"code":"BET_PLACEMENT"}}
        """
        pass

    def test_003_verify_cash_out_pagewidget(self):
        """
        DESCRIPTION: Verify Cash Out page/widget
        EXPECTED: 'Oops! We are having trouble loading this page. Please check your connection' error message is displayed. 'Try Again' button is shown
        """
        pass

    def test_004_click_on_try_again_button(self):
        """
        DESCRIPTION: Click on 'Try Again' button
        EXPECTED: New EventStream request is sent to Cash Out MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * New WebSocket connection to Cash Out MS is created
        EXPECTED: * Data is loaded on Cash Out page/widget
        """
        pass

    def test_005_go_to_any_other_page(self):
        """
        DESCRIPTION: Go to any other page
        EXPECTED: 
        """
        pass

    def test_006_trigger_unknown_service_error_error_on_cash_out_ms(self):
        """
        DESCRIPTION: Trigger 'UNKNOWN_SERVICE_ERROR' error on Cash Out MS
        EXPECTED: 
        """
        pass

    def test_007_go_to_cash_out_pagewidget(self):
        """
        DESCRIPTION: Go to Cash Out page/widget
        EXPECTED: * Cash Out page/widget is opened
        EXPECTED: * EventStream connection to Cash Out MS is set up
        EXPECTED: * The next error is received in **event:initial** response
        EXPECTED: data:{"error":{"code":"UNKNOWN_SERVICE_ERROR"}}
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cash Out page/widget is opened
        EXPECTED: * WebSocket connection to Cash Out MS is set up
        EXPECTED: * The next error is received in **event:initial** response
        EXPECTED: data:{"error":{"code":"UNKNOWN_SERVICE_ERROR"}}
        """
        pass

    def test_008_repeat_step_3_5(self):
        """
        DESCRIPTION: Repeat step #3-5
        EXPECTED: 
        """
        pass
