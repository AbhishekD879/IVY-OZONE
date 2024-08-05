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
class Test_C57732072_Verify_view_and_data_of_Submit_pop_up(Common):
    """
    TR_ID: C57732072
    NAME: Verify view and data of Submit pop-up
    DESCRIPTION: This test case verifies view and data of Submit pop-up
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - Splash page displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_tap_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap 'Play now for free' button
        EXPECTED: - Questions page successfully displayed
        """
        pass

    def test_003___move_to_the_last_question__tap_on_answer_on_the_last_question(self):
        """
        DESCRIPTION: - Move to the last question
        DESCRIPTION: - Tap on answer on the last question
        EXPECTED: - Submit pop-up displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a1db0449b1282fca9
        """
        pass

    def test_004___make_changes_to_each_field_on_cms__question_enginee__quiz__activequiz__pupups_tab__save_changes(self):
        """
        DESCRIPTION: - Make changes to each field on CMS > Question Enginee > Quiz > [activequiz] > Pupups Tab
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_005___open_questions_page_again__move_to_the_last_question__tap_on_answer_on_the_last_question(self):
        """
        DESCRIPTION: - Open 'Questions' page again
        DESCRIPTION: - Move to the last question
        DESCRIPTION: - Tap on answer on the last question
        EXPECTED: - All data retrieved from CMS to Submit pop-up and correctly displayed
        EXPECTED: - All successfully styled
        """
        pass

    def test_006_tap_on_go_back_and_edit_button(self):
        """
        DESCRIPTION: Tap on 'Go back and edit' button
        EXPECTED: User returns to the first question with the already selected answer
        """
        pass

    def test_007___move_to_the_last_question__tap_on_answer_on_the_last_question(self):
        """
        DESCRIPTION: - Move to the last question
        DESCRIPTION: - Tap on answer on the last question
        EXPECTED: - Submit pop-up displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a1db0449b1282fca9
        """
        pass

    def test_008_tap_on_submit_button(self):
        """
        DESCRIPTION: Tap on 'Submit' button
        EXPECTED: User predictions sent successfully
        """
        pass
