import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 # QA2 configuration for QE not working
# @pytest.mark.stg2
@pytest.mark.qe_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732060_Verify_End_page_tabs(Common):
    """
    TR_ID: C57732060
    NAME: Verify 'End' page tabs
    DESCRIPTION: This test case verifies 'End' page tabs
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and submit my final answers
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        user has completed a quiz and submit final answers
        """
        self.__class__.cms_qe_config = self.create_question_engine_quiz()
        self.assertTrue(self.cms_qe_config, msg='Question Engine Quiz not created')
        splash_pages = self.cms_config.get_qe_splash_page()
        self.__class__.cms_splash_page = next(
            (page for page in splash_pages if page.get('title') == "Autotest_Splash_Page"))
        self.site.login()
        self.navigate_to_page('footballsuperseries')
        self.site.wait_splash_to_hide(timeout=10)

        try:
            self.assertTrue(self.site.question_engine.has_cta_button(),
                            msg='"Play now for free" button is not displayed')
            actual_playnowforfree_button = self.site.question_engine.cta_button.text
            self.assertEqual(actual_playnowforfree_button, self.cms_splash_page['playForFreeCTAText'],
                             msg=f'Actual "Play now for free" button text : "{actual_playnowforfree_button}"'
                                 f'is not as expected : "{self.cms_splash_page["playForFreeCTAText"]}"')
            self.site.question_engine.cta_button.click()
            questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
            self.assertTrue(questions, msg='Questions are not displayed')

            for question in questions:
                options = list(question.answer_options.items_as_ordered_dict.values())
                options[0].click()
                sleep(4)  # time required to swipe to next question
                self.site.wait_splash_to_hide(timeout=10)
            self.site.quiz_home_page.submit.click()
            sleep(3)
            self.site.wait_splash_to_hide(timeout=10)
            submit_msg_cms = self.cms_qe_config['endPage']['submitMessage']
            submit_msg_ui = self.site.quiz_results_page.submit_message
            self.assertEqual(submit_msg_ui, submit_msg_cms,
                             msg=f'Actual Message{submit_msg_ui}'
                                 f' is not same as expected message {submit_msg_cms} ')
            self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')
        except Exception:
            cms_btn_text = self.cms_qe_config['splashPage']['seePreviousSelectionsCTAText']
            cta_btn_text = self.site.question_engine.cta_button.text
            self.assertEqual(cta_btn_text.lower(), cms_btn_text.lower(),
                             msg=f'"CTA message not appeared as expected: {cms_btn_text} '
                                 f'Actual message appeared: "{cta_btn_text}"')

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        # Covered in above step

    def test_002_user_tap_on_latest_tab(self):
        """
        DESCRIPTION: User tap on Latest Tab
        EXPECTED: - Latest Tab successfully opened
        EXPECTED: - Submit message text displayed according to configuration on CMS
        EXPECTED: - Information about Latest game is correctly displayed
        """
        ans_summary = self.cms_qe_config['endPage']['showAnswersSummary']
        self.assertTrue(ans_summary, msg='User Selected answers summary not displayed in end page')

    def test_003_user_tap_on_previous_tab(self):
        """
        DESCRIPTION: User tap on Previous Tab
        EXPECTED: - Previous Tab succssefuly opened
        EXPECTED: - Information about Previous game is correctly displayed
        """
        cta_btn_text_ui = self.site.question_engine.cta_button.text
        cta_cms_btn = self.cms_splash_page['seePreviousSelectionsCTAText']
        if cta_btn_text_ui.lower() == cta_cms_btn.lower():
            self.assertTrue(self.site.question_engine.cta_button,
                            msg="'See previous results' link is not displayed")
            self.site.contents.scroll_to_top()
            self.site.question_engine.cta_button.click()
            self.assertTrue(self.site.quiz_results_page.quicklinks_section, msg="Footer text is not  displayed")
        else:
            self.site.contents.scroll_to_top()
            self.site.quiz_results_page.previous_tab.click()

        try:
            self.assertTrue(self.site.quiz_results_page.has_results_summary,
                            msg='No resulted quiz found in previous tab')
        except Exception:
            self.assertTrue(self.site.quiz_results_page.has_no_game_text,
                            msg='Found Resulted quiz in previous tab')
