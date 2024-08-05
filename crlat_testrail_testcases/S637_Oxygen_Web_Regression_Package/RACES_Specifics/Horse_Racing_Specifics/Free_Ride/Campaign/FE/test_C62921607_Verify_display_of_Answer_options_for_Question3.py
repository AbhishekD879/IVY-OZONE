import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C62921607_Verify_display_of_Answer_options_for_Question3(Common):
    """
    TR_ID: C62921607
    NAME: Verify display of Answer options for Question3
    DESCRIPTION: This test case verifies display of Answer options for Question3
    PRECONDITIONS: CMS
    PRECONDITIONS: 1: Campaign should be created and in currently running status
    PRECONDITIONS: 2: First ,Second and Third questions with Answer options(Option1, Option2 and option3) are configured
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
        DESCRIPTION: Select Answer for Second question
        EXPECTED: Selected Answer should be displayed below to Step 2 of 3
        """
        pass

    def test_006_verify_display_of_third_question(self):
        """
        DESCRIPTION: Verify display of Third Question
        EXPECTED: Second Question should be displayed in Free Ride Overlay screen
        """
        pass

    def test_007_verify_display_of_answer_options_for_third_question(self):
        """
        DESCRIPTION: Verify display of Answer Options for Third Question
        EXPECTED: Answer Options should be displayed below to Step 3 of 3 as below
        EXPECTED: * Good Chance
        EXPECTED: * Nice price
        EXPECTED: * Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        pass
