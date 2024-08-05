import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 # QA2 configuration for QE not working
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.question_engine
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C57732064_Verify_Answers_Summary_footer_text(Common):
    """
    TR_ID: C57732064
    NAME: Verify 'Answers Summary' footer text
    DESCRIPTION: This test case verifies 'Answers Summary' on 'Latest' Tab
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and results are not yet available in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        user has completed a quiz and submit final answers
        """
        quiz = self.create_question_engine_quiz()
        self.assertTrue(quiz, msg='Quiz is not configured in the CMS')
        user = tests.settings.user_has_completed_quiz
        self.site.login(username=user)

    def test_001___tap_on_correct_4_link__tap_on_see_previous_results_button(self):
        """
        DESCRIPTION: - Tap on Correct 4 link
        DESCRIPTION: - Tap on 'See previous results' button
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ac05f3d5241970342
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: - Footer text displayed
        """
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.has_previous_results_link(), msg="'See previous results' link is not displayed")
        self.site.question_engine.previous_results_link.click()
        self.assertTrue(self.site.quiz_results_page.quicklinks_section, msg="Footer text is not  displayed")
