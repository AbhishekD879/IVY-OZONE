import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 # no config for QE in tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732069_Verify_Submit_message(Common):
    """
    TR_ID: C57732069
    NAME: Verify 'Submit' message
    DESCRIPTION: This test case verifies 'Submit' message

    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Please look for some insights on a pages as follow:
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
        PRECONDITIONS: 1. The user is logged in to CMS
        PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
        """
        self.__class__.quiz = self.create_question_engine_quiz()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001___open_correct_4__submit_final_answers(self):
        """
        DESCRIPTION: - Open Correct 4
        DESCRIPTION: - Submit final answers
        EXPECTED: - User navigated to the Latest Tab (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ac05f3d5241970342
        EXPECTED: - Green stripe with Submit message text displayed (message will fade away after 3sec)
        """
        self.navigate_to_page('footballsuperseries')
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        for question in questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[0].click()
            sleep(4)
        self.site.quiz_home_page.submit.click()
        success_message = wait_for_result(lambda: self.site.quiz_results_page.submit_message is not None,
                                          name='Amount field text to display',
                                          timeout=3)
        self.assertTrue(success_message, msg=f'Submit message not displayed')

    def test_002_user_tap_on_previous_tab_and_open_again_latest_tab(self):
        """
        DESCRIPTION: User tap on Previous Tab and open again Latest Tab
        EXPECTED: - Latest Tab succssefuly opened
        EXPECTED: - Submit message text should not be displayed
        """
        self.site.quiz_results_page.previous_tab.click()
        sleep(1.5)
        result = self.site.quiz_results_page.previous_tab.is_bold
        self.assertTrue(result, msg='Previous tab is not selected')
        self.site.quiz_results_page.latest_tab.click()
        sleep(1.5)
        result = self.site.quiz_results_page.latest_tab.is_bold
        self.assertTrue(result, msg='Latest tab is not selected')
        success_message = self.site.quiz_results_page.submit_message
        self.assertFalse(success_message, msg=f'Submit message is still displayed')
        