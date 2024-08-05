import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C35219404_Verify_user_request_after_expiration_of_bpp_token(Common):
    """
    TR_ID: C35219404
    NAME: Verify 'user' request after expiration of bpp token
    DESCRIPTION: This test case verifies 'user' request after expiration of bpp token.
    PRECONDITIONS: 1. User should have Free bets, Odds Boost tokens and Private markets available.
    PRECONDITIONS: 2. User should be logged in.
    PRECONDITIONS: In order to expire bpp token:
    PRECONDITIONS: Go to Devtools -> Application -> Local storage -> delete OX.User
    """
    keep_browser_open = True

    def test_001_expire_bpp_token_refresh_the_page_and_check_network_for_user_request(self):
        """
        DESCRIPTION: Expire bpp token, refresh the page and check Network for 'user' request
        EXPECTED: 
        """
        pass

    def test_002_check_user_request(self):
        """
        DESCRIPTION: Check 'user' request
        EXPECTED: Free bets, Odds Boost tokens and Private markets that are available for the user are received in 'user' request after page refresh.
        EXPECTED: * https://{env}.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?channel=MI&returnOffers=Y
        """
        pass
