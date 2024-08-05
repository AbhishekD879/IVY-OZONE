import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C74766_Verify_Oxygen_error_handling_during_freebets_requests_to_BPP(Common):
    """
    TR_ID: C74766
    NAME: Verify Oxygen error handling during freebets requests to BPP
    DESCRIPTION: This test case verifies Oxygen app error handling after sending freebet request and not receiving response from BPP
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-16409 Handle errors from BPP during freebets requests - no response back from BPP
    DESCRIPTION: BMA-16395 Handle errors from BPP during freebets requests - Logged Out
    DESCRIPTION: BMA-16408 Handle errors from BPP during freebets requests - Connection dropped with BPP
    DESCRIPTION: BMA-16748 BPP - Combine all BPP service calls during login process into one
    DESCRIPTION: BMA-16749 CLIENT - Combine all BPP service calls during login process into one
    PRECONDITIONS: 1. Link to set private markets:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: 2. Link to generate freebets for user:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Manually+Add+Freebet+Token+to+Account?preview=/36604221/36604223/HowToManuallyAddFreebetTokenToAccount.pdf
    PRECONDITIONS: 3. Developer's help is needed for triggering BPP responses
    PRECONDITIONS: 4. Open Development Tool -> Network and keep it active during testing
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Home page is opened
        """
        pass

    def test_002__log_in_under_user_that_has_freebets_and_private_markets_available_trigger_bpp_not_sending_the_response(self):
        """
        DESCRIPTION: * Log in under user that has freebets and private markets available
        DESCRIPTION: * Trigger BPP not sending the response
        EXPECTED: * User is logged in
        EXPECTED: * Private markets Tab on Home Page is not available for user.
        """
        pass

    def test_003_check_request_displaying_user_in_development_tool(self):
        """
        DESCRIPTION: Check request displaying 'user' in Development Tool
        EXPECTED: Response for Freebets and Private Market is empty:
        EXPECTED: ... login response data ...,
        EXPECTED: 'privateMarkets':
        EXPECTED: { data: []  }
        EXPECTED: ,
        EXPECTED: freeBets:
        EXPECTED: { data: [] }
        EXPECTED: }
        """
        pass

    def test_004_navigate_to_freebets_page(self):
        """
        DESCRIPTION: Navigate to Freebets page
        EXPECTED: * Freebet icon is missing on User balance button on Header, Event details page, Right Slider Menu and Betslip Slider Menu.
        EXPECTED: * Freebets page is opened. No available freebets is displayed.
        """
        pass

    def test_005_check_request_displaying_accountfreebetsfreebettokentypesports__for_freebets_in_development_tool(self):
        """
        DESCRIPTION: Check request displaying 'accountFreebets?freebetTokenType=SPORTS' ( for freebets) in Development tool
        EXPECTED: Response is empty
        """
        pass

    def test_006_verify_that_user_can_place_bets_cashout_bets_and_browse_the_app_successfully(self):
        """
        DESCRIPTION: Verify that user can place bets, cashout bets and browse the app successfully
        EXPECTED: User stays logged in
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log Out
        EXPECTED: User is logged out
        """
        pass

    def test_008__log_in_under_user_that_has_freebets_and_private_markets_available_trigger_bpp_sending__log_out_response(self):
        """
        DESCRIPTION: * Log in under user that has freebets and private markets available
        DESCRIPTION: * Trigger BPP sending  Log OUT response
        EXPECTED: * User is logged in
        EXPECTED: * Private markets on Home Page are not available for user.
        """
        pass

    def test_009_check_request_displaying_user__in_development_tool(self):
        """
        DESCRIPTION: Check request displaying 'user'  in Development tool
        EXPECTED: Error is present in response:
        EXPECTED: "error":"Token expired or user does not exist" message:"Service error"  status :"LOGGED_OUT"
        EXPECTED: ... login response data ...,
        EXPECTED: 'privateMarkets':
        EXPECTED: { data: [], error: status 'LOGGED OUT', error:'Token expired or user does not exist' }
        EXPECTED: ,
        EXPECTED: freeBets:
        EXPECTED: { data: [], error: status 'LOGGED OUT', error:'Token expired or user does not exist' } }
        EXPECTED: }
        """
        pass

    def test_010_repeat_step_4_7(self):
        """
        DESCRIPTION: Repeat step #4-7
        EXPECTED: * Error is present in response:
        EXPECTED: "error":"Token expired or user does not exist" message:"Service error"  status :"LOGGED_OUT"
        EXPECTED: * User stays logged in
        """
        pass

    def test_011_log_in_under_user_that_has_freebets_and_private_markets_available(self):
        """
        DESCRIPTION: Log in under user that has freebets and private markets available
        EXPECTED: * User is logged in
        EXPECTED: * Private markets on Home Page are not available for user.
        """
        pass

    def test_012__trigger_disconnection_with_bpp_turn_off_internet_connection_navigate_to_freebets_page(self):
        """
        DESCRIPTION: * Trigger disconnection with BPP (turn off internet connection)
        DESCRIPTION: * Navigate to Freebets page
        EXPECTED: Maintanence page is shown
        """
        pass

    def test_013_click_on_reload_button(self):
        """
        DESCRIPTION: Click on 'Reload' button
        EXPECTED: Message is shown that there is no connection to internet
        """
        pass

    def test_014_connect_to_internet_and_load_oxygen_app(self):
        """
        DESCRIPTION: Connect to Internet and load Oxygen app
        EXPECTED: User is logged in
        """
        pass
