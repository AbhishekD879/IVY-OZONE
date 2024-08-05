import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2   # question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.question_engine
@vtest
class Test_C57732157_Verify_view_of_a_Question_page_and_transition(Common):
    """
    TR_ID: C57732157
    NAME: Verify view of a Question page and transition
    DESCRIPTION: This test case verifies view of a Question page and transition
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user is on the Splash page
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """"
        PRECONDITIONS: Please look for some insights on a pages as follow:
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
        PRECONDITIONS: 1. The user is logged in to CMS
        PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
        PRECONDITIONS: 3. The user is on the Splash page
        """
        self.__class__.quiz = self.create_question_engine_quiz()
        self.assertTrue(self.quiz, msg='Quiz is not present')
        source_page_url = self.quiz['sourceId']
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(user_name=user_name)
        self.navigate_to_page(name=source_page_url)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')

    def test_001_tap_on_play_now_for_free(self):
        """
        DESCRIPTION: Tap on 'Play now for free'
        EXPECTED: - Question page displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: ![](index.php?/attachments/get/36345)
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg='Quiz question are not displayed')
        ui_first_question = self.questions[0].question_header.text
        cms_first_question = self.quiz['firstQuestion']['text']
        self.assertEqual(ui_first_question, cms_first_question,
                         msg=f'Quiz first question is incorrect, expected is "{cms_first_question}" and actual "{ui_first_question}"')

    def test_002_select_answer(self):
        """
        DESCRIPTION: Select answer
        EXPECTED: - The Selected answer is highlighted
        EXPECTED: - The user is navigated to the next question after 2 seconds delay
        """
        self.questions[0].click()
        sleep(5)
        list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        ui_second_question = self.questions[1].question_header.text
        cms_second_question = self.quiz['firstQuestion']['nextQuestions']['123']['text'].rstrip()
        self.assertEqual(ui_second_question, cms_second_question,
                         msg=f'Quiz second question is incorrect, expected is "{cms_second_question}" and actual "{ui_second_question}"')
