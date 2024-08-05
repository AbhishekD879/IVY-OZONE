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
class Test_C29176_500_error_handling_on_Cash_Out_page(Common):
    """
    TR_ID: C29176
    NAME: 500 error handling on 'Cash Out' page
    DESCRIPTION: This test scenario verifies error handling on 'Cash Out' page, when 500 console error appears with particular error codes
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Data is present on 'Cash out' tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: In order to define which error code is received with 500 error it is needed to click on link from error in console -> highlagted request ->  'Response'.
    PRECONDITIONS: Code is shown in format: "code":Nxxx (e.g. "code":3503)
    PRECONDITIONS: Where N is server code:
    PRECONDITIONS: *   1: Pirozhok Proxy Error;
    PRECONDITIONS: *   2: OXI Api Error;
    PRECONDITIONS: *   3: Betplacement Api Error;
    PRECONDITIONS: *   4: Betplacement Api Authentication Error;
    PRECONDITIONS: xxx - is error code:
    PRECONDITIONS: *   500: Unhandled error;
    PRECONDITIONS: *   521: Parse Error, caused by invalid response from OpenBet servers;
    PRECONDITIONS: *   400: Bad Request, caused by bad request from our App to Pirozhok Proxy;
    PRECONDITIONS: *   503: Service unavailable error, caused when some server is down;
    PRECONDITIONS: Dev's support is needed to check all cases. Or use Charles to edit Status code on the following:
    PRECONDITIONS: POST {host}/Proxy/v1/cashoutBet - to trigger error pop-up
    PRECONDITIONS: GET {host}/Proxy/getBetDetails OR GET {host}/bet-details for cashout v4 - to trigger error message on tab/page
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_002___trigger_error_occurance_of_500_error_in_console_described_in_preconditions_for_cashoutbet_request__cash_out_any_bet_line(self):
        """
        DESCRIPTION: - Trigger error occurance of 500 error in console (described in Preconditions) for cashoutBet request
        DESCRIPTION: - Cash Out any bet line
        EXPECTED: Error pop-up is shown on 'Cash Out' page
        """
        pass

    def test_003_verify_error_pop_up(self):
        """
        DESCRIPTION: Verify error pop-up
        EXPECTED: **Coral**
        EXPECTED: Header:
        EXPECTED: *   'Cash Out Service Unavailable' label
        EXPECTED: *   'X' button to close the message
        EXPECTED: Body:
        EXPECTED: *   'We're sorry. Cash Out service is currently unavailable, please try again later. If this problem persists, contact our Customer Service Department' text message
        EXPECTED: *   'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened)
        EXPECTED: **Ladbrokes:**
        EXPECTED: *   'Cash Out Service Unavailable' header label
        EXPECTED: *   'We're sorry. Cash Out service is currently unavailable, please try again later.
        EXPECTED: *   'OK' button to close pop-up
        """
        pass

    def test_004_close_pop_up(self):
        """
        DESCRIPTION: Close pop-up
        EXPECTED: * Content of 'Cash out' tab remains displayed
        EXPECTED: * 'Cash out' buttons remain active
        """
        pass

    def test_005_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: 
        """
        pass

    def test_006_trigger_error_occurance_of_500_error_in_console_described_in_preconditionsfor_getbetdetailsbet_details_request(self):
        """
        DESCRIPTION: Trigger error occurance of 500 error in console (described in Preconditions) for getBetDetails/bet-details request
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: Error pop-up is shown (the same content as described in step 3)
        """
        pass

    def test_008_close_pop_up(self):
        """
        DESCRIPTION: Close pop-up
        EXPECTED: *   Content is not loaded
        EXPECTED: *   'Server is unavailable at the moment, please try again later. If this problem persists, contact our Customer Service Department' error message is shown on the page
        EXPECTED: *   'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened) is available
        EXPECTED: *   'Reload' button to refresh page
        EXPECTED: **From OX100.3 Ladbrokes (Coral from OX 101.1):**
        EXPECTED: * Content is not loaded
        EXPECTED: * 'Oops! We are having trouble loading this page. Please check your connection' error message is shown with 'Try Again' button
        """
        pass
