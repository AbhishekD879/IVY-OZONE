import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C62921605_Verify_display_of_Third_question_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921605
    NAME: Verify display of Third question in Free Ride Overlay
    DESCRIPTION: This test case verifies display of Third question in Free Ride Overlay
    PRECONDITIONS: CMS:
    PRECONDITIONS: 1: Campaign should be created(Currently running)
    PRECONDITIONS: 2: Make sure First, Second and Third questions are configured
    PRECONDITIONS: 3: Answer options for Question 1 and 2 are configured
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_eligible(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_launch_free_ride_banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash page with CTA button should be displayed
        """
        pass

    def test_003_click_on_cta_button_in_splash_page(self):
        """
        DESCRIPTION: Click on CTA button in Splash Page
        EXPECTED: Free Ride overlay should be displayed
        """
        pass

    def test_004_select_answer_for_first_question(self):
        """
        DESCRIPTION: Select Answer for First question
        EXPECTED: Selected Answer should be displayed below to Step 1 of 3
        """
        pass

    def test_005_select_answer_for_second_question(self):
        """
        DESCRIPTION: Select Answer for second question
        EXPECTED: Selected Answer should be displayed below to Step 2 of 3
        """
        pass

    def test_006_verify_display_of_third_question(self):
        """
        DESCRIPTION: Verify display of Third Question
        EXPECTED: Third Question should be displayed in Free Ride Overlay screen
        """
        pass

    def test_007_verify_the_content_in_third_question(self):
        """
        DESCRIPTION: Verify the content in Third Question
        EXPECTED: Content in Third Question should be displayed as per the CMS configurations from 'Question3' field in Questions section in campaign
        """
        pass
