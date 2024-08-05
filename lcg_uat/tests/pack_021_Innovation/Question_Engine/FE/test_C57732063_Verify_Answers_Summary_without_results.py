import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.question_engine
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C57732063_Verify_Answers_Summary_without_results(Common):
    """
    TR_ID: C57732063
    NAME: Verify 'Answers Summary' without results
    DESCRIPTION: This test case verifies 'Answers Summary' on 'Latest' Tab
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and results are not yet available in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: The user has completed a quiz and results are not yet available in CMS
        """
        self.create_question_engine_quiz()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg='Questions are not displayed')
        for question in questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[0].click()
            sleep(4)  # time required to swipe to next question
            self.site.wait_splash_to_hide(timeout=10)
        self.site.quiz_page_popup.submit_button.click()
        sleep(3)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')

    def test_001___tap_on_correct_4_link__tap_on_see_previous_results_button(self):
        """
        DESCRIPTION: - Tap on Correct 4 link
        DESCRIPTION: - Tap on 'See previous results' button
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ac05f3d5241970342
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: I will see a summary of the questions and my answers as per the attached design as follows:
        EXPECTED: - Header (Your Answers)
        EXPECTED: - Question Numbers
        EXPECTED: - Question
        EXPECTED: - User's answer (formatted bold)
        """
        latest_tab = self.site.quiz_results_page.tab_content
        self.assertEqual(latest_tab.summary_title.text.upper(), vec.question_engine.YOUR_ANSWERS.upper(),
                         msg=f'Actual summary title "{latest_tab.summary_title.text.upper()}" is not same as'
                             f'Expected summary title "{vec.question_engine.YOUR_ANSWERS.upper()}".')
        answers = list(latest_tab.items_as_ordered_dict.items())
        self.assertTrue(answers, msg='"Answers" are not displayed.')
        for key, value in answers:
            self.assertTrue(value.name,
                            msg=f'"Question Number" is not available for the question "{key}"')
            self.assertTrue(value.question_name,
                            msg=f'"Question Name" is not available for the question "{key}"')
            self.assertTrue(value.answer_name,
                            msg=f'"Answer" is not available for the question "{key}"')
