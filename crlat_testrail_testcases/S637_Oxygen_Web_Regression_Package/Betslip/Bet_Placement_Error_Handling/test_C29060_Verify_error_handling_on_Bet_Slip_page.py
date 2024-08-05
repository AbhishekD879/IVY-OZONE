import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29060_Verify_error_handling_on_Bet_Slip_page(Common):
    """
    TR_ID: C29060
    NAME: Verify error handling on 'Bet Slip' page
    DESCRIPTION: This test scenario verifies error handling on 'Bet Slip' page, when 500 console error appears with particular error codes.
    PRECONDITIONS: -Load the app and log in
    PRECONDITIONS: -Add any selection to betslip and open it
    PRECONDITIONS: -Enter valid stakes for any bet lines
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
    PRECONDITIONS: Dev's support is needed to check all cases.OR use Charles to edit Status code on POST {environment}/Proxy/v1/buildBet response or POST {environment}/Proxy/v1/placeBet
    """
    keep_browser_open = True

    def test_001_trigger_error_occurrence_of_500_error_in_console_described_in_preconditions_for_placebet_request___tap_place_bet(self):
        """
        DESCRIPTION: Trigger error occurrence of 500 error in console (described in Preconditions) for placeBet request -> Tap 'Place Bet'
        EXPECTED: Error pop-up is shown
        """
        pass

    def test_002_verify_error_pop_up(self):
        """
        DESCRIPTION: Verify error pop-up
        EXPECTED: **Coral**
        EXPECTED: Header:
        EXPECTED: *   'Bet Placement Service Unavailable' label
        EXPECTED: *   'X' button to close the message
        EXPECTED: Body:
        EXPECTED: *   'We're sorry. Bet Placement service is currently unavailable, please try again later. If this problem persists, contact our Customer Service Department' text message
        EXPECTED: *   'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened)
        EXPECTED: **Ladbrokes:**
        EXPECTED: *   'Bet Placement Service Unavailable' header label
        EXPECTED: *   'We're sorry. Bet Placement service is currently unavailable, please try again later.
        EXPECTED: *   'OK' button to close pop-up
        """
        pass

    def test_003_close_pop_up(self):
        """
        DESCRIPTION: Close pop-up
        EXPECTED: * Selections remain displayed in Betslip
        EXPECTED: * 'Place Bet' button remains active
        """
        pass

    def test_004_remove_selections_from_betslip_and_close_it(self):
        """
        DESCRIPTION: Remove selections from betslip and close it
        EXPECTED: 
        """
        pass

    def test_005___trigger_error_occurance_of_500_error_in_console_described_in_preconditionsfor_buildbet_request__add_any_selection_to_betslip(self):
        """
        DESCRIPTION: - Trigger error occurance of 500 error in console (described in Preconditions) for buildBet request
        DESCRIPTION: - Add any selection to betslip
        EXPECTED: Error pop-up is shown
        EXPECTED: **Coral**
        EXPECTED: Header:
        EXPECTED: *   'Bet Placement Service Unavailable' label
        EXPECTED: *   'X' button to close the message
        EXPECTED: Body:
        EXPECTED: *   'We're sorry. Bet Placement service is currently unavailable, please try again later. If this problem persists, contact our Customer Service Department' text message
        EXPECTED: *   'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened)
        EXPECTED: **Ladbrokes:**
        EXPECTED: *   'Bet Placement Service Unavailable' header label
        EXPECTED: *   'We're sorry. Bet Placement service is currently unavailable, please try again later.
        EXPECTED: *   'OK' button to close pop-up
        """
        pass

    def test_006___close_pop_up__open_betslip(self):
        """
        DESCRIPTION: - Close pop-up
        DESCRIPTION: - Open Betslip
        EXPECTED: *   Content is not loaded
        EXPECTED: *   'Server is unavailable at the moment, please try again later. If this problem persists, contact our Customer Service Department' error message is shown on the page
        EXPECTED: *   'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened) is available
        EXPECTED: *   'Reload' button to refresh page
        EXPECTED: **From OX100.3 Ladbrokes (Coral from OX 101.1):**
        EXPECTED: * Content is not loaded
        EXPECTED: * 'Oops! We are having trouble loading this page. Please check your connection' error message is shown with 'Try Again' button
        """
        pass
