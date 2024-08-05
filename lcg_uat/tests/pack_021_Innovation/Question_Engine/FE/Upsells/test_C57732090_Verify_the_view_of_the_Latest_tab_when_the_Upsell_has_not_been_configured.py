import pytest
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2 #question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732090_Verify_the_view_of_the_Latest_tab_when_the_Upsell_has_not_been_configured(Common):
    """
    TR_ID: C57732090
    NAME: Verify the view of the Latest tab  when the Upsell has not been configured
    DESCRIPTION: This test case verifies the view of the Latest tab  when the Upsell has not been configured
    PRECONDITIONS: 1. The Upsell has not been configured in the CMS or the 'Show Upsell' toggle is off in the End page configuration.
    PRECONDITIONS: 2. The current Event has not started yet.
    PRECONDITIONS: 3. The Quiz is configured in the CMS.
    PRECONDITIONS: 4. The User is logged in.
    PRECONDITIONS: 5. The User has not played a Quiz yet.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The Upsell has not been configured in the CMS or the 'Show Upsell' toggle is off in the End page configuration.
        PRECONDITIONS: 2. The current Event has not started yet.
        PRECONDITIONS: 3. The Quiz is configured in the CMS.
        PRECONDITIONS: 4. The User is logged in.
        PRECONDITIONS: 5. The User has not played a Quiz yet.
        """
        question = self.create_question_engine_quiz()
        self.__class__.expected_first_question = question['firstQuestion']['text']
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.__class__.expected_first_question = question['firstQuestion']['text']
        self.navigate_to_page('footballsuperseries')

    def test_001_tap_on_the_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap on the 'Play Now For Free' button.
        EXPECTED: The User is redirected to the 1st Question page.
        """
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg='Questions are not displayed')
        actual_first_question = self.questions[0].question_header.text
        self.assertEqual(actual_first_question, self.expected_first_question,
                         msg=f'Actual first question: "{actual_first_question}"'
                             f'is not as expected first question: "{self.expected_first_question}"')

    def test_002_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the next Question page.
        """
        for question in self.questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[1].click()
            sleep(4)  # time required to swipe to next question
            self.site.wait_splash_to_hide(timeout=10)
            self.assertEquals(self.questions[0].background_color_value, vec.colors.QE_ANSWER_BACKGROUND_COLOR,
                              msg=f'Actual items: "{self.questions[0].background_color_value}"is not same as '
                                  f'Expected items: "{vec.colors.QE_ANSWER_BACKGROUND_COLOR}"')

    def test_003_repeat_the_2nd_step_until_the_last_question_page_is_reached(self):
        """
        DESCRIPTION: Repeat the 2nd step until the last Question page is reached.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the last Question page.
        """
        # Covered in step 002

    def test_004_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The 'Confirm your selections!' pop-up is opened.
        """
        self.assertTrue(self.site.quiz_page_popup.has_submit_button(), msg='Confirm your selections! pop-up is not opened.')

    def test_005_tap_on_the_submit_button(self):
        """
        DESCRIPTION: Tap on the 'Submit' button.
        EXPECTED: 1. The 'Confirm your selections!' pop-up is closed.
        EXPECTED: 2. The User is navigated to the Latest tab of the Results page.
        EXPECTED: 3. The Upsell 'card' is not displayed (i.e. answers only).
        EXPECTED: Notes:
        EXPECTED: No design for this but it will be the same page without the Upsell section, i.e answer summary should be shifted up.
        """
        self.site.quiz_page_popup.submit_button.click()
        sleep(2)
        result = self.site.quiz_results_page.latest_tab.is_bold
        self.assertTrue(result, msg='Latest tab is not selected')
        self.assertFalse(self.site.quiz_results_page.tab_content.has_upsell_card(expected_result=False), msg='Upsell card is displayed ')
