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
class Test_C57732088_Verify_the_hiding_of_the_Upsell(Common):
    """
    TR_ID: C57732088
    NAME: Verify the hiding of the Upsell
    DESCRIPTION: This test case verifies the hiding of the Upsell.
    PRECONDITIONS: 1. The dynamic or generic Upsell is configured in the CMS.
    PRECONDITIONS: 2. The current Event has finished (results available and all answers are set as correct in the CMS).
    PRECONDITIONS: 3. The Quiz is configured in the CMS.
    PRECONDITIONS: 4. The User is logged in.
    PRECONDITIONS: 5. The User has not played a Quiz yet.
    """
    keep_browser_open = True

    def test_001_tap_on_the_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap on the 'Play Now For Free' button.
        EXPECTED: The User is redirected to the 1st Question page.
        """
        pass

    def test_002_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the next Question page.
        """
        pass

    def test_003_repeat_the_2nd_step_until_the_last_question_page_is_reached(self):
        """
        DESCRIPTION: Repeat the 2nd step until the last Question page is reached.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the last Question page.
        """
        pass

    def test_004_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The 'Confirm your selections!' pop-up is opened.
        """
        pass

    def test_005_tap_on_the_submit_button(self):
        """
        DESCRIPTION: Tap on the 'Submit' button.
        EXPECTED: 1. The 'Confirm your selections!' pop-up is closed.
        EXPECTED: 2. The User is navigated to the Latest tab of the Results page.
        EXPECTED: 3. The Upsell card is note displayed (i.e only answer section is shown).
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a2ffb679bba35fce2
        """
        pass
