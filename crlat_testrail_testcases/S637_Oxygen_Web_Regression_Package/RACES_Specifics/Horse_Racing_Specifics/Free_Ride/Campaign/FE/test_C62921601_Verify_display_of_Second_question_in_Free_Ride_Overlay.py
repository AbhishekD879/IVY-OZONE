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
class Test_C62921601_Verify_display_of_Second_question_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921601
    NAME: Verify display of Second question in Free Ride Overlay
    DESCRIPTION: This test case verifies display of Second question in Free Ride Overlay
    PRECONDITIONS: CMS:
    PRECONDITIONS: 1: Campaign should be created(Currently running)
    PRECONDITIONS: 2: Make sure First question & Answer options and second question is configured
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

    def test_005_verify_display_of_second_question(self):
        """
        DESCRIPTION: Verify display of Second Question
        EXPECTED: Second Question should be displayed in Free Ride Overlay screen
        """
        pass

    def test_006_verify_the_content_in_second_question(self):
        """
        DESCRIPTION: Verify the content in Second Question
        EXPECTED: Content in Second Question should be displayed as per the CMS configurations from 'Question2' field in Questions section in campaign
        """
        pass
