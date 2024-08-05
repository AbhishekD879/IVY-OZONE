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
class Test_C62921600_Verify_display_of_Answer_options_for_Question1(Common):
    """
    TR_ID: C62921600
    NAME: Verify display of Answer options for Question1
    DESCRIPTION: This test case verifies display of Answer options for Question1
    PRECONDITIONS: 1: Campaign should should in CMS and it is currently running
    PRECONDITIONS: 2: First questions with Answer options(Option1, Option2 and option3) are configured in CMS
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

    def test_004_verify_display_of_first_question(self):
        """
        DESCRIPTION: Verify display of First Question
        EXPECTED: First Question should be displayed in Free Ride Overlay screen
        """
        pass

    def test_005_verify_display_of_answer_options_for_first_question(self):
        """
        DESCRIPTION: Verify display of Answer Options for First Question
        EXPECTED: Answer Options should be displayed below to Step 1 of 3 as below
        EXPECTED: * Top Player
        EXPECTED: * Dark Horse
        EXPECTED: * Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        pass
