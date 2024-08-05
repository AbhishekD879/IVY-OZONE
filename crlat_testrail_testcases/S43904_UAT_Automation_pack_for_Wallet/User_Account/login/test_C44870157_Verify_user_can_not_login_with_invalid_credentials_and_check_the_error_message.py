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
class Test_C44870157_Verify_user_can_not_login_with_invalid_credentials_and_check_the_error_message(Common):
    """
    TR_ID: C44870157
    NAME: Verify user can not login with invalid credentials and check the error message.
    DESCRIPTION: 
    PRECONDITIONS: Launch the app
    PRECONDITIONS: Login with the invalid credentials
    """
    keep_browser_open = True

    def test_001_try_to_login_with_a_wrong_username_eg_try_a_weird_combination_of_characters_so_the_username_does_not_exist(self):
        """
        DESCRIPTION: Try to login with a wrong username (e.g. try a weird combination of characters so the username does not exist)
        EXPECTED: Error message is displayed
        """
        pass

    def test_002_try_to_login_with_a_correct_username_but_wrong_password(self):
        """
        DESCRIPTION: Try to login with a correct username but wrong password
        EXPECTED: Error message is displayed
        """
        pass

    def test_003_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
