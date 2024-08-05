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
class Test_C57732098_Verify_the_Quiz_Popup_is_not_displayed_for_logged_out_User(Common):
    """
    TR_ID: C57732098
    NAME: Verify the Quiz Popup is not displayed for logged out User
    DESCRIPTION: This test case verifies that the Quiz Popup is nod displayed after proceeding to the Sport page for logged out User.
    PRECONDITIONS: 1. The CMS User has configured an active Quiz Popup.
    PRECONDITIONS: 2. The User is logged out.
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. The CMS User has configured an active Quiz Popup.
        PRECONDITIONS: 2. The User is logged out.
        """
        question_engine = self.create_question_engine_quiz(pop_up=True)
        self.assertTrue(question_engine, msg='Quiz is not configured in the CMS')

    def test_001_open_a_sport_page_which_was_configured_in_the_quiz_popup(self):
        """
        DESCRIPTION: Open a Sport page, which was configured in the Quiz Popup.
        EXPECTED: The Quiz Popup is not displayed.
        """
        self.navigate_to_page("/sport/football")
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False)
        self.assertFalse(popup, msg='Quiz popup is displayed for logged out user')
