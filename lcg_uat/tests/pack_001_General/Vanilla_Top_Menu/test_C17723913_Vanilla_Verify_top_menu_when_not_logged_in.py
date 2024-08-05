import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.top_menu
@vtest
class Test_C17723913_Vanilla_Verify_top_menu_when_not_logged_in(Common):
    """
    TR_ID: C17723913
    NAME: [Vanilla] Verify top menu when not logged in
    DESCRIPTION: This test case is to verify top menu options when user is not logged in
    """
    keep_browser_open = True

    def test_001_verify_the_top_menu_when_not_logged_in(self):
        """
        DESCRIPTION: Verify the top menu when not logged in:
        EXPECTED: Top menu contains following menu options:
        EXPECTED: - Join
        EXPECTED: - Login
        """
        self.site.wait_content_state(state_name='HomePage')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Top menu does not contain "Login" option')
        self.assertTrue(self.site.header.join_us.is_displayed(), msg='Top menu does not contain "Join" option')

    def test_002_click_join_button(self):
        """
        DESCRIPTION: Click/Tap Join button
        EXPECTED: Registration form is displayed on the first step.
        """
        self.site.header.join_us.click()
        # We Need To Wait For Registration To Load Before Proceeding With Three Step Registration
        wait_for_result(lambda: self.device.driver.execute_script("document.readyState;") == "complete", timeout=20)
        self.assertTrue(self.site.three_steps_registration.is_displayed(timeout=5),
                        msg='"Registration" form is not opened')

    def test_003_close_join_form_and_click_login_button(self):
        """
        DESCRIPTION: Close Join form and click/tap Login button
        EXPECTED: Login form is opened.
        """
        self.site.three_steps_registration.header.close_button.click()
        self.site.wait_content_state(state_name='HomePage')
        self.site.header.sign_in.click()
        login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(login_dialog, msg='"Login" form is not opened')
