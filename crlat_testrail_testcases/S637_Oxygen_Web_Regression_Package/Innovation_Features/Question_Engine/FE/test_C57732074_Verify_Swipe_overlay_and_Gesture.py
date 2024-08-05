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
class Test_C57732074_Verify_Swipe_overlay_and_Gesture(Common):
    """
    TR_ID: C57732074
    NAME: Verify Swipe overlay and Gesture
    DESCRIPTION: This test case verifies Swipe overlay and Gesture
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
        EXPECTED: - Splash page displayed
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_tap_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap 'Play now for free' button
        EXPECTED: - Questions page successfully displayed
        """
        pass

    def test_003_tap_on_answer_on_question_1(self):
        """
        DESCRIPTION: Tap on answer on Question 1
        EXPECTED: - User automatically be navigated to Question 2
        EXPECTED: - Swipe overlay with the left / right swipe gesture appear
        EXPECTED: Mobile:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ab19d56351032d23e
        EXPECTED: Tablet:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b4b6c1b60256cb4cdf
        """
        pass

    def test_004_tap_on_answer_on_question_2(self):
        """
        DESCRIPTION: Tap on answer on Question 2
        EXPECTED: - User automatically be navigated to Question 3
        EXPECTED: - Swipe overlay with the left / right swipe gesture NOT appear
        EXPECTED: (Show once per quiz)
        """
        pass

    def test_005___return_to_question_1_using_swipe_right__tap_on_answer_on_question_1(self):
        """
        DESCRIPTION: - Return to Question 1 using Swipe right
        DESCRIPTION: - Tap on answer on Question 1
        EXPECTED: - User navigated to Question 1
        EXPECTED: - Swipe overlay with the left / right swipe gesture NOT appear
        EXPECTED: (Show once per quiz)
        """
        pass

    def test_006___return_to_question_3_using_swipe_left(self):
        """
        DESCRIPTION: - Return to Question 3 using Swipe left
        EXPECTED: - User navigated to Question 3
        EXPECTED: - Swipe overlay with the left / right swipe gesture NOT appear
        EXPECTED: (Show once per quiz)
        """
        pass
