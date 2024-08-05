import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


# @pytest.mark.tst2  #question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732085_Verify_the_view_of_the_Question_page_Desktop(Common):
    """
    TR_ID: C57732085
    NAME: Verify the view of the Question page [Desktop]
    DESCRIPTION: This test case verifies the view of the Question page on the Desktop.
    PRECONDITIONS: 1. The game is configured in the CMS.
    PRECONDITIONS: 2. The User is logged in.
    PRECONDITIONS: 3. The User has not played the game yet.
    PRECONDITIONS: 4. Click on the 'Correct4' link.
    PRECONDITIONS: 5. Login with valid credentials.
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
        self.__class__.quiz = self.create_question_engine_quiz()
        self.assertTrue(self.quiz, msg='Quiz is not present')
        source_page_url = self.quiz['sourceId']
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(user_name=user_name)
        self.navigate_to_page(name=source_page_url)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')

    def test_001_click_on_the_cta_to_start_a_game(self):
        """
        DESCRIPTION: Click on the CTA to start a game.
        EXPECTED: 1. The first question page is displayed with the CMS content.
        EXPECTED: 2. The Back arrow in the top left corner is not displayed.
        EXPECTED: 3. The Next arrow button is disabled.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        EXPECTED: 5. The blue background container is displayed to the end of the page as on the screenshot
        EXPECTED: https://files.slack.com/files-pri/T383TLAQG-FQNDP7CTG/screenshot_2019-11-15_at_16.17.14.png
        """
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg='Quiz question are not displayed')
        self.__class__.ui_first_question = self.questions[0].question_header.text
        self.__class__.cms_first_question = self.quiz['firstQuestion']['text']
        self.assertEqual(self.ui_first_question, self.cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{self.cms_first_question}" and actual "{self.ui_first_question}"')
        self.assertTrue(self.site.quiz_home_page.has_quiz_right_swipe_inactive(), msg=f'next link is not disabled')

    def test_002_click_on_the_exit_button(self):
        """
        DESCRIPTION: Click on the 'Exit' button.
        EXPECTED: 1. The Exit pop-up is opened with:
        EXPECTED: - 'Keep playing' button
        EXPECTED: - 'Exit game' button.
        EXPECTED: 2. The sub-header with breadcrumbs is not displayed. https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c42bb3cda171b2ee259
        """
        self.site.question_engine.exit_button.click()
        self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(), msg=f'exit popup is not displayed')

    def test_003_click_on_the_keep_playing_button(self):
        """
        DESCRIPTION: Click on the 'Keep playing' button.
        EXPECTED: 1. The Exit pop-up is closed.
        EXPECTED: 2. The first question page is displayed with the CMS content.
        EXPECTED: 3. The Back arrow in the top left corner is not displayed.
        EXPECTED: 4. The Next arrow button is disabled.
        EXPECTED: 5. The sub-header with breadcrumbs is not displayed.
        """
        self.site.quiz_page_popup.exit_quiz_popup.keep_playing_button.click()
        self.assertTrue(self.site.question_engine.has_exit_link(), msg=f'"Quiz Exit Popup" is displayed')
        self.assertEqual(self.ui_first_question, self.cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{self.cms_first_question}" and actual "{self.ui_first_question}"')
        self.assertTrue(self.site.quiz_home_page.has_quiz_right_swipe_inactive(), msg=f'next link is not disabled')

    def test_004_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: 1. The Next arrow button is activated.
        EXPECTED: 2. The User is auto-navigated to the next question after 2 sec delay.
        EXPECTED: 3. The Previous arrow button is activated.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        """
        self.questions[0].click()
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay.is_enabled(),
                        msg=f'next  button is not clickable')
        sleep(5)
        list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        ui_second_question = self.questions[1].question_header.text
        cms_second_question = self.quiz['firstQuestion']['nextQuestions']['123']['text'].rstrip()
        self.assertEqual(ui_second_question, cms_second_question,
                         msg=f'Quiz second question is incorrect, expected is "{cms_second_question}" and actual "{ui_second_question}"')
        self.assertTrue(self.site.quiz_home_page.quiz_left_swipe_overlay.is_enabled(),
                        msg=f'previous button is not clickable')

    def test_005_click_on_the_previous_arrow_button(self):
        """
        DESCRIPTION: Click on the Previous arrow button.
        EXPECTED: 1. The User is redirected to the first question page.
        EXPECTED: 2. The previously selected answer is highlighted with yellow colour.
        EXPECTED: 3. The Next arrow button is activated.
        EXPECTED: 4. The Previous arrow button is not displayed.
        EXPECTED: 5. The sub-header with breadcrumbs is not displayed.
        """
        self.site.quiz_home_page.quiz_left_swipe_overlay.click()
        self.assertEqual(self.ui_first_question, self.cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{self.cms_first_question}" and actual "{self.ui_first_question}"')
        self.assertTrue(self.site.quiz_home_page.quiz_right_swipe_overlay.is_enabled(),
                        msg=f'next  button is not clickable')
        self.assertEquals(self.questions[0].background_color_value, vec.colors.QE_ANSWER_BACKGROUND_COLOR,
                          msg=f'Actual items: "{self.questions[0].background_color_value}"is not same as '
                              f'Expected items: "{vec.colors.QE_ANSWER_BACKGROUND_COLOR}"')

    def test_006_click_on_the_next_arrow_button(self):
        """
        DESCRIPTION: Click on the Next arrow button.
        EXPECTED: 1. The User is redirected to the second question page.
        EXPECTED: 2. The Previous arrow button is activated.
        EXPECTED: 3. The Next arrow button is disabled until the current question is not answered yet.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        """
        self.site.quiz_home_page.quiz_right_swipe_overlay.click()
        sleep(2)
        list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        sleep(3)
        ui_second_question = self.questions[1].question_header.text
        cms_second_question = self.quiz['firstQuestion']['nextQuestions']['123']['text'].rstrip()
        self.assertEqual(ui_second_question, cms_second_question,
                         msg=f'Quiz second question is incorrect, expected is "{cms_second_question}" and actual "{ui_second_question}"')
        self.assertTrue(self.site.quiz_home_page.quiz_left_swipe_overlay.is_enabled(),
                        msg=f'previous button is not clickable')

    def test_007_select_any_answer_to_reach_the_last_question(self):
        """
        DESCRIPTION: Select any answer to reach the last question.
        EXPECTED: 1. The User is redirected to the last question page.
        EXPECTED: 2. The Previous arrow button is activated.
        EXPECTED: 3. The Next arrow button is not displayed.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        """
        sleep(2)
        options = list(self.questions[1].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(4)
        options = list(self.questions[2].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(4)
        self.assertTrue(self.site.quiz_home_page.quiz_left_swipe_overlay.is_enabled(),
                        msg=f'previous button is not clickable')

    def test_008_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: 1. The Submit pop-up is opened with:
        EXPECTED: - 'Submit' CTA button;
        EXPECTED: - 'Go back and edit' CTA button.
        EXPECTED: 2. The sub-header with breadcrumbs is not displayed. https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c423a69a102934ab917
        """
        options = list(self.questions[3].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(3)
        self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(), msg=f'submit popup is not displayed')
        self.assertTrue(self.site.quiz_page_popup.has_submit_button(), msg='submit button is not displayed')

    def test_009_click_on_the_go_back_and_edit_button(self):
        """
        DESCRIPTION: Click on the 'Go back and edit' button.
        EXPECTED: 1. The User is auto-navigated to the first question page.
        EXPECTED: 2. The Next arrow button is activated.
        EXPECTED: 3. The previously selected answer is highlighted with yellow colour.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        EXPECTED: 5. The swipe gesture tutorial is not displayed.
        """
        self.site.quiz_page_popup.go_back_edit_button.click()
        sleep(5)
        self.assertEqual(self.ui_first_question, self.cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{self.cms_first_question}" and actual "{self.ui_first_question}"')
        self.assertEquals(self.questions[0].background_color_value, vec.colors.QE_ANSWER_BACKGROUND_COLOR,
                          msg=f'Actual items: "{self.questions[0].background_color_value}"is not same as '
                              f'Expected items: "{vec.colors.QE_ANSWER_BACKGROUND_COLOR}"')

    def test_010_edit_the_answers_and_proceed_to_the_last_question_page(self):
        """
        DESCRIPTION: Edit the answers and proceed to the last question page.
        EXPECTED: 1. The User is auto-navigated to the next question.
        EXPECTED: 2. The Next and Previous arrow buttons are activated.
        EXPECTED: 3. The sub-header with breadcrumbs is not displayed.
        """

        for question in self.questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            sleep(2)
            options[1].click()
            sleep(5)  # time required to swipe to next question
            self.site.wait_splash_to_hide(timeout=10)

    def test_011_click_on_the_submit_button(self):
        """
        DESCRIPTION: Click on the 'Submit' button.
        EXPECTED: 1. The end page is displayed showing the CMS content as per designs.
        EXPECTED: 2. The content is centered. https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c424447d165903a0bd5
        """
        self.site.quiz_home_page.submit.click()
        sleep(3)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')
