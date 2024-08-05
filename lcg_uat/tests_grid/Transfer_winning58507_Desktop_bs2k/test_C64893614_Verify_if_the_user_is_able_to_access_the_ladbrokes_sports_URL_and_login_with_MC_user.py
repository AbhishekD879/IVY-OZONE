import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893614_Verify_if_the_user_is_able_to_access_the_ladbrokes_sports_URL_and_login_with_MC_user(Common):
    """
    TR_ID: C64893614
    NAME: Verify if the user is able to access the ladbrokes sports URL and login with MC user.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid MC username and password.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2click_on_login_button3user_must_enter_the_valid_username_and_password4click_on_loginexpected_result1user_must_be_able_to_access_the_ladbrokes_sports2user_must_be_able_to_click_on_login_button3enter_the_valid_username_and_password4clicking_on_login_user_must_be_able_to_login_as_mc_user(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on login button.
        DESCRIPTION: 3.User must enter the valid username and password.
        DESCRIPTION: 4.Click on login.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.User must be able to access the ladbrokes sports.
        DESCRIPTION: 2.User must be able to click on login button.
        DESCRIPTION: 3.Enter the valid username and password.
        DESCRIPTION: 4.Clicking on login user must be able to login as MC user.
        EXPECTED: 1. 1.User must be able to access the ladbrokes sports.
        EXPECTED: 2.User must be able to click on login button.
        EXPECTED: 3.Enter the valid username and password.
        EXPECTED: 4.Clicking on login user must be able to login as MC user.
        """
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        dialog.username = tests.settings.mc_user
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
