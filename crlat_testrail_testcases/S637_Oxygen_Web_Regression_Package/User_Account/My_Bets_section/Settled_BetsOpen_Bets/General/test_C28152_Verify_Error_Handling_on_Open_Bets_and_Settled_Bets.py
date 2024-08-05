import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C28152_Verify_Error_Handling_on_Open_Bets_and_Settled_Bets(Common):
    """
    TR_ID: C28152
    NAME: Verify Error Handling on Open Bets and Settled Bets
    DESCRIPTION: This test scenario verifies error handling on 'Settled Bets' tab, when 500 console error appears with particular error codes.
    PRECONDITIONS: Load and login into the application with User
    PRECONDITIONS: User has Open and Settled bets
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: In order to define which error code is received with 500 error it is needed to click on link from error in console -> highligted request ->  'Response'.
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
    PRECONDITIONS: Dev's support is needed to check all cases. Or use Charles to edit Status code on GET {environment}/Proxy/accountHistory response
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: 'Settled Bets' tab is opened with 'Regular' tab selected by default
        """
        pass

    def test_002_wait_until_all_content_is_loaded_within_tab(self):
        """
        DESCRIPTION: Wait until all content is loaded within tab
        EXPECTED: All content is loaded and available
        """
        pass

    def test_003_waittrigger_error_occurance_of_500_error_in_console_described_in_preconditions_on_settled_bets_tab(self):
        """
        DESCRIPTION: Wait/Trigger error occurance of 500 error in console (described in Preconditions) on 'Settled Bets' tab
        EXPECTED: 
        """
        pass

    def test_004_expand_any_collapsible_panel(self):
        """
        DESCRIPTION: Expand any collapsible panel
        EXPECTED: * 'Server is unavailable at the moment, please try again later. If this problem persists, contact our Customer Service Department' error message is shown within expanded panel
        EXPECTED: * 'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened) is available
        EXPECTED: * 'Reload' button to refresh page
        EXPECTED: **From OX100.3 Ladbrokes (Coral from OX 101.1)**
        EXPECTED: *   'Oops! We are having trouble loading this page. Please check your connection' error message is shown within expanded panel
        EXPECTED: *   'Try Again' button to refresh page
        """
        pass

    def test_005_repeat_steps_1_5_steps_for_pools_and_lotto_tabs(self):
        """
        DESCRIPTION: Repeat steps #1-5 steps for 'Pools' and 'Lotto' tabs
        EXPECTED: 
        """
        pass

    def test_006_refresh_page_and_make_sure_that_error_is_no_more_reproducible___go_to_homepage(self):
        """
        DESCRIPTION: Refresh page and make sure that error is no more reproducible -> Go to Homepage
        EXPECTED: *   Homepage is opened
        EXPECTED: *   No errors in console are present
        """
        pass

    def test_007_waittrigger_error_occurance_of_500_error_in_console_described_in_preconditions(self):
        """
        DESCRIPTION: Wait/Trigger error occurance of 500 error in console (described in Preconditions)
        EXPECTED: 
        """
        pass

    def test_008_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled bets' tab on 'My Bets' page (for mobile)
        EXPECTED: *   Content is not loaded
        EXPECTED: * 'Server is unavailable at the moment, please try again later. If this problem persists, contact our Customer Service Department' error message is shown on the page
        EXPECTED: * 'Contact Customer Services' hyperlink (after tapping 'Contact Us' page is opened) is available
        EXPECTED: * 'Reload' button to refresh page
        EXPECTED: **From OX100.3 Ladbrokes (Coral from OX 101.1)**
        EXPECTED: *   'Oops! We are having trouble loading this page. Please check your connection' error message is shown on the page
        EXPECTED: *   'Try Again' button to refresh page
        """
        pass

    def test_009_repeat_steps_3_8_for_open_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: Repeat steps 3-8 for:
        DESCRIPTION: * 'Open Bets' tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        EXPECTED: 
        """
        pass
