import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C31302510_Verify_tapping_Login_Register(Common):
    """
    TR_ID: C31302510
    NAME: Verify tapping Login/Register
    DESCRIPTION: This test case verifies that Login Pop-up is displayed (Can just display both states without generating a mock login pop-up window) when tapping on 'Login/Register' button when user is in logged out state
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. user is not logged in
    """
    keep_browser_open = True

    def test_001_tap_on_loginregister_button(self):
        """
        DESCRIPTION: tap on 'Login/Register' button
        EXPECTED: Login Pop-up is displayed (Can just display both states without generating a mock login pop-up window)
        """
        pass
