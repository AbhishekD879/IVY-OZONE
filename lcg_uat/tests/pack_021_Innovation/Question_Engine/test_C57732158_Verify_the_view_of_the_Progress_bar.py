import pytest
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2    # QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732158_Verify_the_view_of_the_Progress_bar(Common):
    """
    TR_ID: C57732158
    NAME: Verify the view of the Progress bar
    DESCRIPTION: This test case verifies the view of the Progress bar.
    PRECONDITIONS: 1. The User is on the Splash page.
    PRECONDITIONS: 2. Tap on the CTA button.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with the created User and Create the QUIZ in CMS
        """
        self.create_question_engine_quiz()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')

    def test_001_tap_on_any_answer(self):
        """
        DESCRIPTION: Tap on any answer.
        EXPECTED: The User is navigated to the next question.
        EXPECTED: The Progress bar is incremented to indicate progress out of the total number of questions available.
        """
        progress_bar = self.site.quiz_home_page.progress_bar.bar_size
        options = list(self.questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()
        wait_for_result(lambda: self.site.quiz_home_page.progress_bar.bar_size != progress_bar)
        self.__class__.new_progress_bar = self.site.quiz_home_page.progress_bar.bar_size
        self.assertTrue(self.new_progress_bar > progress_bar,
                        msg=f'New progress bar: "{self.new_progress_bar}" is same as previous progress bar: "{progress_bar}" but expected increment')
        self.assertTrue(self.questions[1].is_displayed(), msg='User is not navigated to next question')

    def test_002_swipe_left(self):
        """
        DESCRIPTION: Swipe left.
        EXPECTED: The User is navigated to the previous question.
        EXPECTED: The Progress bar is decremented to indicate progress out of the total number of questions available.
        """
        if self.device_type == 'desktop':
            self.site.quiz_home_page.quiz_left_swipe_overlay.click()
            self.assertTrue(self.questions[0].is_displayed(), msg='User is not navigated to the previous question')
            wait_for_result(lambda: self.site.quiz_home_page.progress_bar.bar_size != self.new_progress_bar)
            updated_progress_bar = self.site.quiz_home_page.progress_bar.bar_size
            self.assertTrue(updated_progress_bar < self.new_progress_bar,
                            msg=f'New progress bar: "{updated_progress_bar}" is same as previous progress bar: "{self.new_progress_bar}" but expected decrement')
