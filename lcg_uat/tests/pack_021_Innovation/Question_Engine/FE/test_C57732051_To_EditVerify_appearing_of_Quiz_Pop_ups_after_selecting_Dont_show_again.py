import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2   # QE not configured on tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732051_To_EditVerify_appearing_of_Quiz_Pop_ups_after_selecting_Dont_show_again(Common):
    """
    TR_ID: C57732051
    NAME: [To-Edit]Verify appearing of Quiz Pop-ups after selecting 'Don't show again'
    DESCRIPTION: [To-Edit] - the screenshot needs to be updated
    DESCRIPTION: This test case verifies displaying of Quiz Pop-ups
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. User did not play quiz yet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        self.__class__.quiz = self.create_question_engine_quiz(pop_up=True)
        self.__class__.cms_url = self.quiz[1]['pageUrls'].strip('*')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, async_close_dialogs=False)

    def test_001_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz__pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz > Pop-Ups)
        EXPECTED: - Pop-up appears after [xx] seconds after page fully loads first
        EXPECTED: - Pop-up with buttons:
        EXPECTED: Take quiz
        EXPECTED: Don't show me again
        EXPECTED: Maybe later
        EXPECTED: Texts from CMS displayed and designed:
        EXPECTED: ![](index.php?/attachments/get/36694089)
        """
        self.device.navigate_to(url=f'{tests.HOSTNAME}{self.cms_url}')
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ,
                                                          verify_name=False)
        self.assertTrue(self.dialog, msg='Quiz popup Take quiz Yes button not displayed')
        self.assertTrue(self.dialog.dont_show_again.is_displayed(),
                        msg='Quiz popup dont show me again button not displayed')
        self.assertTrue(self.dialog.remind_me_later.is_displayed(),
                        msg='Quiz popup remind me later button not displayed')
        cms_quiz_pop_text = list(self.quiz)[1]['popupText']
        self.assertEqual(cms_quiz_pop_text, self.dialog.description,
                         msg=f'Quiz popup actual description{self.dialog.description}'
                             f' not as expected {cms_quiz_pop_text} ')

    def test_002_user_select_dont_show_again_on_the_launching_pop_up(self):
        """
        DESCRIPTION: User select 'Don't show agxain' on the launching pop-up
        EXPECTED: - Pop-up should be closed and user redirected to the previous page
        """
        self.dialog.dont_show_again.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ, verify_name=False)
        self.assertFalse(dialog, msg='Quiz popup is displayed for user')
        self.site.wait_content_state("football")

    def test_003_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz__pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz > Pop-Ups)
        EXPECTED: - Pop-up should NOT appear again on the configured page
        """
        self.device.navigate_to(url=f'{tests.HOSTNAME}{self.cms_url}')
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ, verify_name=False)
        self.assertFalse(dialog, msg='Quiz popup is displayed for user after navigating to configured URL')
