import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.question_engine
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C57732080_Verify_that_the_User_is_navigated_to_the_End_Page_which_was_linked_to_an_Option(Common):
    """
    TR_ID: C57732080
    NAME: Verify that the User is navigated to the End Page, which was linked to an Option
    DESCRIPTION: This test case verifies that the User is navigated to the End Page, which was previously linked to an Option in the 'Questions' tab.
    PRECONDITIONS: 1. The CMS User is logged in.
    PRECONDITIONS: 2. Navigate to the 'Question' tab of an active Quiz.
    PRECONDITIONS: 3. Link the 1st Option to the End page #1.
    PRECONDITIONS: 4. Link the 2nd Option to the End page #2.
    PRECONDITIONS: 5. Save the changes.
    """
    keep_browser_open = True
    first_option = 0
    second_option = 1

    def test_000_preconditions(self):
        self.__class__.quiz = self.create_question_engine_quiz()
        self.__class__.user2 = self.gvc_wallet_user_client.register_new_user().username

    def test_001_login_to_the_system_with_credentials_of_user1(self):
        """
        DESCRIPTION: Login to the system with credentials of User1.
        EXPECTED: The User is successfully logged in.
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_navigate_to_an_active_quiz_by_entering_a_valid_url_eg_httpsrooney_excaliburladbrokescomqenew6(self):
        """
        DESCRIPTION: Navigate to an active Quiz by entering a valid URL (e.g. https://rooney-excalibur.ladbrokes.com/qe/new6/).
        EXPECTED: The User is redirected to the Quiz.
        """
        # covered in step 3

    def test_003_select_the_1st_option_on_last_question_of_quiz(self, option=first_option):
        """
        DESCRIPTION: Select the 1st option on last question of Quiz
        EXPECTED: The User is redirected to the End page, which was linked to the Option1 in the CMS.
        """
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')
        for question in self.questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[option].click()
            sleep(4)  # time required to swipe to next question
        self.site.quiz_page_popup.submit_button.click()
        sleep(5)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out.
        EXPECTED: The User is successfully logged out.
        """
        self.site.logout()

    def test_005_login_to_the_system_with_credentials_of_user2(self):
        """
        DESCRIPTION: Login to the system with credentials of User2.
        EXPECTED: The User is successfully logged in.
        """
        self.site.login(username=self.user2)

    def test_006_navigate_to_an_active_quiz_by_entering_a_valid_url_eg_httpsrooney_excaliburladbrokescomqenew6(self):
        """
        DESCRIPTION: Navigate to an active Quiz by entering a valid URL (e.g. https://rooney-excalibur.ladbrokes.com/qe/new6/).
        EXPECTED: The User is redirected to the Quiz.
        """
        self.test_002_navigate_to_an_active_quiz_by_entering_a_valid_url_eg_httpsrooney_excaliburladbrokescomqenew6()

    def test_007_select_the_2nd_option_on_last_question_of_quiz(self):
        """
        DESCRIPTION: Select the 2nd option on last question of Quiz
        EXPECTED: The User is redirected to the End page, which was linked to the Option2 in the CMS.
        """
        self.test_003_select_the_1st_option_on_last_question_of_quiz(option=self.second_option)
