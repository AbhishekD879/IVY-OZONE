import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


# @pytest.mark.tst2 #QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732074_Verify_Swipe_overlay_and_Gesture(Common):
    """
    TR_ID: C57732074
    NAME: Verify Swipe overlay and Gesture
    DESCRIPTION: This test case verifies Swipe overlay and Gesture
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with the created User and Create the QUIZ in CMS
        """
        self.__class__.quiz = self.create_question_engine_quiz()
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - Splash page displayed
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.footer_text, msg=f'footer text is not displayed')
        self.assertTrue(self.site.question_engine.strap_line_text, msg=f'strap line is not displayed')
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.strap_line_text, msg='Splash page failed to open')

    def test_002_tap_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap 'Play now for free' button
        EXPECTED: - Questions page successfully displayed
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        sleep(2)  # to load the questions
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')

    def test_003_tap_on_answer_on_question_1(self):
        """
        DESCRIPTION: Tap on answer on Question 1
        EXPECTED: - User automatically be navigated to Question 2
        EXPECTED: - Swipe overlay with the left / right swipe gesture appear
        EXPECTED: Mobile:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ab19d56351032d23e
        EXPECTED: Tablet:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b4b6c1b60256cb4cdf
        """
        self.__class__.ui_first_question = self.questions[0].question_header.text
        self.__class__.cms_first_question = self.quiz['firstQuestion']['text']
        self.assertEqual(self.ui_first_question, self.cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{self.cms_first_question}" and actual "{self.ui_first_question}"')
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay, msg="Right overlay is not displayed")
        options = list(self.questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()

    def test_004_tap_on_answer_on_question_2(self):
        """
        DESCRIPTION: Tap on answer on Question 2
        EXPECTED: - User automatically be navigated to Question 3
        EXPECTED: - Swipe overlay with the left / right swipe gesture NOT appear
        EXPECTED: (Show once per quiz)
        """
        sleep(4)  # to load the questions
        ui_second_question = self.questions[1].question_header.text
        cms_second_question = self.quiz['firstQuestion']['nextQuestions']['123']['text'].rstrip()
        self.assertEqual(ui_second_question, cms_second_question,
                         msg=f'Quiz second question is incorrect, expected is "{cms_second_question}" and actual "{ui_second_question}"')
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay, msg="Right overlay is not displayed")
        self.assertTrue(self.site.quiz_home_page.quiz_left_swipe_overlay, msg="Right overlay is not displayed")
        options = list(self.questions[1].answer_options.items_as_ordered_dict.values())
        options[0].click()

    def test_005___return_to_question_1_using_swipe_right__tap_on_answer_on_question_1(self):
        """
        DESCRIPTION: - Return to Question 1 using Swipe right
        DESCRIPTION: - Tap on answer on Question 1
        EXPECTED: - User navigated to Question 1
        EXPECTED: - Swipe overlay with the left / right swipe gesture NOT appear
        EXPECTED: (Show once per quiz)
        """
        self.assertTrue(self.site.quiz_home_page.quiz_left_swipe_overlay, msg="Right overlay is not displayed")
        self.site.quiz_home_page.quiz_left_swipe_overlay.click()
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay, msg="Right overlay is not displayed")
        self.assertEqual(self.ui_first_question, self.cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{self.cms_first_question}" and actual "{self.ui_first_question}"')

    def test_006___return_to_question_3_using_swipe_left(self):
        """
        DESCRIPTION: - Return to Question 3 using Swipe left
        EXPECTED: - User navigated to Question 3
        EXPECTED: - Swipe overlay with the left / right swipe gesture NOT appear
        EXPECTED: (Show once per quiz)
        """
        sleep(2)  # to load the questions
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay, msg="Right overlay is not displayed")
        self.site.quiz_home_page.quiz_right_swipe_overlay.click()
        sleep(2)  # to load the questions
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay, msg="Right overlay is not displayed")
        self.site.quiz_home_page.quiz_right_swipe_overlay.click()
        ui_third_question = self.questions[2].question_header.text
        cms_third_question = self.quiz['firstQuestion']['nextQuestions']['123']['nextQuestions']['234']['text'].rstrip()
        self.assertEqual(ui_third_question, cms_third_question,
                         msg=f'Quiz third question is incorrect, expected is "{cms_third_question}" and actual "{ui_third_question}"')
