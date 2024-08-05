import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C61619005_Verify_the_display_of_Images_on_Highlight_Carousal(Common):
    """
    TR_ID: C61619005
    NAME: Verify the display of Images on Highlight Carousal
    DESCRIPTION: This test case verifies display of image on
    DESCRIPTION: * Highlight Carousal
    PRECONDITIONS: 1: User should have access to CMS
    PRECONDITIONS: 2: Highlight Carousal should be configured with Football event in CMS
    PRECONDITIONS: **CMS CONFIGURATIONS**
    PRECONDITIONS: CMS > BYB > ASSET MANAGEMENT > CREATE ASSET MANAGAMENT
    """
    keep_browser_open = True

    def test_001_asset_management_is_created_for_both_teams_with_image_navigate_to_home_page_and_validate_the_kits_displayed_in_highlight_carousal_section(self):
        """
        DESCRIPTION: **Asset Management is created for both Teams (With Image)**
        DESCRIPTION: * Navigate to Home page and Validate the Kits displayed in Highlight Carousal section
        EXPECTED: **Display on Highlight Carosal= ON**
        EXPECTED: (Both Teams should be ON)
        EXPECTED: * User should be displayed with Images uploaded in CMS before the Team Names
        EXPECTED: **Display on Highlight Carosal= OFF**
        EXPECTED: (If any one Team is OFF or both Teams OFF)
        EXPECTED: * User should be displayed with Crest Colors configured in CMS (Primary & Secondary Colors)
        """
        pass

    def test_002_asset_management_is_created_for_both_teams_only_one_team_has_image_navigate_to_home_page_and_validate_the_kits_displayed_in_highlight_carousal_section(self):
        """
        DESCRIPTION: **Asset Management is created for both Teams (Only One Team has Image)**
        DESCRIPTION: * Navigate to Home page and Validate the Kits displayed in Highlight Carousal section
        EXPECTED: * User should be displayed with Crest Colors configured in CMS (Primary & Secondary Colors)
        """
        pass

    def test_003_asset_management_is_created_for_only_one_team_navigate_to_home_page_and_validate_the_kits_displayed_in_highlight_carousal_section(self):
        """
        DESCRIPTION: **Asset Management is created for only one Team**
        DESCRIPTION: * Navigate to Home page and Validate the Kits displayed in Highlight Carousal section
        EXPECTED: * Default Images should be displayed from the Asset Folder
        """
        pass

    def test_004_asset_management_is_created_for_both_teams_no_image_navigate_to_home_page_and_validate_the_kits_displayed_in_highlight_carousal_section(self):
        """
        DESCRIPTION: **Asset Management is created for both Teams (No Image)**
        DESCRIPTION: * Navigate to Home page and Validate the Kits displayed in Highlight Carousal section
        EXPECTED: * User should be displayed with Crest Colors configured in CMS (Primary & Secondary Colors)
        """
        pass

    def test_005_asset_management_is_not_created_for_both_teams_navigate_to_home_page_and_validate_the_kits_displayed_in_highlight_carousal_section(self):
        """
        DESCRIPTION: **Asset Management is NOT created for both Teams**
        DESCRIPTION: * Navigate to Home page and Validate the Kits displayed in Highlight Carousal section
        EXPECTED: * Default Images should be displayed from the Asset Folder
        """
        pass

    def test_006_default_images_are_not_available_in_asset_folder_navigate_to_home_page_and_validate_the_kits_displayed_in_highlight_carousal_section(self):
        """
        DESCRIPTION: **Default Images are not available in Asset Folder**
        DESCRIPTION: * Navigate to Home page and Validate the Kits displayed in Highlight Carousal section
        EXPECTED: * No Images or crest should be displayed before the Team Names
        """
        pass

    def test_007_validate_the_above_highlight_carousal_in_event_hub_sport_landing_pages_type_id_and_event_id(self):
        """
        DESCRIPTION: Validate the above Highlight Carousal in Event Hub, Sport Landing pages (Type ID and Event ID)
        EXPECTED: 
        """
        pass
