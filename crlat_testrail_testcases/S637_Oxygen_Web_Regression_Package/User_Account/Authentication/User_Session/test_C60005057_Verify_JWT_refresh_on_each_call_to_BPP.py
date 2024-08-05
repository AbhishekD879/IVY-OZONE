import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C60005057_Verify_JWT_refresh_on_each_call_to_BPP(Common):
    """
    TR_ID: C60005057
    NAME: Verify JWT refresh on each call to BPP
    DESCRIPTION: Bpp token is valid 1 hour.
    DESCRIPTION: In order to not relogin user in every hour, we refresh token on each call to BPP, so that user can execute requests to BPP for an hour since *last request to BPP*.
    DESCRIPTION: UI is going to place that token in Local Storage.
    PRECONDITIONS: 401 error - Unauthorized Access
    """
    keep_browser_open = True

    def test_001_navigate_to_the_app_and_login(self):
        """
        DESCRIPTION: Navigate to the app and login
        EXPECTED: 
        """
        pass

    def test_002__wait_40_min_place_a_bet(self):
        """
        DESCRIPTION: * Wait 40 min
        DESCRIPTION: * Place a bet
        EXPECTED: * New action to BPP is made
        EXPECTED: * Token is refreshed
        """
        pass

    def test_003__wait_30_min_more_together_its_1hour_and_10min_verify_if_user_is_logged_out(self):
        """
        DESCRIPTION: * Wait 30 min more (together it`s 1hour and 10min)
        DESCRIPTION: * Verify if user is logged out
        EXPECTED: * User is Not logged out
        EXPECTED: * 401 error is Not available
        """
        pass

    def test_004_place_a_bet(self):
        """
        DESCRIPTION: Place a bet
        EXPECTED: * User is logged in
        EXPECTED: * Bet is placed successfully
        """
        pass
