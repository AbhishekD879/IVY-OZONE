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
class Test_C31302511_Verify_Account_Balance(Common):
    """
    TR_ID: C31302511
    NAME: Verify Account Balance
    DESCRIPTION: This test case verifies 'My Account' button UI WHEN user is in Logged In state
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. user is not logged in
    """
    keep_browser_open = True

    def test_001_log_in_emulate_logged_in_state(self):
        """
        DESCRIPTION: Log in (emulate Logged In state)
        EXPECTED: My Account button is displayed with users Logged In state:
        EXPECTED: Account Balance is shown (based on currency of user account) AND  is presented through Animation as per designs attached:
        EXPECTED: https://jira.egalacoral.com/secure/attachment/1290957/Native-Lads-Header_v1.mp4
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/6348748)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/6348751)
        """
        pass

    def test_002_log_out_emulate_logged_out_state(self):
        """
        DESCRIPTION: Log out (emulate Logged Out state)
        EXPECTED: My Account button is displayed with users Logged out state:
        EXPECTED: 'Login/Register' button within Header is shown as per design (Account Balance or Free Bet Balance is not shown):
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/6348753)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/6348755)
        """
        pass
