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
class Test_C62782281_Verify_display_of_Splash_Page_in_FE_as_per_CMS_config(Common):
    """
    TR_ID: C62782281
    NAME: Verify display of Splash Page in FE as per CMS config
    DESCRIPTION: This test case verifies display of Splash Page in FE as per CMS configurations
    PRECONDITIONS: 1. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 2. Splash Page for Free Ride should be created in CMS
    """
    keep_browser_open = True

    def test_001_click_on_launch_banner_for_free_ride_in_homepage(self):
        """
        DESCRIPTION: Click on 'Launch Banner' for Free Ride in Homepage
        EXPECTED: Free Ride Splash page should be displayed
        """
        pass

    def test_002_verify_the_data_in_below_fields_splash_page_welcome_message_tc_button_title(self):
        """
        DESCRIPTION: Verify the data in below fields
        DESCRIPTION: * Splash page welcome message
        DESCRIPTION: * T&C
        DESCRIPTION: * Button Title
        EXPECTED: Data in below fields should be displayed as per the CMS configuration
        EXPECTED: * Splash page welcome message
        EXPECTED: * T&C
        EXPECTED: * Button Title
        """
        pass

    def test_003_verify_the_below_image_uploads_in_splash_page_launch_banner_splash_page_image_free_ride_text_image(self):
        """
        DESCRIPTION: Verify the below image uploads in Splash page
        DESCRIPTION: * Launch Banner
        DESCRIPTION: * Splash Page Image
        DESCRIPTION: * Free Ride Text Image
        EXPECTED: Uploaded images should be displayed as per the CMS configurations
        """
        pass
