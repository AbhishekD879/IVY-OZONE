import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732053_Verify_appearing_of_Quiz_Pop_ups_when_user_abandons_the_Quiz(Common):
    """
    TR_ID: C57732053
    NAME: Verify appearing  of Quiz Pop-ups when user abandons the Quiz
    DESCRIPTION: This test case verifies displaying of Quiz Pop-ups
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. User did not play quiz yet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The user is logged in to Coral/Ladbrokes test environment
        PRECONDITIONS: 2. User did not play quiz yet
        """
        self.__class__.quiz = self.create_question_engine_quiz(pop_up=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_open_correct_4qe_link(self):
        """
        DESCRIPTION: Open Correct 4/QE link
        EXPECTED: - Correct 4/QE successfully opened
        """
        self.navigate_to_page('footballsuperseries')

    def test_002_user_abandons_the_quiz_by_selecting_the_back_arrow_or_x(self):
        """
        DESCRIPTION: User abandons the Quiz by selecting the Back arrow or 'X'
        EXPECTED: - Correct 4/QE should be closed and user redirected to the previous page
        """
        if self.device_type == 'mobile':
            self.site.question_engine.close_button.click()
        else:
            self.site.question_engine.back_button.click()
        self.site.wait_content_state('Homepage')

    def test_003_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz__pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz > Pop-Ups)
        EXPECTED: - Pop-up should appear on the configured page until predictions made
        """
        self.navigate_to_page(self.quiz[1]['pageUrls'].strip('*'), qe=True)
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False, timeout=5)
        self.assertTrue(popup, msg='Quiz popup is not displayed')

    def test_004_open_any_page_url_which_is_not_configured_to_trigger_pop_up(self):
        """
        DESCRIPTION: Open ANY page URL which is NOT configured to trigger Pop-Up
        EXPECTED: - Pop-up should NOT appear on any other pages
        """
        self.navigate_to_page('sport/basketball')
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False, timeout=5)
        self.assertFalse(popup, msg='Quiz popup is displayed')
