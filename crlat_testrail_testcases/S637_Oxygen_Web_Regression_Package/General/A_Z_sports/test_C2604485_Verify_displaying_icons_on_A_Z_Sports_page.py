import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2604485_Verify_displaying_icons_on_A_Z_Sports_page(Common):
    """
    TR_ID: C2604485
    NAME: Verify displaying icons on 'A-Z' Sports page
    DESCRIPTION: This test case verifies displaying icons for 'A-Z' Sport page
    PRECONDITIONS: 1. Sports are configured in CMS: Sports Pages > Sport Categories
    PRECONDITIONS: 2. 'Top Sports' are configured in CMS for some Sports e.g. Football, Horse Racing, Greyhounds
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Is Top Sport' check box is checked)
    PRECONDITIONS: 3. 'A-Z Sports' is configured in CMS for some Sports e.g. Basketball, Football, Greyhounds, Horse Racing etc
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 4. Icons are uploaded in CMS for Sports with checked 'Show in AZ' & 'Top Sports' check box e.g. Basketball, Football, Greyhounds, Horse Racing (Sports Pages > Sport Categories > <Sport> 'SVG Filename')
    PRECONDITIONS: 5. 'All Sports' page is opened (A-Z Sports)
    """
    keep_browser_open = True

    def test_001_verify_availability_of_icons_in_a_z_sports_section(self):
        """
        DESCRIPTION: Verify availability of icons in 'A-Z Sports' section
        EXPECTED: Icons uploaded in CMS are displayed next to each sport in 'A-Z Sports' section
        """
        pass

    def test_002_in_cms__navigate_to_sports_pages__sport_categories__sport_with_checked_show_in_az__is_top_sport_boxes_eg_football__click_on_remove_file_next_to_svg_filename_of_an_uploaded_icon__save_changes(self):
        """
        DESCRIPTION: In CMS:
        DESCRIPTION: - Navigate to Sports Pages > Sport Categories > <Sport> with checked 'Show in AZ' & 'Is Top Sport' boxes e.g. Football
        DESCRIPTION: - Click on 'Remove File' next to 'SVG Filename' of an uploaded icon
        DESCRIPTION: - Save changes
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_003_verify_an_icon_for_a_sport_from_step_2_eg_football_in_az_sports_section(self):
        """
        DESCRIPTION: Verify an icon for a Sport from Step 2 (e.g. Football) in 'AZ Sports' section
        EXPECTED: Icon (hardcoded) is displayed next to a Sport from Step 2 (e.g. Football) in 'AZ Sports' section
        """
        pass

    def test_004_in_cms__navigate_to_sports_pages__sport_categories__sport_with_checked_show_in_az__is_top_sport_boxes_eg_football__upload_an_svg_icon_back_for_svg_filename__save_changes(self):
        """
        DESCRIPTION: In CMS:
        DESCRIPTION: - Navigate to Sports Pages > Sport Categories > <Sport> with checked 'Show in AZ' & 'Is Top Sport' boxes e.g. Football
        DESCRIPTION: - Upload an svg icon back for 'SVG Filename'
        DESCRIPTION: - Save changes
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_in_app_verify_availability_of_an_icon_for_a_sport_from_step_4_eg_football_in_az_sports_section(self):
        """
        DESCRIPTION: In app: Verify availability of an icon for a Sport from Step 4 (e.g. Football) in 'AZ Sports' section
        EXPECTED: Icon uploaded in CMS is displayed next to the Sport from Step 4 (e.g. Football) in 'AZ Sports' section
        """
        pass

    def test_006_repeat_steps_1_5__verify_icons_next_to_sports_in_top_sports_section(self):
        """
        DESCRIPTION: Repeat steps 1-5 > Verify icons next to Sports in 'Top Sports' section
        EXPECTED: Icons are NOT displayed next to sports in 'Top Sports' section
        """
        pass
