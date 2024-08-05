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
class Test_C44870158_Verify_forgot_password_functionality(Common):
    """
    TR_ID: C44870158
    NAME: Verify forgot password functionality
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application__tap_on_log_in(self):
        """
        DESCRIPTION: Load Application & Tap on 'Log in'
        EXPECTED: Login overlay is loaded with
        EXPECTED: I forgot my username & I forgot my Password options available along with Registration tab.
        """
        pass

    def test_002_tab_on_i_forgot_my_password(self):
        """
        DESCRIPTION: Tab on 'I forgot my Password'
        EXPECTED: Forgot password page is opened & the user is asked to enter the "username" and Submit
        EXPECTED: 'Live chat' & 'Contact us' is present just below submit tab.
        """
        pass

    def test_003_when_the_username_is_entered_and_submitted(self):
        """
        DESCRIPTION: When the username is entered and submitted
        EXPECTED: The user is asked to enter registered email id and DOB and when submitted, a link to reset password is sent to the email.
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
