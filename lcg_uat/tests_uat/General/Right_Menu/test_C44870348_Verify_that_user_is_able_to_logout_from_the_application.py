import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.prod
@pytest.mark.desktop
@vtest
class Test_C44870348_Verify_that_user_is_able_to_logout_from_the_application(Common):
    """
    TR_ID: C44870348
    NAME: Verify that user is able to logout from the application.
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in the application
        """
        self.site.login()

    def test_001_navigate_to_my_accountright_menu_click_on_logout_and_verify(self):
        """
        DESCRIPTION: Navigate to My Account/Right menu, click on Logout and verify.
        EXPECTED: User is logged out from the application, i.e. Login/Join button is displayed.
        """
        self.site.logout()
        self.assertTrue(self.site.header.join_us.is_displayed(),
                        msg=f'"{vec.BMA.JOIN_US}" button is not visible on the screen!')
        self.assertTrue(self.site.header.sign_in.is_displayed(),
                        msg=f'"{vec.Dialogs.DIALOG_MANAGER_LOG_IN}" button is not visible on the screen!')
