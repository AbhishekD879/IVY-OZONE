import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.user_account
@pytest.mark.right_hand_menu
@pytest.mark.navigation
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C17995889_Vanilla_Verify_Log_Out_right_menu_option(BaseUserAccountTest):
    """
    TR_ID: C17995889
    NAME: [Vanilla] Verify Log Out right menu option
    DESCRIPTION: This test case is to verify Log Out right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env_and_navigate_to_the_page_other_than_the_home_page(self):
        """
        DESCRIPTION: Log in to test env and navigate to the page other than the home page
        EXPECTED: User is logged in, My Account button appears
        """
        self.site.wait_content_state('HomePage')
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.my_account_button = self.site.header.user_panel.my_account_button
        self.assertTrue(self.my_account_button.is_displayed(),
                        msg='My Account button is not displayed!')

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        self.my_account_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')

    def test_003_clicktap_log_out_menu_option(self):
        """
        DESCRIPTION: Click/tap Log Out menu option
        EXPECTED: Use is logged out and redirected to the home page
        """
        self.site.right_menu.log_out_button.click()
        self.site.wait_content_state('HomePage')
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
