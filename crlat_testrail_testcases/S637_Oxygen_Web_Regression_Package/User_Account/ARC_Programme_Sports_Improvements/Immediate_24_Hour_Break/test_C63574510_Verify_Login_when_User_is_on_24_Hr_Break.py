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
class Test_C63574510_Verify_Login_when_User_is_on_24_Hr_Break(Common):
    """
    TR_ID: C63574510
    NAME: Verify Login when User is on 24 Hr Break
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_coral(self):
        """
        DESCRIPTION: Login to Ladbrokes /Coral
        EXPECTED: User should be successfully logged in
        """
        pass

    def test_002_navigate_to_user_account_gt_gambling_control(self):
        """
        DESCRIPTION: Navigate to User Account &gt; Gambling Control
        EXPECTED: User should be navigated to Gambling Controls page
        """
        pass

    def test_003_click_on_the_immediate_24_hr_break_link(self):
        """
        DESCRIPTION: Click on the Immediate 24 Hr Break link
        EXPECTED: User should be displayed
        EXPECTED: "Your account has now been put on Time Out for the next 24 hours"
        EXPECTED: message
        """
        pass

    def test_004_logout_and_re_login(self):
        """
        DESCRIPTION: Logout and Re-login
        EXPECTED: User should not be able to Login
        """
        pass
