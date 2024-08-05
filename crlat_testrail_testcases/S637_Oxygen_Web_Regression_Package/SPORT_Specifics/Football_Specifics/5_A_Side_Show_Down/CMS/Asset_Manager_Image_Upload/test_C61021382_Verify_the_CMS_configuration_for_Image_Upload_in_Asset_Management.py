import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C61021382_Verify_the_CMS_configuration_for_Image_Upload_in_Asset_Management(Common):
    """
    TR_ID: C61021382
    NAME: Verify the CMS configuration for Image Upload in Asset Management
    DESCRIPTION: This test case verifies the display of CMS configurations for Image upload in Asset Management
    PRECONDITIONS: User should have admin roles to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_click_on_byb_section(self):
        """
        DESCRIPTION: Click on BYB section
        EXPECTED: User should be able to Expand BYB section
        """
        pass

    def test_003_click_on_asset_management_section(self):
        """
        DESCRIPTION: Click on Asset Management section
        EXPECTED: * User should be able to view Create Asset Management CTA
        EXPECTED: * Already Created asset Management should be displayed
        EXPECTED: * Image, Image Name and Status Columns should be displayed
        """
        pass

    def test_004_click_on_create_asset_management(self):
        """
        DESCRIPTION: Click on Create Asset Management
        EXPECTED: * Pop-up should be displayed
        """
        pass

    def test_005_add_team_name_sports_id_primary_color_and_secondary_colorclick_on_save(self):
        """
        DESCRIPTION: Add Team Name, Sports ID, Primary Color and Secondary Color
        DESCRIPTION: Click on Save
        EXPECTED: * User should be able to add and save successfully
        EXPECTED: * User should be navigated to edit asset management details page
        """
        pass

    def test_006_validate_the_display_of_team_image_field_and_add_button(self):
        """
        DESCRIPTION: Validate the display of Team Image field and Add button
        EXPECTED: * User should be able to view Team Image Field
        EXPECTED: * Add button should be displayed
        """
        pass

    def test_007_add_image(self):
        """
        DESCRIPTION: Add Image
        EXPECTED: * User should be able to upload supported file successfully
        EXPECTED: * Change button should be displayed
        EXPECTED: * FiveASide Toggle and Highlights Carosal Toggle should be displayed
        EXPECTED: * Toggles should be disabled by default
        """
        pass

    def test_008_validate_the_user_is_able_to_enable_or_disable_fiveaside_toggle_highlights_carousel_toggle(self):
        """
        DESCRIPTION: Validate the User is able to enable or disable
        DESCRIPTION: * FiveASide Toggle
        DESCRIPTION: * Highlights Carousel Toggle
        EXPECTED: * User should be able to enable/ disable
        """
        pass
