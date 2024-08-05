import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.js_functions import click


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_hl
@pytest.mark.crl_prod
@pytest.mark.mobile_only
@pytest.mark.popup
@pytest.mark.tutorial_overlay
@pytest.mark.user_account
@pytest.mark.cookies
@pytest.mark.medium
@pytest.mark.local_storage
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-35413')
@pytest.mark.navigation
@vtest
class Test_C28235_Homepage_Tutorial_Overlay_displaying_for_user_after_login_to_application(BaseUserAccountTest):
    """
    TR_ID: C28235
    NAME: Homepage Tutorial Overlay displaying for user after login to application
    DESCRIPTION: This test case verifies Homepage Tutorial Overlay displaying after user's login to application
    DESCRIPTION: AUTOTEST [C2593985]
    """
    keep_browser_open = True
    zero_balance_username = None
    _ls_cookies = None

    def close_login_pop_ups(self):
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, timeout=5)
        if dialog:
            # click using js is added to avoid interaction with unexpected Freebet dialog
            click(dialog.header_object.close_button._we)
            dialog.wait_dialog_closed()

        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=5)
        if dialog:
            # click using js is added to avoid interaction with unexpected odds boost dialog
            click(dialog.header_object.close_button._we)
            dialog.wait_dialog_closed()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: **JIRA tickets:**
        PRECONDITIONS: - BMA-7029 Homepage Tutorial Overlay
        PRECONDITIONS: - BMA-16264 Cookie Banner :- Football tutorial displaying when cookie banner message is shown
        PRECONDITIONS: Information that Homepage Tutorial Overlay was shown is saved in Local Storage: name - OX.tutorial, value - true. Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
        PRECONDITIONS: ![](index.php?/attachments/get/1227)
        """
        self.__class__.cookie_name = 'OX.tutorial'
        self.__class__.cookie_name_football = 'OX.footballTutorial'
        self.__class__.default_username = tests.settings.betplacement_user
        self.__class__.default_password = tests.settings.default_password
        self.__class__.zero_balance_username = self.generate_user()
        self.gvc_wallet_user_client.register_new_user(username=self.zero_balance_username)
        self.site.wait_content_state(state_name='Homepage')

    def test_001_clear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.device.driver.implicitly_wait(5)

    def test_002_do_not_login_to_application_and_go_to_the_homepage(self):
        """
        DESCRIPTION: Do not login to application and go to the Homepage
        EXPECTED: Homepage is displayed without Homepage Tutorial Overlay
        """
        self.site.wait_content_state('Homepage')
        self.assertFalse(self.site.tutorial_overlay, msg='Tutorial overlay is shown for not logged user')

    def test_003_login_to_application_with_already_existing_user(self):
        """
        DESCRIPTION: Login to application with already existing user
        EXPECTED: - Homepage is displayed with Homepage Tutorial Overlay
        EXPECTED: - Homepage Tutorial Overlay is displayed under Cookie Banner if its present
        EXPECTED: - Homepage Tutorial Overlay is scrollable on devices with small screen resolution when Cookie Banner is present
        """
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='Login dialog is not present on page')
        self._logger.info('*** Trying to login with user %s' % self.default_username)
        dialog.username = self.default_username
        dialog.password = self.default_password
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed(timeout=15)
        self.assertTrue(dialog_closed, msg='User is not logged in as Login Dialog was not closed')

        self.assertTrue(self.site.wait_for_tutorial_overlay(), msg='Tutorial overlay is not shown')

    def test_004_tap_close_button(self):
        """
        DESCRIPTION: Tap 'Close' button
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   User stays on the Homepage
        EXPECTED: *   'OX.tutorial: True' cookie is added to Local Storage
        """
        self.site.tutorial_overlay.text_panel.close_button.click()
        self.assertFalse(self.site.wait_for_tutorial_overlay(expected_result=False),
                         msg='Tutorial overlay is not closed')
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self.assertTrue(cookie, msg="'OX.tutorial: True' cookie is not added to Local Storage")

    def test_005_repeat_steps_1_and_3tap_my_betsbalancemy_accountbetslip_button(self):
        """
        DESCRIPTION: Repeat steps 1 and 3
        DESCRIPTION: Tap 'My Bets'/Balance/'My Account'/'Betslip' button
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   Appropriate page is opened e.g. My Bets/Balance/Betslip
        EXPECTED: *   'OX.tutorial: True' cookie is added to Local Storage
        """
        self.test_001_clear_browser_cookies_and_load_oxygen_application()
        self.test_003_login_to_application_with_already_existing_user()

        self.site.tutorial_overlay.text_panel.close_button.click()
        self.assertFalse(self.site.wait_for_tutorial_overlay(expected_result=False),
                         msg='Tutorial overlay is not closed')
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self.assertTrue(cookie, msg="'OX.tutorial: True' cookie is not added to Local Storage")

        self.close_login_pop_ups()
        self.site.open_my_bets_cashout()
        self.assertFalse(self.site.wait_for_tutorial_overlay(expected_result=False),
                         msg='Tutorial overlay is not closed')
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self.assertTrue(cookie, msg="'OX.tutorial: True' cookie is not added to Local Storage")

    def test_006_repeat_steps_1_and_3and_change_url_eg_football(self):
        """
        DESCRIPTION: Repeat steps 1 and 3
        DESCRIPTION: and change URL e.g. football
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   User is navigated to appropriate page
        """
        self.test_001_clear_browser_cookies_and_load_oxygen_application()
        self.test_003_login_to_application_with_already_existing_user()
        self.close_login_pop_ups()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        self.assertFalse(self.site.wait_for_tutorial_overlay(expected_result=False),
                         msg='Tutorial overlay is not closed')
        # BMA-35413
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name_football)
        self.assertTrue(cookie, msg="'OX.tutorial: True' cookie is not added to Local Storage")

    def test_007_clear_browser_cookies_and_login_with_any_user_that_will_have_to_interact_with_pop_up_after_successful_logineg_user_with_000_balance_user_that_increased_deposit_limits_and_has_to_confirm_this_action__user_that_needs_to_pass_netverify_procedure_user_with_freebets_etc(self):
        """
        DESCRIPTION: Clear browser cookies and login with any user that will have to interact with Pop-up after successful login
        DESCRIPTION: (e.g. user with '0.00' balance, user that increased deposit limits and has to confirm this action,  user that needs to pass NetVerify procedure, user with freebets, etc.)
        EXPECTED: *   User is redirected to the Homepage
        EXPECTED: *   Homepage Tutorial Overlay is displayed
        """
        self.__class__.default_username = self.zero_balance_username
        self.test_001_clear_browser_cookies_and_load_oxygen_application()
        self.test_003_login_to_application_with_already_existing_user()

    def test_008_close_homepage_tutorial_overlay(self):
        """
        DESCRIPTION: Close Homepage Tutorial Overlay
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   Appropriate Pop-up messages are displayed one by one after closing the Overlay
        EXPECTED: *   User stays on the Homepage
        EXPECTED: *   'OX.tutorial: True' cookie is added to Local Storage
        """
        self.test_004_tap_close_button()
        self.close_login_pop_ups()
