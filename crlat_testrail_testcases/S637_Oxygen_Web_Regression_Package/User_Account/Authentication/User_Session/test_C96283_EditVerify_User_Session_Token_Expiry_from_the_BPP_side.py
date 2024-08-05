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
class Test_C96283_EditVerify_User_Session_Token_Expiry_from_the_BPP_side(Common):
    """
    TR_ID: C96283
    NAME: [Edit]Verify User Session Token Expiry from the BPP side
    DESCRIPTION: This test case verifies the user session expiry when 'Not Define' option is set in session limit menu
    PRECONDITIONS: - Make sure that user session limit is set as 'Not Defined'
    PRECONDITIONS: - Expiry time for BPP token is 1 hour. After this time user BPP token should be removed.
    PRECONDITIONS: - For Kibana URL use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Symphony+Infrastructure+creds
    """
    keep_browser_open = True

    def test_001_log_in_with_user_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with user with valid credentials
        EXPECTED: User is logged in
        EXPECTED: User login time is detected
        """
        pass

    def test_002_leave_user_inactive_for_40_min_after_40_min_verify_logs_in_kibana(self):
        """
        DESCRIPTION: Leave user inactive for 40 min. After 40 min verify logs in Kibana
        EXPECTED: Message about Token refresh received
        EXPECTED: ![](index.php?/attachments/get/119597480)
        """
        pass

    def test_003_leave_user_inactive_for_another_20_min_and_verify_logs_after_that(self):
        """
        DESCRIPTION: Leave user inactive for another 20 min and verify logs after that
        EXPECTED: Message about Token removing received
        EXPECTED: ![](index.php?/attachments/get/119597481)
        """
        pass
