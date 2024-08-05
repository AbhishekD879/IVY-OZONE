import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C16268962_Vanilla_to_UPDATE_Verify_calls_sequence_to_BPP_after_login_page_refresh_and_log_out(Common):
    """
    TR_ID: C16268962
    NAME: [Vanilla to UPDATE] Verify calls sequence to BPP after login, page refresh and log out
    DESCRIPTION: This test case verifies private markets and freebets displaying for user according to request and response received
    DESCRIPTION: To Update:
    DESCRIPTION: step 11 - need to recheck - assume should perform only step 8
    DESCRIPTION: step13 - only for Ladbrokes?
    PRECONDITIONS: 1. Link to set private markets:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: 2. Link to generate freebets for user:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Manually+Add+Freebet+Token+to+Account?preview=/36604221/36604223/HowToManuallyAddFreebetTokenToAccount.pdf
    PRECONDITIONS: 3. Clear cache and cookies
    PRECONDITIONS: 4. Open Development Tool -> Network and set filter 'proxy' and keep it active during testing
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is successfully logged in
        """
        pass

    def test_002_check_user_request_presence_in_development_tool(self):
        """
        DESCRIPTION: Check 'user' request presence in Development Tool
        EXPECTED: 'user' request is sent with session token and username.
        EXPECTED: e.g.
        EXPECTED: token:"AsC1DPt8sohjDQtMz5lwgNBgsFAw0NDY"
        EXPECTED: username:"lolita"
        """
        pass

    def test_003_check_response_for_user_request(self):
        """
        DESCRIPTION: Check response for 'user' request
        EXPECTED: Response about user, freebets and private markets is present and has next format: {
        EXPECTED: ... login response data ...,
        EXPECTED: 'privateMarkets':
        EXPECTED: { data: [] }
        EXPECTED: ,
        EXPECTED: freeBets:
        EXPECTED: { data: [] }
        EXPECTED: }
        """
        pass

    def test_004_check_private_market_displaying_according_to_response(self):
        """
        DESCRIPTION: Check Private Market displaying according to response
        EXPECTED: * If Private Market is available for user, it's displayed on Home page in the first tab.
        EXPECTED: * If Private Market is not available for user, ' Your Enhanced Markets' tab is not displayed on Home page
        """
        pass

    def test_005_refresh_page_on_home_page_and_verify_request_presence_in_console(self):
        """
        DESCRIPTION: Refresh page on Home Page and verify request presence in console
        EXPECTED: 'accountFreebets?freebetTokenType=ACCESS' ( for private markets) is sent
        EXPECTED: NOTE: 'user' request is not sent
        """
        pass

    def test_006_navigate_to_freebet_page(self):
        """
        DESCRIPTION: Navigate to Freebet page
        EXPECTED: * List of Freebets received in response (step 4) is displayed on Freebet rage.
        EXPECTED: * 'Freebet' icon is displayed on user balance if user has freebets available
        EXPECTED: * If no Freebets available for user, message is shown 'No Freebets available today'
        """
        pass

    def test_007_check_request_sending_accountfreebetsfreebettokentypesports__for_freebets_in_development_tool(self):
        """
        DESCRIPTION: Check request sending 'accountFreebets?freebetTokenType=SPORTS' ( for freebets) in Development Tool
        EXPECTED: Request is sent and list of freebets is received if available
        """
        pass

    def test_008_refresh_the_page_and_check_request_presence_in_console(self):
        """
        DESCRIPTION: Refresh the page and check request presence in console
        EXPECTED: 'accountFreebets?freebetTokenType=SPORTS' ( for freebets) is sent
        EXPECTED: NOTE: 'user' request is not sent
        """
        pass

    def test_009_navigate_to_home_page(self):
        """
        DESCRIPTION: Navigate to Home page
        EXPECTED: Home Page is opened
        """
        pass

    def test_010_check_request_sending_accountfreebetsfreebettokentypeaccess__for_private_markets__in_development_tool(self):
        """
        DESCRIPTION: Check request sending 'accountFreebets?freebetTokenType=ACCESS' ( for private markets)  in Development Tool
        EXPECTED: Request is sent and private markets are received if available
        """
        pass

    def test_011_repeat_step_7_8(self):
        """
        DESCRIPTION: Repeat step #7-8
        EXPECTED: 
        """
        pass

    def test_012_log_out_and_check_no_new_request_sending_in_console(self):
        """
        DESCRIPTION: Log Out and check no new request sending in console
        EXPECTED: * No requests to BPP are sent after log out
        EXPECTED: * User is logged out and redirected on Home page
        EXPECTED: * Private market tab is absent if it was available.
        """
        pass

    def test_013_repeat_steps_2_13_when_logging_in_with_username_in_uppercaseeg_lolita_or_lolita(self):
        """
        DESCRIPTION: Repeat steps #2-13 when logging in with username in Uppercase
        DESCRIPTION: e.g. LOLITA or LOLita
        EXPECTED: 
        """
        pass
