import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28648_Favorites_widget_configuration_in_CMS(Common):
    """
    TR_ID: C28648
    NAME: Favorites widget configuration in CMS
    DESCRIPTION: This test case verifies Favorites Widget is CMS configurable
    PRECONDITIONS: 1. User is logged in to CMS
    """
    keep_browser_open = True

    def test_001_go_to_cms_widgets_section(self):
        """
        DESCRIPTION: Go to CMS-Widgets section
        EXPECTED: 
        """
        pass

    def test_002_verify_favoriteswidget_displaying_in_application_appropriately_to_its_order_in_cms(self):
        """
        DESCRIPTION: Verify Favorites widget displaying in application appropriately to its order in CMS
        EXPECTED: Favorites widget in application is dispayed appropriately to its order in CMS
        """
        pass

    def test_003_change_widgets_order_in_cms_and_reload_the_application(self):
        """
        DESCRIPTION: Change widgets order in CMS and reload the application
        EXPECTED: Widgets order is updated in application appropriately to the changes
        """
        pass

    def test_004_open_favoriteswidget_details_page_in_cms(self):
        """
        DESCRIPTION: Open Favorites widget details page in CMS
        EXPECTED: The widget details page is opened with the next elements:
        EXPECTED: *   'Active' checkbox
        EXPECTED: *   'Title' field
        EXPECTED: *   'Type' field (now editable)
        EXPECTED: *   'Columns' drop-down option (Right Column/Left Column/Both)
        EXPECTED: *   'Show Expanded' checkbox
        EXPECTED: *   'Show on Mobile' check box
        EXPECTED: *   'Show on Desktop' check box
        EXPECTED: *   'Show on Tablet' check box
        """
        pass

    def test_005_select_active_checkbox_and_check_that_the_widget_is_displayed_in_the_application_after_saving_the_changes(self):
        """
        DESCRIPTION: Select 'Active' checkbox and check that the widget is displayed in the application after saving the changes
        EXPECTED: *   Widget is displayed when 'Active' checkbox is checked in CMS
        EXPECTED: *   Widget is not displayed when 'Active' checkbox is unchecked in CMS
        """
        pass

    def test_006_for_columns_drop_down_option_should_be_selected_right_column_as_left_column_doesnt_exist_anymore(self):
        """
        DESCRIPTION: For 'Columns' drop-down option should be selected 'Right Column' as 'Left Column' doesn't exist anymore.
        EXPECTED: 
        """
        pass

    def test_007_verify_widget_displaying_in_the_application_according_to_show_expanded_option_settled_in_cms(self):
        """
        DESCRIPTION: Verify widget displaying in the application according to 'Show Expanded' option settled in CMS
        EXPECTED: *   Widget is expanded when 'Show Expanded' checkbox is checked in CMS
        EXPECTED: *   Widget is collapsed when 'Show Expanded' checkbox is unchecked in CMS
        """
        pass

    def test_008_verify_widget_displaying_in_the_application_according_to_display_on_mobiledesktoptablet_option_settled_in_cms(self):
        """
        DESCRIPTION: Verify widget displaying in the application according to Display on Mobile/Desktop/Tablet option settled in CMS
        EXPECTED: *   Widget is displayed on the mobile if 'Show on Mobile' checkbox is selected in CMS
        EXPECTED: *   Widget is displayed on the desktop if 'Show on Desktop' checkbox is selected in CMS
        EXPECTED: *   Widget is displayed on the tablet if 'Show on Tablet' checkbox is selected in CMS
        """
        pass
