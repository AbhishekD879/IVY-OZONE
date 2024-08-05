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
class Test_C29398_CMS_Verify_Max_Events_to_Display(Common):
    """
    TR_ID: C29398
    NAME: CMS: Verify 'Max Events to Display'
    DESCRIPTION: This test case verifies 'Max Events to Display' field and it's impact on number of events that are displayed on front-end
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___home_modules(self):
        """
        DESCRIPTION: Go to CMS -> Home Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_create_home_module_button(self):
        """
        DESCRIPTION: Tap 'Create Home Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_set_positive_value_into_max_events_to_display_field(self):
        """
        DESCRIPTION: Set positive value into '**Max Events to Display**' field
        EXPECTED: 
        """
        pass

    def test_005_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: Number of retrieved events corresponds to value set in step №4
        """
        pass

    def test_006_load_invictus_application_and_verify_number_of_events_within_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify number of events within created Module
        EXPECTED: Number of events corresponds to value set in CMS
        """
        pass

    def test_007_go_to_cms_home_module_open_created_module_on_the_previous_steps(self):
        """
        DESCRIPTION: Go to CMS->Home Module->open created module on the previous steps
        EXPECTED: 
        """
        pass

    def test_008_set_negative_value_into_max_events_to_display_field(self):
        """
        DESCRIPTION: Set negative value into '**Max Events to Display**' field
        EXPECTED: 
        """
        pass

    def test_009_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: All events are retreived
        """
        pass

    def test_010_leave_field_max_events_to_display_blank(self):
        """
        DESCRIPTION: Leave field **'Max Events to Display'** blank
        EXPECTED: 
        """
        pass

    def test_011_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: There is no restriction on the number of events that are retrieved. Number of retrieved events corresponds to number of available events respectively to all filters set for module
        """
        pass

    def test_012_load_invictus_application_and_verify_number_of_events_within_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify number of events within created Module
        EXPECTED: Number of events corresponds to number of events retrieved in CMS
        """
        pass
