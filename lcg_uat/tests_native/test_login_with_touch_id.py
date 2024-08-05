import pytest
from tests.base_test import vtest
from tests_native.native_base_test import NativeBaseTest
from voltron.pages.shared import get_driver


@vtest
# @pytest.mark.android
@pytest.mark.ios
class TestLoginWithTouchFaceId(NativeBaseTest):
    """
    NAME: Login with touch id
    DESCRIPTION: This test case verifies that user is able to login with touch id
    """
    def test_001_log_in(self):
        """
        Log in
        """
        if self.device.platform == 'ios':
            get_driver().toggle_touch_id_enrollment()
            self.oxygen_app.coral_notification_dialog.ok_button.click()
            self.device.accept_allert()
            self.device.accept_allert()

        self.oxygen_app.web_content.login()
        self.device.accept_allert()
        self.oxygen_app.fast_login_pop_up.use_button.click()
        self.oxygen_app.fast_login_confirmed_pop_up.ok_button.click()
        self.oxygen_app.web_content.logout()

        self.oxygen_app.web_content.header.sign_in.click()
        if self.device.platform_version == 12.1:
            self.device.accept_allert()
        get_driver().touch_id(match=True)
        self.oxygen_app.auto_login_pop_up.confirm_button.click()
        self.oxygen_app.fast_login_confirmed_pop_up.ok_button.click()

        self.assertTrue(self.oxygen_app.web_content.wait_logged_in(), msg='User is not logged in')

        self.device.close_app()
        self.device.launch_app()
        self.assertTrue(self.oxygen_app.web_content.wait_logged_in(), msg='User is not logged in')

        self.device.put_app_in_background()
        self.assertTrue(self.oxygen_app.web_content.wait_logged_in(), msg='User is not logged in')
