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
class Test_C57732158_Verify_the_view_of_the_Progress_bar(Common):
    """
    TR_ID: C57732158
    NAME: Verify the view of the Progress bar
    DESCRIPTION: This test case verifies the view of the Progress bar.
    PRECONDITIONS: 1. The User is on the Splash page.
    PRECONDITIONS: 2. Tap on the CTA button.
    """
    keep_browser_open = True

    def test_001_tap_on_any_answer(self):
        """
        DESCRIPTION: Tap on any answer.
        EXPECTED: The User is navigated to the next question.
        EXPECTED: The Progress bar is incremented to indicate progress out of the total number of questions available.
        """
        pass

    def test_002_swipe_left(self):
        """
        DESCRIPTION: Swipe left.
        EXPECTED: The User is navigated to the previous question.
        EXPECTED: The Progress bar is decremented to indicate progress out of the total number of questions available.
        """
        pass
