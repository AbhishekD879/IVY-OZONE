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
class Test_C62782214_Verify_display_of_data_fields_in_Splash_Page_of_CMS(Common):
    """
    TR_ID: C62782214
    NAME: Verify display of data fields in Splash Page of CMS
    DESCRIPTION: This test case verifies all the data fields displayed in Splash home page in Free Ride menu in CMS
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

    def test_002_validate_the_display_of_free_ride_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of 'Free Ride' tab in left side menu of CMS
        EXPECTED: User should be able to view the 'Free Ride' tab
        """
        pass

    def test_003_click_onfree_ride_tab(self):
        """
        DESCRIPTION: Click on 'Free Ride' tab
        EXPECTED: * User should be able to click on 'Free Ride' tab
        EXPECTED: * Sub Menu list of item/s should be displayed
        """
        pass

    def test_004_validate_the_display_of_splash_page_in_sub_menu_list_of_items(self):
        """
        DESCRIPTION: Validate the display of 'Splash Page' in Sub Menu list of item/s
        EXPECTED: User should be able to view Splash Page
        """
        pass

    def test_005_click_on_splash_page_from_the_sub_menu(self):
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
