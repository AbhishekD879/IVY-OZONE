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
class Test_C57732090_Verify_the_view_of_the_Latest_tab_when_the_Upsell_has_not_been_configured(Common):
    """
    TR_ID: C57732090
    NAME: Verify the view of the Latest tab  when the Upsell has not been configured
    DESCRIPTION: This test case verifies the view of the Latest tab  when the Upsell has not been configured
    PRECONDITIONS: 1. The Upsell has not been configured in the CMS or the 'Show Upsell' toggle is off in the End page configuration.
    PRECONDITIONS: 2. The current Event has not started yet.
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
        EXPECTED: 3. The Upsell 'card' is not displayed (i.e. answers only).
        EXPECTED: Notes:
        EXPECTED: No design for this but it will be the same page without the Upsell section, i.e answer summary should be shifted up.
        """
        pass
