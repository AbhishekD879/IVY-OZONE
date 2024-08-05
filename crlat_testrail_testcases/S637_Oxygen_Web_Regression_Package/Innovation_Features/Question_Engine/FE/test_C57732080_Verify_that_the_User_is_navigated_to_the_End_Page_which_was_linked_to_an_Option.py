import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
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

    def test_001_login_to_the_system_with_credentials_of_user1(self):
        """
        DESCRIPTION: Login to the system with credentials of User1.
        EXPECTED: The User is successfully logged in.
        """
        pass

    def test_002_navigate_to_an_active_quiz_by_entering_a_valid_url_eg_httpsrooney_excaliburladbrokescomqenew6(self):
        """
        DESCRIPTION: Navigate to an active Quiz by entering a valid URL (e.g. https://rooney-excalibur.ladbrokes.com/qe/new6/).
        EXPECTED: The User is redirected to the Quiz.
        """
        pass

    def test_003_select_the_1st_option_on_last_question_of_quiz(self):
        """
        DESCRIPTION: Select the 1st option on last question of Quiz
        EXPECTED: The User is redirected to the End page, which was linked to the Option1 in the CMS.
        """
        pass

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out.
        EXPECTED: The User is successfully logged out.
        """
        pass

    def test_005_login_to_the_system_with_credentials_of_user2(self):
        """
        DESCRIPTION: Login to the system with credentials of User2.
        EXPECTED: The User is successfully logged in.
        """
        pass

    def test_006_navigate_to_an_active_quiz_by_entering_a_valid_url_eg_httpsrooney_excaliburladbrokescomqenew6(self):
        """
        DESCRIPTION: Navigate to an active Quiz by entering a valid URL (e.g. https://rooney-excalibur.ladbrokes.com/qe/new6/).
        EXPECTED: The User is redirected to the Quiz.
        """
        pass

    def test_007_select_the_2nd_option_on_last_question_of_quiz(self):
        """
        DESCRIPTION: Select the 2nd option on last question of Quiz
        EXPECTED: The User is redirected to the End page, which was linked to the Option2 in the CMS.
        """
        pass
