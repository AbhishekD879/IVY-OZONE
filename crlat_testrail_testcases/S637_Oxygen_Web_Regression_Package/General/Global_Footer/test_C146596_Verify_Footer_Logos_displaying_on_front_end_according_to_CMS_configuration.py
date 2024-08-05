import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C146596_Verify_Footer_Logos_displaying_on_front_end_according_to_CMS_configuration(Common):
    """
    TR_ID: C146596
    NAME: Verify Footer Logos displaying on front-end according to CMS configuration
    DESCRIPTION: This test case verifies displaying of Footer Logos configured via CMS on front-end.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_menus_section___footer_logos(self):
        """
        DESCRIPTION: Go to Menus section -> Footer Logos
        EXPECTED: Footer Logos page is opened
        """
        pass

    def test_003_create_new_footer_logo(self):
        """
        DESCRIPTION: Create new Footer Logo
        EXPECTED: * New Footer Logo is created successfully
        EXPECTED: * Detailed view of created page is opened
        """
        pass

    def test_004_upload_file_of_png_format_in_png_file_field_using_upload_file_button(self):
        """
        DESCRIPTION: Upload file of 'png' format in 'PNG file' field using 'Upload File' button
        EXPECTED: Image is uploaded successfully
        """
        pass

    def test_005_upload_file_of_svg_format_in_svg_file_field_using_upload_file_button(self):
        """
        DESCRIPTION: Upload file of 'svg' format in 'SVG file' field using 'Upload File' button
        EXPECTED: Image is uploaded successfully
        """
        pass

    def test_006_untick_inactive_checkbox(self):
        """
        DESCRIPTION: Untick 'Inactive' checkbox
        EXPECTED: 'Inactive' checkbox is unticked
        """
        pass

    def test_007_load_oxygen_application_on_desktop_and_scroll_page_down(self):
        """
        DESCRIPTION: Load Oxygen application on Desktop and scroll page down
        EXPECTED: 
        """
        pass

    def test_008_verify_previously_created_footer_logo(self):
        """
        DESCRIPTION: Verify previously created Footer Logo
        EXPECTED: New Footer Logo is displayed
        """
        pass

    def test_009_back_to_cms___menus_section___footer_logos(self):
        """
        DESCRIPTION: Back to CMS -> Menus section -> Footer Logos
        EXPECTED: 
        """
        pass

    def test_010_tick_inactive_checkbox(self):
        """
        DESCRIPTION: Tick 'Inactive' checkbox
        EXPECTED: 'Inactive' checkbox is ticked
        """
        pass

    def test_011_back_to_oxygen_application_and_scroll_page_down(self):
        """
        DESCRIPTION: Back to Oxygen application and scroll page down
        EXPECTED: New Footer Logo is NOT displayed
        """
        pass

    def test_012_repeat_steps_1_12_for_mobile(self):
        """
        DESCRIPTION: Repeat steps 1-12 for Mobile
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_1_12_for_tablet(self):
        """
        DESCRIPTION: Repeat steps 1-12 for Tablet
        EXPECTED: 
        """
        pass
