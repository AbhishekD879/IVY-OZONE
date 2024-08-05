from time import sleep

import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2   #  QE not configured on tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732103_Verify_the_Quiz_Popup_is_not_displayed_for_the_User_who_has_already_played_a_Quiz(Common):
    """
    TR_ID: C57732103
    NAME: Verify the Quiz Popup is not displayed for the User who has already played a Quiz
    DESCRIPTION: This test case verifies that the Quiz Popup is not displayed for the User who has already played a Quiz.
    PRECONDITIONS: 1. The CMS User has configured the Quiz Popup for a Tennis page.
    PRECONDITIONS: 2. The Quiz Popup is active.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. Open DevTools/Application
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. The CMS User has configured an active Quiz Popup.
        PRECONDITIONS: 2. The User is logged in.
        """
        question_engine = self.create_question_engine_quiz(pop_up=True)
        self.assertTrue(question_engine, msg='Quiz is not configured in the CMS')
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.navigate_to_page('footballsuperseries')

    def test_001_open_a_quiz_page_directly(self):
        """
        DESCRIPTION: Open a Quiz page directly
        EXPECTED: The Quiz is opened
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')

    def test_002_select_any_answer_to_complete_a_quiz(self):
        """
        DESCRIPTION: Select any answer to complete a Quiz.
        EXPECTED: The User has reached the End Page.
        """
        options = list(self.questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(5)
        options = list(self.questions[1].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(5)
        options = list(self.questions[2].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(5)
        options = list(self.questions[3].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(5)
        self.site.quiz_page_popup.submit_button.click()
        sleep(3)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')

    def test_003_open_a_sport_page_which_was_configured_in_the_quiz_popupselect_an_env_which_is_currently_testing_in_the_local_storage(
            self):
        """
        DESCRIPTION: Open a Sport page, which was configured in the Quiz Popup.
        DESCRIPTION: Select an env, which is currently testing, in the local storage.
        EXPECTED: The Quiz Popup is not displayed.
        EXPECTED: The 'qeQuiz' key is not set.
        """
        self.navigate_to_page("/sport/football")
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False)
        self.assertFalse(popup, msg='Quiz popup is displayed for logged out user')
