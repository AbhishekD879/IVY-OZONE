import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.homepage_featured
@vtest
class Test_C62921598_Verify_display_of_First_question_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921598
    NAME: Verify display of First question in Free Ride Overlay
    DESCRIPTION: This test case verifies display of First question in Free Ride Overlay
    PRECONDITIONS: Campaign should be created(Currently running) in Free Ride and First Question should be configured in CMS
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
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

    def test_005_verify_the_content_in_first_question(self):
        """
        DESCRIPTION: Verify the content in First Question
        EXPECTED: Content in First Question should be displayed as per the CMS configurations from 'Question1' field in Questions section in campaign
        """
        pass
