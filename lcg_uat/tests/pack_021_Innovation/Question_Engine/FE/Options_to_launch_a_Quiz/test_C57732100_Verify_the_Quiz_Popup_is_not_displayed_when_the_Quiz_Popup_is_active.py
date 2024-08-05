import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2   #  QE not configured on tst2
# @pytest.mark.stg2
@pytest.mark.qe_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732100_Verify_the_Quiz_Popup_is_not_displayed_when_the_Quiz_Popup_is_active(Common):
    """
    TR_ID: C57732100
    NAME: Verify the Quiz Popup is not displayed when the Quiz Popup is active
    DESCRIPTION: This test case verifies that the Quiz Popup is nod displayed after proceeding to the Sport page when:
    DESCRIPTION: - the Quiz Popup is active,
    DESCRIPTION: - the User is logged in,
    DESCRIPTION: - the User proceeds to the Sport page which was not configured in the Quiz Popup.
    PRECONDITIONS: 1. The CMS User has configured the Quiz Popup for a Tennis page.
    PRECONDITIONS: 2. The Quiz Popup is active.
    PRECONDITIONS: 3. The User is logged in.
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. The CMS User has configured an active Quiz Popup.
        PRECONDITIONS: 2. The User is logged out.
        """
        question_engine = self.create_question_engine_quiz(pop_up=True)
        self.assertTrue(question_engine, msg='Quiz is not configured in the CMS')
        self.site.login()

    def test_001_open_a_sport_page_which_was_not_configured_in_the_quiz_popup(self):
        """
        DESCRIPTION: Open a Sport page, which was not configured in the Quiz Popup.
        EXPECTED: The Quiz Popup is not displayed.
        """
        self.navigate_to_page("/sport/basketball")
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False)
        self.assertFalse(popup, msg='Quiz popup is displayed for Sport page "Basketball", which was not configured in the Quiz Popup')
