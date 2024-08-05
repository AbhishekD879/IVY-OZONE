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
class Test_C57732103_Verify_the_Quiz_Popup_is_not_displayed_for_the_User_who_has_already_played_a_Quiz(Common):
    """
    TR_ID: C57732103
    NAME: Verify the Quiz Popup is not displayed for the User who has already played a Quiz
    DESCRIPTION: This test case verifies that the Quiz Popup is not displayed for the User who has already played a Quiz.
    PRECONDITIONS: 1. The CMS User has configured the Quiz Popup for a Tennis page.
    PRECONDITIONS: 2. The Quiz Popup is active.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. Open DevTools/Application.
    """
    keep_browser_open = True

    def test_001_open_a_quiz_page_directly(self):
        """
        DESCRIPTION: Open a Quiz page directly
        EXPECTED: The Quiz is opened.
        """
        pass

    def test_002_select_any_answer_to_complete_a_quiz(self):
        """
        DESCRIPTION: Select any answer to complete a Quiz.
        EXPECTED: The User has reached the End Page.
        """
        pass

    def test_003_open_a_sport_page_which_was_configured_in_the_quiz_popupselect_an_env_which_is_currently_testing_in_the_local_storage(self):
        """
        DESCRIPTION: Open a Sport page, which was configured in the Quiz Popup.
        DESCRIPTION: Select an env, which is currently testing, in the local storage.
        EXPECTED: The Quiz Popup is not displayed.
        EXPECTED: The 'qeQuiz' key is not set.
        """
        pass
