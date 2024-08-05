import pytest

from time import sleep
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


# @pytest.mark.tst2 # question enginee not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732071_Verify_view_and_data_of_Exit_pop_up(Common):
    """
    TR_ID: C57732071
    NAME: Verify view and data of Exit pop-up
    DESCRIPTION: This test case verifies view and data on 'Splash' page
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cls.question['exitPopup']['description'] = "Leaving the quiz now will mean your answers will not be submitted"
        cms_config.update_question_engine_quiz(quiz_id=cls.quiz_id, title=cls.title, payload=cls.question)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The game is configured in the CMS.
        PRECONDITIONS: 2. The User is logged in.
        PRECONDITIONS: 3. User opens previously created Quiz
        PRECONDITIONS: 4. Content for Splash page configured before
        PRECONDITIONS: 5. User haven't played the current game yet
        """
        splash_pages = self.cms_config.get_qe_splash_page()
        self.__class__.splash_page = next((page for page in splash_pages if page.get('title') == "Autotest_Splash_Page"))
        self.__class__.question = self.create_question_engine_quiz()
        self.__class__.expected_first_question = self.question['firstQuestion']['text']
        self.__class__.quiz_id = self.question['id']
        self.__class__.title = self.question['title']
        self.__class__.exitpopup_desc = self.question['exitPopup']['description']
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('footballsuperseries')

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - Splash page displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        self.assertEqual(self.site.question_engine.strap_line_text, self.splash_page['strapLine'],
                         msg=f'Actual strap line text text : "{self.site.question_engine.strap_line_text}"'
                             f'is not as expected : "{ self.splash_page["strapLine"]}"')
        self.assertEqual(self.site.question_engine.footer_text, self.splash_page['footerText'],
                         msg=f'Actual footer text text : "{self.site.question_engine.footer_text}"'
                             f'is not as expected : "{self.splash_page["footerText"]}"')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg='"Play now for free" button is not displayed')

    def test_002_tap_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap 'Play now for free' button
        EXPECTED: - Questions page successfully displayed
        """
        actual_playnowforfree_button = self.site.question_engine.cta_button.text
        self.assertEqual(actual_playnowforfree_button, self.splash_page['playForFreeCTAText'],
                         msg=f'Actual "Play now for free" button text : "{actual_playnowforfree_button}"'
                             f'is not as expected : "{self.splash_page["playForFreeCTAText"]}"')
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg='Questions are not displayed')
        actual_first_question = questions[0].question_header.text
        self.assertEqual(actual_first_question, self.expected_first_question,
                         msg=f'Actual first question: "{actual_first_question}"'
                             f'is not as expected first question: "{self.expected_first_question}"')

    def test_003_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: - Exit pop-up displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d96291db0449b1282fc49
        EXPECTED: ![](index.php?/attachments/get/3050962)
        """
        self.assertTrue(self.site.question_engine.quick_links_page.has_back_button(),
                        msg=f'"Back Button" is not displayed')
        self.site.question_engine.quick_links_page.back_button.click()
        self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(expected_result=True),
                        msg='Exit pop-up is not displayed')

    def test_004_make_changes_to_each_field_on_cms__question_enginee__quiz__activequiz__pupups_tab__save_changes(
            self):
        """
        DESCRIPTION: - Make changes to each field on CMS > Question Enginee > Quiz > [activequiz] > Pupups Tab
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        self.question['exitPopup']['description'] = 'updated ' + self.exitpopup_desc
        self.cms_config.update_question_engine_quiz(quiz_id=self.quiz_id, title=self.title, payload=self.question)

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(wait=20),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_005_open_questions_page_again__tap_back_button_again(self):
        """
        DESCRIPTION: - Open 'Questions' page again
        DESCRIPTION: - Tap 'Back' button again
        EXPECTED: - All data retrieved from CMS to Exit pop-up and correctly displayed
        EXPECTED: - All successfully styled
        """
        self.navigate_to_page('footballsuperseries')
        actual_playnowforfree_button = self.site.question_engine.cta_button.text
        self.assertEqual(actual_playnowforfree_button, self.splash_page['playForFreeCTAText'],
                         msg=f'Actual "Play now for free" button text : "{actual_playnowforfree_button}"'
                             f'is not as expected : "{self.splash_page["playForFreeCTAText"]}"')
        self.site.question_engine.cta_button.click()
        self.test_003_tap_back_button()
        desc = self.site.quiz_page_popup.exit_quiz_popup.exit_popup_desc
        self.assertEqual(desc, 'updated ' + self.exitpopup_desc, msg=f'Actual exit popup description {desc} is '
                                                                     f'not matching with expected {"updated " + self.exitpopup_desc}')

    def test_006_tap_on_keep_playing_button(self):
        """
        DESCRIPTION: Tap on 'Keep playing' button
        EXPECTED: User returns to the currently opened question
        """
        self.site.quiz_page_popup.exit_quiz_popup.keep_playing_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg='Questions are not displayed')
        actual_first_question = questions[0].question_header.text
        self.assertEqual(actual_first_question, self.expected_first_question,
                         msg=f'Actual first question: "{actual_first_question}"'
                             f'is not as expected first question: "{self.expected_first_question}"')

    def test_007_move_to_another_question__tap_back_button_again(self):
        """
        DESCRIPTION: - Move to another question
        DESCRIPTION: - Tap 'Back' button again
        EXPECTED: - Exit pop-up displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d96291db0449b1282fc49
        EXPECTED: ![](index.php?/attachments/get/3050962)
        """
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        options = list(questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(5)
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        ui_second_question = questions[1].question_header.text
        cms_second_question = self.question['firstQuestion']['nextQuestions']['123']['text'].rstrip()
        self.assertEqual(ui_second_question, cms_second_question,
                         msg=f'Quiz second question is incorrect, expected is "{cms_second_question}" and actual "{ui_second_question}"')
        self.site.contents.scroll_to_top()
        self.site.question_engine.quick_links_page.back_button.click()
        self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(expected_result=True),
                        msg='Exit pop-up is not displayed')

    def test_008_tap_on_exit_game_button(self):
        """
        DESCRIPTION: Tap on 'Exit game' button
        EXPECTED: User returned to the 'Splash' page
        """
        self.site.quiz_page_popup.exit_quiz_popup.leave_button.click()
        self.site.wait_content_state(state_name='Homepage')
