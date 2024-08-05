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
class Test_C57732102_Verify_the_Quiz_Popup_stops_displaying(Common):
    """
    TR_ID: C57732102
    NAME: Verify the Quiz Popup  stops displaying
    DESCRIPTION: This test case verifies that the Quiz Popup stops displaying to the User.
    PRECONDITIONS: 1. The CMS User has configured the Quiz Popup for a Tennis page.
    PRECONDITIONS: 2. The Quiz Popup is active.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. Open DevTools/Application.
    """
    keep_browser_open = True

    def test_001_open_a_sport_page_which_was_configured_in_the_quiz_popupselect_an_env_which_is_currently_testing_in_the_local_storage(self):
        """
        DESCRIPTION: Open a Sport page, which was configured in the Quiz Popup.
        DESCRIPTION: Select an env, which is currently testing, in the local storage.
        EXPECTED: The Quiz Popup is displayed.
        EXPECTED: The 'qeQuiz' key is not set.
        """
        pass

    def test_002_click_on_the_take_a_quiz_button(self):
        """
        DESCRIPTION: Click on the 'Take a quiz' button.
        EXPECTED: The User is redirected to the Quiz.
        EXPECTED: The 'qeQuiz' key with "showAgain: false" value is set.
        """
        pass

    def test_003_click_on_the_horce_racing_tab(self):
        """
        DESCRIPTION: Click on the 'Horce racing' tab.
        EXPECTED: The Quiz Popup is not displayed.
        """
        pass

    def test_004_delete_the_qequiz_key(self):
        """
        DESCRIPTION: Delete the 'qeQuiz' key.
        EXPECTED: The key is successfully deleted.
        """
        pass

    def test_005_click_on_the_home_tab(self):
        """
        DESCRIPTION: Click on the 'Home' tab.
        EXPECTED: The Quiz Popup is displayed.
        EXPECTED: The 'qeQuiz' key is not set.
        """
        pass

    def test_006_click_on_the_dont_chow_me_again_button(self):
        """
        DESCRIPTION: Click on the 'Don't chow me again' button.
        EXPECTED: The Quiz pop-up is closed.
        EXPECTED: The 'qeQuiz' key with "showAgain: false" value is set.
        """
        pass

    def test_007_click_on_the_horce_racing_tab(self):
        """
        DESCRIPTION: Click on the 'Horce racing' tab.
        EXPECTED: The Quiz Popup is not displayed.
        """
        pass

    def test_008_delete_the_qequiz_key(self):
        """
        DESCRIPTION: Delete the 'qeQuiz' key.
        EXPECTED: The key is successfully deleted.
        """
        pass

    def test_009_click_on_the_home_tab(self):
        """
        DESCRIPTION: Click on the 'Home' tab.
        EXPECTED: The Quiz Popup is displayed.
        EXPECTED: The 'qeQuiz' key is not set.
        """
        pass

    def test_010_click_on_the_remind_me_later_button(self):
        """
        DESCRIPTION: Click on the 'Remind me later' button.
        EXPECTED: The Quiz pop-up is closed.
        EXPECTED: The 'qeQuiz' key is not set.
        """
        pass

    def test_011_click_on_the_horce_racing_tab(self):
        """
        DESCRIPTION: Click on the 'Horce racing' tab.
        EXPECTED: The Quiz Popup is displayed.
        """
        pass
