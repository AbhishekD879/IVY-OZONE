import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 # QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732077_Verify_the_view_and_functionality_of_Back_arrow_button_when_the_Use_back_button_to_exit_and_hide_X_button_toggle_is_set_ON(Common):
    """
    TR_ID: C57732077
    NAME: Verify the view and functionality of Back arrow button when the 'Use back button to exit and hide X button' toggle is set ON
    DESCRIPTION: This test case verifies the view and functionality of Back arrow button when the 'Use back button to exit and hide X button' toggle is set ON.
    PRECONDITIONS: 1. The CMS User is logged in.
    PRECONDITIONS: 2. Open an active Quiz.
    PRECONDITIONS: 3. Navigate to the 'Quiz Configuration' tab.
    PRECONDITIONS: 4. Set the 'Use back button to exit and hide X button' toggle ON.
    PRECONDITIONS: 5. Set 'Show exit pop-up' toggle ON
    PRECONDITIONS: 6. Save the changes.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        quiz = self.create_question_engine_quiz()
        self.assertTrue(quiz, msg=f'"Created Quiz" is not displayed')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.wait_content_state('HomePage', timeout=10)

    def test_001_navigate_to_a_question_page_of_an_active_quiz_on_feeg_httpsrooney_excaliburladbrokescomqenew155questions(self):
        """
        DESCRIPTION: Navigate to a Question page of an active Quiz on FE
        DESCRIPTION: (e.g. https://rooney-excalibur.ladbrokes.com/qe/new155/questions).
        EXPECTED: A Question page is displayed.
        EXPECTED: The 'X' icon is not displayed.
        EXPECTED: The Back arrow button is displayed in the top left corner and has size 19x16 px.
        """
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'"CTA Button" is not displayed')
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg='Questions are not displayed')

    def test_002_tap_the_back_arrow_button(self):
        """
        DESCRIPTION: Tap the Back arrow button.
        EXPECTED: The Exit pop-up is opened.
        """
        self.assertTrue(self.site.question_engine.quick_links_page.has_back_button(),
                        msg=f'"Back Button" is not displayed')
        self.site.question_engine.quick_links_page.back_button.click()
        self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(expected_result=True),
                        msg='Exit pop-up is not displayed')

    def test_003_tap_the_close_cta_button(self):
        """
        DESCRIPTION: Tap the 'Close' CTA button.
        EXPECTED: The Exit pop-up is closed.
        EXPECTED: The User is redirected to the Home page.
        """
        self.site.quiz_page_popup.exit_quiz_popup.leave_button.click()
        self.site.wait_content_state("HomePage")
