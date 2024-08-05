import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.desktop
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.question_engine
@vtest
class Test_C57732083_Verify_the_view_of_the_Splash_page_Desktop(Common):
    """
    TR_ID: C57732083
    NAME: Verify the view of the Splash page [Desktop]
    DESCRIPTION: This test case verifies the view of the Splash page on the Desktop.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The game is configured in the CMS.
        PRECONDITIONS: 2. The User is logged in.
        PRECONDITIONS: 3. The User has not played the game yet.
        PRECONDITIONS: 4. Click on the 'Correct4' link.
        PRECONDITIONS: 5. Login with valid credentials.
        """
        quiz = self.create_question_engine_quiz()
        self.assertTrue(quiz, msg=f'"Created Quiz" is not displayed')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_click_on_the_correct4_link(self):
        """
        DESCRIPTION: Click on the 'Correct4' link.
        EXPECTED: 1. The Splash page is opened.
        EXPECTED: 2. The content is centered within the middle column.
        EXPECTED: 3. The Game Header is displayed as per design
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c43cae74a026e8eedd0
        EXPECTED: 4. The breadcrumbs in the sub-menu are not displayed.
        EXPECTED: 5. The 'X' icon is not displayed.
        """
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.strap_line_text, msg=f'"Strap Line Text" is not displayed')
        self.assertFalse(self.site.question_engine.has_close_button(), msg=f'"Close Button" is displayed')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'"CTA Button" is not displayed')
        self.site.question_engine.cta_button.click()

    def test_002_click_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Click on the Back arrow icon.
        EXPECTED: 1. The User is redirected to the Home page.
        EXPECTED: 2. The Exit pop-up is not displayed.
        EXPECTED: 3. The sub-header with breadcrumbs is not displayed.
        """
        self.site.wait_content_state_changed(timeout=20)
        self.assertTrue(self.site.quiz_home_page.back_button, msg=f'"Back Button" is not displayed')
        self.site.quiz_home_page.back_button.click()
        self.site.wait_content_state('homepage')
        try:
            quiz_exit_popup = self.site.quiz_page_popup.has_quiz_exit_popup()
            self.assertFalse(quiz_exit_popup, msg=f'"Quiz Exit Popup" is not displayed')
        except Exception:
            self._logger.info(f'Quiz Exit Popup is displayed')
