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
class Test_C62782220_Verify_CMS_configurations_for_creating_Editing_Splash_Page(Common):
    """
    TR_ID: C62782220
    NAME: Verify CMS configurations for creating & Editing Splash Page
    DESCRIPTION: This test case verifies CMS configurations for creating and editing Splash Page in Free Ride menu
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

    def test_004_enter_data_and_upload_image(self):
        """
        DESCRIPTION: Enter data and upload image
        EXPECTED: User should be able to enter the data and upload image
        """
        pass

    def test_005_click_on_save(self):
        """
        DESCRIPTION: Click on Save
        EXPECTED: Save option should be enabled and user should save the data successfully
        """
        pass

    def test_006_verify_the_save_button_after_successfully_splash_page_creation(self):
        """
        DESCRIPTION: Verify the save button after successfully Splash page creation
        EXPECTED: Save button should be disabled
        """
        pass

    def test_007_enter_data_in_the_data_fields_and_verify_the_save_button(self):
        """
        DESCRIPTION: Enter data in the data fields and verify the save button
        EXPECTED: * User should be able to enter the data and save button is enabled
        EXPECTED: * Entered data should be updated on clicking on save button
        """
        pass

    def test_008_verify_the_display_of_splash_page_screen(self):
        """
        DESCRIPTION: Verify the display of splash page screen
        EXPECTED: Only one Splash page should be displayed
        """
        pass
