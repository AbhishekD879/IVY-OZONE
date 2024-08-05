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
class Test_C62782219_Verify_data_validations_of_the_fields_in_Splash_Page_of_CMS(Common):
    """
    TR_ID: C62782219
    NAME: Verify data validations of the fields in Splash Page of CMS
    DESCRIPTION: This test case verifies data validation of the fields displayed in Splash home page in Free Ride menu in CMS
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Free Ride menu should be configured in CMS
    PRECONDITIONS: ***How to Configure Menu Item***
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: Free Ride
    PRECONDITIONS: Path: /Free Ride
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: Splash Page
    PRECONDITIONS: Path: /Splash Page
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_onfree_ride_tab(self):
        """
        DESCRIPTION: Click on 'Free Ride' tab
        EXPECTED: * Splash Page should be displayed on sub menu list/s
        """
        pass

    def test_003_click_on_splash_page_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Splash page from the sub menu
        EXPECTED: User should be navigate to Splash page and the below fields should be displayed
        EXPECTED: * Launch Banner
        EXPECTED: * Splash Page Image
        EXPECTED: * Free Ride Text Image
        EXPECTED: * Splash page welcome message
        EXPECTED: * T&C
        EXPECTED: * Button Title
        """
        pass

    def test_004_verify_data_validations_of_the_fields(self):
        """
        DESCRIPTION: Verify data validations of the fields
        EXPECTED: * Launch Banner : Able to upload Image or enter URL
        EXPECTED: * Splash Page Image : Able to upload Image
        EXPECTED: * Free Ride Text Image : Able to upload Image
        EXPECTED: * Splash page welcome Message - Allows max 200 chars
        EXPECTED: * T&C - Allows max 200 chars
        EXPECTED: * Button Title - Allows max 30 chars
        """
        pass
