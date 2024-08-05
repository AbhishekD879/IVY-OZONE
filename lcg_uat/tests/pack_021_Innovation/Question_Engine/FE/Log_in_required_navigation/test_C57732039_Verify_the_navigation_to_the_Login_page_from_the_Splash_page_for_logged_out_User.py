import pytest
import tests
from voltron.environments import constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2   # question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732039_Verify_the_navigation_to_the_Login_page_from_the_Splash_page_for_logged_out_User(Common):
    """
    TR_ID: C57732039
    NAME: Verify the navigation to the Login page from the Splash page for logged out User
    DESCRIPTION: This test case verifies the navigation to the Login page from the Splash page for logged out User.
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to view' (the 'START' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    """
    keep_browser_open = True

    def test_001_tap_on_the_cta_to_start_the_quiz_log_in_to_play_for_free(self):
        """
        DESCRIPTION: Tap on the CTA to start the quiz (Log in to Play for free).
        EXPECTED: The Login pop-up is opened.
        """
        splash_pages = self.cms_config.get_qe_splash_page()
        self.__class__.splash_page = next(
            (page for page in splash_pages if page.get('title') == "Autotest_Splash_Page"))
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.navigate_to_page('footballsuperseries')

    def test_002_enter_valid_credentials(self):
        """
        DESCRIPTION: Enter valid credentials.
        EXPECTED: The existing 'After log in' pop-ups are displayed (Odds Boost/Quick Deposit).
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        dialog.username = self.username
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')

    def test_003_tap_on_the_x__okthanks_buttons(self):
        """
        DESCRIPTION: Tap on the 'X' / 'OK,Thanks' buttons.
        EXPECTED: The starting Splash page is displayed.
        """
        sleep(5)
        if self.site.root_app.has_timeline_overlay_tutorial(timeout=10, expected_result=True):
            self.site.timeline_tutorial_overlay.close_icon.click()
        self.assertEqual(self.site.question_engine.strap_line_text, self.splash_page['strapLine'],
                         msg=f'Actual strap line text text : "{self.site.question_engine.strap_line_text}"'
                             f'is not as expected : "{self.splash_page["strapLine"]}"')
        self.assertEqual(self.site.question_engine.footer_text, self.splash_page['footerText'],
                         msg=f'Actual footer text text : "{self.site.question_engine.footer_text}"'
                             f'is not as expected : "{self.splash_page["footerText"]}"')
        sleep(3)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg='"Play now for free" button is not displayed')
        actual_playnowforfree_button = self.site.question_engine.cta_button.text
        self.assertEqual(actual_playnowforfree_button, self.splash_page['playForFreeCTAText'],
                         msg=f'Actual "Play now for free" button text : "{actual_playnowforfree_button}"'
                             f'is not as expected : "{self.splash_page["playForFreeCTAText"]}"')
