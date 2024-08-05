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
class Test_C50044_Verify_functionality_of_Maintenance_Page_configured_via_CMS(Common):
    """
    TR_ID: C50044
    NAME: Verify functionality of Maintenance Page configured via CMS
    DESCRIPTION: This test case verifies functionality of showing the module in application for Maintenance Section configured via CMS
    DESCRIPTION: Test case is outdated on step #10, it is a png file that should be accepted instead of jpg.
    PRECONDITIONS: CMS > System configuration > Config > maintenancePage > enabled = true
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_maintenance_section(self):
        """
        DESCRIPTION: Go to Maintenance section
        EXPECTED: Maintenance section is opened
        """
        pass

    def test_003_click_on_create_maintenance_page_button(self):
        """
        DESCRIPTION: Click on 'Create Maintenance Page' button
        EXPECTED: 'Create a new Maintenance Page' pop-up appears
        """
        pass

    def test_004_fill_in_all_required_fields_and_click_on_create_button(self):
        """
        DESCRIPTION: Fill in all required fields and click on 'Create' button
        EXPECTED: New Maintenance page appears in the list of items
        """
        pass

    def test_005_open_previously_created_maintenance_page(self):
        """
        DESCRIPTION: Open previously created Maintenance page
        EXPECTED: Maintenance page is opened
        """
        pass

    def test_006_enter_past_time_in_validity_period_start_field_and_future_time_in_validity_period_end_field(self):
        """
        DESCRIPTION: Enter past time in 'Validity Period Start' field and future time in 'Validity Period End' field
        EXPECTED: 
        """
        pass

    def test_007_tick_checkboxes_for_mobile_tablet_and_desktop(self):
        """
        DESCRIPTION: Tick checkboxes for 'Mobile', 'Tablet' and 'Desktop'
        EXPECTED: 
        """
        pass

    def test_008_click_on_save_button(self):
        """
        DESCRIPTION: Click on 'Save' button
        EXPECTED: 'Your changes have been saved' successful message is displayed
        """
        pass

    def test_009_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Dark background is displayed on Mobile/Tablet/Desktop
        """
        pass

    def test_010_back_to_cmsload_image_that_does_not_have_jpeg_format_and_click_on_save_button(self):
        """
        DESCRIPTION: Back to CMS.
        DESCRIPTION: Load image that does NOT have 'jpeg' format and click on 'Save' button
        EXPECTED: 'Filename uploaded failed - Unsupported File Type: image/format' error message appears
        """
        pass

    def test_011_load_image_that_has_jpeg_format_and_click_on_save_button(self):
        """
        DESCRIPTION: Load image that has 'jpeg' format and click on 'Save' button
        EXPECTED: 'Your changes have been saved' successful message is displayed
        """
        pass

    def test_012_enter_the_future_time_in_validity_period_start_field_for_previously_created_maintenance_page_and_save_changes(self):
        """
        DESCRIPTION: Enter the future time in 'Validity Period Start' field for previously created Maintenance page and save changes
        EXPECTED: 'Your changes have been saved' successful message is displayed
        """
        pass

    def test_013_back_to_oxygen_applicationrefresh_the_page_and_wait_time_that_was_set_in_step_12(self):
        """
        DESCRIPTION: Back to Oxygen application.
        DESCRIPTION: Refresh the page and wait time that was set in step 12
        EXPECTED: * Page is refreshed and Maintenance page is displayed on Mobile/Tablet/Desktop
        EXPECTED: * Image uploaded in step 12 is displayed as  Maintenance Splash Banner
        """
        pass

    def test_014_back_to_cmsenter_the_future_time_in_validity_period_end_field_for_previously_created_maintenance_page_and_save_changes(self):
        """
        DESCRIPTION: Back to CMS.
        DESCRIPTION: Enter the future time in 'Validity Period End' field for previously created Maintenance page and save changes
        EXPECTED: 'Your changes have been saved' successful message is displayed
        """
        pass

    def test_015_back_to_oxygen_applicationrefresh_the_page_and_wait_time_that_was_set_in_step_14(self):
        """
        DESCRIPTION: Back to Oxygen application.
        DESCRIPTION: Refresh the page and wait time that was set in step 14
        EXPECTED: * Page is refreshed and Maintenance page disappears on Mobile/Tablet/Desktop
        EXPECTED: * Homepage is loaded on Mobile/Tablet/Desktop
        """
        pass

    def test_016_back_to_cmsenter_past_time_in_validity_period_start_field_and_future_time_in_validity_period_end_field(self):
        """
        DESCRIPTION: Back to CMS.
        DESCRIPTION: Enter past time in 'Validity Period Start' field and future time in 'Validity Period End' field
        EXPECTED: 
        """
        pass

    def test_017_enter_data_in_target_uri_field_and_save_changes(self):
        """
        DESCRIPTION: Enter data in 'Target Uri' field and save changes
        EXPECTED: 'Your changes have been saved' successful message is displayed
        """
        pass

    def test_018_back_to_oxygen_applicationrefresh_the_page_and_click_on_maintenance_splash_banner(self):
        """
        DESCRIPTION: Back to Oxygen application.
        DESCRIPTION: Refresh the page and click on Maintenance Splash Banner
        EXPECTED: * Maintenance page is displayed on Mobile/Tablet/Desktop
        EXPECTED: * User is redirected to the page that was set in step 17
        """
        pass

    def test_019_back_to_cmsuntick_checkbox_for_tablet_and_save_changes(self):
        """
        DESCRIPTION: Back to CMS.
        DESCRIPTION: Untick checkbox for tablet and save changes
        EXPECTED: 'Your changes have been saved' successful message is displayed
        """
        pass

    def test_020_load__oxygen_application_on_tablet(self):
        """
        DESCRIPTION: Load  Oxygen application on tablet
        EXPECTED: * Homepage is loaded on Tablet
        EXPECTED: * Maintenance page is NOT displayed on Tablet
        EXPECTED: * Maintenance page is displayed on Mobile and Desktop
        """
        pass

    def test_021_repeat_steps_19_20_for_mobile(self):
        """
        DESCRIPTION: Repeat steps 19-20 for Mobile
        EXPECTED: * Homepage is loaded on Mobile
        EXPECTED: * Maintenance page is NOT displayed on Mobile
        EXPECTED: * Maintenance page is displayed on Tablet and Desktop
        """
        pass

    def test_022_repeat_steps_19_20_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 19-20 for Desktop
        EXPECTED: * Homepage is loaded on Desktop
        EXPECTED: * Maintenance page is NOT displayed on Desktop
        EXPECTED: * Maintenance page is displayed on Tablet and Tablet
        """
        pass
