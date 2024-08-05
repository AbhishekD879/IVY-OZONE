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
class Test_C57732085_Verify_the_view_of_the_Question_page_Desktop(Common):
    """
    TR_ID: C57732085
    NAME: Verify the view of the Question page [Desktop]
    DESCRIPTION: This test case verifies the view of the Question page on the Desktop.
    PRECONDITIONS: 1. The game is configured in the CMS.
    PRECONDITIONS: 2. The User is logged in.
    PRECONDITIONS: 3. The User has not played the game yet.
    PRECONDITIONS: 4. Click on the 'Correct4' link.
    PRECONDITIONS: 5. Login with valid credentials.
    """
    keep_browser_open = True

    def test_001_click_on_the_cta_to_start_a_game(self):
        """
        DESCRIPTION: Click on the CTA to start a game.
        EXPECTED: 1. The first question page is displayed with the CMS content.
        EXPECTED: 2. The Back arrow in the top left corner is not displayed.
        EXPECTED: 3. The Next arrow button is disabled.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        EXPECTED: 5. The blue background container is displayed to the end of the page as on the screenshot
        EXPECTED: https://files.slack.com/files-pri/T383TLAQG-FQNDP7CTG/screenshot_2019-11-15_at_16.17.14.png
        """
        pass

    def test_002_click_on_the_exit_button(self):
        """
        DESCRIPTION: Click on the 'Exit' button.
        EXPECTED: 1. The Exit pop-up is opened with:
        EXPECTED: - 'Keep playing' button
        EXPECTED: - 'Exit game' button.
        EXPECTED: 2. The sub-header with breadcrumbs is not displayed. https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c42bb3cda171b2ee259
        """
        pass

    def test_003_click_on_the_keep_playing_button(self):
        """
        DESCRIPTION: Click on the 'Keep playing' button.
        EXPECTED: 1. The Exit pop-up is closed.
        EXPECTED: 2. The first question page is displayed with the CMS content.
        EXPECTED: 3. The Back arrow in the top left corner is not displayed.
        EXPECTED: 4. The Next arrow button is disabled.
        EXPECTED: 5. The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_004_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: 1. The Next arrow button is activated.
        EXPECTED: 2. The User is auto-navigated to the next question after 2 sec delay.
        EXPECTED: 3. The Previous arrow button is activated.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_005_click_on_the_previous_arrow_button(self):
        """
        DESCRIPTION: Click on the Previous arrow button.
        EXPECTED: 1. The User is redirected to the first question page.
        EXPECTED: 2. The previously selected answer is highlighted with yellow colour.
        EXPECTED: 3. The Next arrow button is activated.
        EXPECTED: 4. The Previous arrow button is not displayed.
        EXPECTED: 5. The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_006_click_on_the_next_arrow_button(self):
        """
        DESCRIPTION: Click on the Next arrow button.
        EXPECTED: 1. The User is redirected to the second question page.
        EXPECTED: 2. The Previous arrow button is activated.
        EXPECTED: 3. The Next arrow button is disabled until the current question is not answered yet.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_007_select_any_answer_to_reach_the_last_question(self):
        """
        DESCRIPTION: Select any answer to reach the last question.
        EXPECTED: 1. The User is redirected to the last question page.
        EXPECTED: 2. The Previous arrow button is activated.
        EXPECTED: 3. The Next arrow button is not displayed.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_008_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: 1. The Submit pop-up is opened with:
        EXPECTED: - 'Submit' CTA button;
        EXPECTED: - 'Go back and edit' CTA button.
        EXPECTED: 2. The sub-header with breadcrumbs is not displayed. https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c423a69a102934ab917
        """
        pass

    def test_009_click_on_the_go_back_and_edit_button(self):
        """
        DESCRIPTION: Click on the 'Go back and edit' button.
        EXPECTED: 1. The User is auto-navigated to the first question page.
        EXPECTED: 2. The Next arrow button is activated.
        EXPECTED: 3. The previously selected answer is highlighted with yellow colour.
        EXPECTED: 4. The sub-header with breadcrumbs is not displayed.
        EXPECTED: 5. The swipe gesture tutorial is not displayed.
        """
        pass

    def test_010_edit_the_answers_and_proceed_to_the_last_question_page(self):
        """
        DESCRIPTION: Edit the answers and proceed to the last question page.
        EXPECTED: 1. The User is auto-navigated to the next question.
        EXPECTED: 2. The Next and Previous arrow buttons are activated.
        EXPECTED: 3. The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_011_click_on_the_submit_button(self):
        """
        DESCRIPTION: Click on the 'Submit' button.
        EXPECTED: 1. The end page is displayed showing the CMS content as per designs.
        EXPECTED: 2. The content is centered. https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c424447d165903a0bd5
        """
        pass
