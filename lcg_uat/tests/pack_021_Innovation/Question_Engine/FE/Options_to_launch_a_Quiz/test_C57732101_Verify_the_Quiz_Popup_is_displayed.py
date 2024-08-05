import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2 # cannot configure QE in tst2
# @pytest.mark.stg2
@pytest.mark.qe_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732101_Verify_the_Quiz_Popup_is_displayed(Common):
    """
    TR_ID: C57732101
    NAME: Verify the Quiz Popup is displayed
    DESCRIPTION: This test case verifies that the Quiz Popup is displayed after proceeding to the Sport page when:
    DESCRIPTION: - the Quiz Popup is active,
    DESCRIPTION: - the User is logged in,
    DESCRIPTION: - the User proceeds to the Sport page which was configured in the Quiz Popup.
    PRECONDITIONS: 1. The CMS User has configured the Quiz Popup for a Tennis page.
    PRECONDITIONS: 2. The Quiz Popup is active.
    PRECONDITIONS: 3. The User is logged in.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        self.__class__.quiz = self.create_question_engine_quiz(pop_up=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_open_a_sport_page_which_was_configured_in_the_quiz_popup(self):
        """
        DESCRIPTION: Open a Sport page, which was configured in the Quiz Popup.
        EXPECTED: The Quiz Popup is displayed.
        """
        self.navigate_to_page(self.quiz[1]['pageUrls'].strip('*'), qe=True)
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False)
        self.assertTrue(popup, msg='Quiz popup is not displayed')
