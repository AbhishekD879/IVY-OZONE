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
class Test_C57732078_Verify_the_view_and_functionality_of_Back_arrow_button_when_the_Use_back_button_to_exit_and_hide_X_button_toggle_is_set_OFF(Common):
    """
    TR_ID: C57732078
    NAME: Verify the view and functionality of Back arrow button when the 'Use back button to exit and hide X button' toggle is set OFF
    DESCRIPTION: This test case verifies the view and functionality of Back arrow button when the 'Use back button to exit and hide X button' toggle is set OFF.
    PRECONDITIONS: 1. The CMS User is logged in.
    PRECONDITIONS: 2. Open an active Quiz.
    PRECONDITIONS: 3. Navigate to the 'Quiz Configuration' tab.
    PRECONDITIONS: 4. Set the 'Use back button to exit and hide X button' toggle ON.
    PRECONDITIONS: 5. Save the changes.
    """
    keep_browser_open = True

    def test_001_navigate_to_a_question_page_of_an_active_quiz_on_feeg_httpsrooney_excaliburladbrokescomqenew155questions(self):
        """
        DESCRIPTION: Navigate to a Question page of an active Quiz on FE
        DESCRIPTION: (e.g. https://rooney-excalibur.ladbrokes.com/qe/new155/questions).
        EXPECTED: A Question page is displayed.
        EXPECTED: The 'X' icon is displayed in the tor right corner and has size 12x12 px.
        EXPECTED: The Back arrow button is displayed in the top left corner and has size 19x16 px.
        """
        pass

    def test_002_tap_the_x_button(self):
        """
        DESCRIPTION: Tap the 'X' button.
        EXPECTED: The Exit pop-up is opened.
        """
        pass

    def test_003_tap_the_close_cta_button(self):
        """
        DESCRIPTION: Tap the 'Close' CTA button.
        EXPECTED: The Exit pop-up is closed.
        EXPECTED: The User is redirected to the Home page.
        """
        pass

    def test_004_navigate_to_a_question_page_of_an_active_quiz_on_feeg_httpsrooney_excaliburladbrokescomqenew155questions(self):
        """
        DESCRIPTION: Navigate to a Question page of an active Quiz on FE
        DESCRIPTION: (e.g. https://rooney-excalibur.ladbrokes.com/qe/new155/questions).
        EXPECTED: A Question page is displayed.
        EXPECTED: The 'X' icon is displayed in the tor right corner and has size 12x12 px.
        EXPECTED: The Back arrow button is displayed in the top left corner and has size 19x16 px.
        """
        pass

    def test_005_tap_the_back_arrow_button(self):
        """
        DESCRIPTION: Tap the Back arrow button.
        EXPECTED: The Exit pop-up is opened.
        """
        pass

    def test_006_tap_the_close_cta_button(self):
        """
        DESCRIPTION: Tap the 'Close' CTA button.
        EXPECTED: The Exit pop-up is closed.
        EXPECTED: The User is redirected to the previous page (e.g. Splash page).
        """
        pass
