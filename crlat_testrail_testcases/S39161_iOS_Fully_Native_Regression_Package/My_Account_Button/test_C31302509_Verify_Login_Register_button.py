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
class Test_C31302509_Verify_Login_Register_button(Common):
    """
    TR_ID: C31302509
    NAME: Verify 'Login/Register' button
    DESCRIPTION: This test case verifies UI of 'My Account' button WHEN user is in Logged Out state.
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. user is not logged in
    """
    keep_browser_open = True

    def test_001_verify_my_account_button_ui(self):
        """
        DESCRIPTION: Verify 'My Account' button UI
        EXPECTED: My account button displays users Logged Out state:
        EXPECTED: 'Login/Register' button within Header is displayed as per design (Account Balance or Free Bet Balance is not displayed):
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/6348722)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/6348723)
        """
        pass
