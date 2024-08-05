import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C26524536_Verify_there_are_no_duplicated_BPP_auth_requests(Common):
    """
    TR_ID: C26524536
    NAME: Verify there are no duplicated  BPP auth requests
    DESCRIPTION: AUTOTEST [C58618758]
    DESCRIPTION: This test case verifies there are no multiple BPP auth requests on My Bets/Cashout, Betslip, QuickBet, and Homepage (or any other page)
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has at least 1 stake placed with cashout available
    """
    keep_browser_open = True

    def test_001_open_devtools__application__local_storage_and_modify_bpptoken_value_in_oxuser(self):
        """
        DESCRIPTION: Open devtools > Application > Local Storage and modify bpp.Token value in OX.USER
        EXPECTED: Token is modified
        """
        pass

    def test_002_refresh_pageopen_devtools__network__xhr_and_verify_auth_requests_ex_request_url_httpsbppladbrokescomproxyauthuser(self):
        """
        DESCRIPTION: Refresh page.
        DESCRIPTION: Open devtools > Network > XHR and verify auth requests (ex: Request URL: https://bpp.ladbrokes.com/Proxy/auth/user)
        EXPECTED: There is only 1 auth request
        """
        pass

    def test_003_stay_logged_in_and_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Stay logged in and navigate to My Bets > Open Bets
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2
        EXPECTED: There is only 1 auth request
        """
        pass

    def test_005_logout_and_add_selection_to_quickbet_click_login_and_place_bet(self):
        """
        DESCRIPTION: Logout and add selection to QuickBet. Click Login and place bet
        EXPECTED: Login pop up displayed
        """
        pass

    def test_006_login_to_appopen_devtools__network__xhr_and_verify_auth_requests_ex_request_url_httpsbppladbrokescomproxyauthuser(self):
        """
        DESCRIPTION: Login to app.
        DESCRIPTION: Open devtools > Network > XHR and verify auth requests (ex: Request URL: https://bpp.ladbrokes.com/Proxy/auth/user)
        EXPECTED: There is only 1 auth request
        """
        pass
