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
class Test_C62921596_Verify_display_of_Welcome_message_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921596
    NAME: Verify display of Welcome message in Free Ride Overlay
    DESCRIPTION: This test case verifies display of Welcome message in Free Ride Overlay
    PRECONDITIONS: Campaign should be created in Free Ride and Welcome Message should be configured in CMS
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
        EXPECTED: User should be able to login successfully and Free Ride Banner is displayed to the user
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

    def test_004_verify_display_of_welcome_message(self):
        """
        DESCRIPTION: Verify display of welcome Message
        EXPECTED: welcome Message should be displayed in Free Ride Overlay screen
        """
        pass

    def test_005_verify_the_content_in_welcome_message(self):
        """
        DESCRIPTION: Verify the content in welcome Message
        EXPECTED: Content in Welcome Message should be displayed as per the CMS configurations from 'Welcome Message' field in Questions section in campaign
        """
        pass
