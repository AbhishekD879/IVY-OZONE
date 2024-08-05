import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C34589248_Verify_that_user_is_able_to_Log_In_only_with_correct_username_password(Common):
    """
    TR_ID: C34589248
    NAME: Verify that user is able to Log In only with correct username/password
    DESCRIPTION: Verify that customers can successfully log in / log out (also check negative scenarios)
    DESCRIPTION: AUTOMATED [C44305379]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_try_to_login_with_a_wrong_username_eg_try_a_weird_combination_of_characters_so_the_username_does_not_exist(self):
        """
        DESCRIPTION: Try to login with a wrong username (e.g. try a weird combination of characters so the username does not exist)
        EXPECTED: Error 'The credentials entered are incorrect' is displayed
        """
        pass

    def test_002_try_to_login_with_a_correct_username_but_wrong_password(self):
        """
        DESCRIPTION: Try to login with a correct username but wrong password
        EXPECTED: Error 'The credentials entered are incorrect' is displayed
        """
        pass

    def test_003_try_to_login_with_correct_username_and_password(self):
        """
        DESCRIPTION: Try to login with correct username and password
        EXPECTED: The customer is successfully logged in. Balance is displayed
        """
        pass

    def test_004_click_on_menu___logout(self):
        """
        DESCRIPTION: Click on Menu -> Logout
        EXPECTED: The customer is logged out
        """
        pass
