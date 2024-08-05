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
class Test_C29412_CMS_Verify_Max_Selections_to_Display(Common):
    """
    TR_ID: C29412
    NAME: CMS: Verify 'Max Selections to Display'
    DESCRIPTION: This test case verifies 'Max Selections to Display' field and it's impact on number of selections that are displayed on front-end
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-6571 CMS: Featured Tab Module - Horse Racing
    DESCRIPTION: *   BMA-7352 CMS: Configure the number of selections to display for a racing event (Grand National)
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_tab_modules(self):
        """
        DESCRIPTION: Go to CMS -> Featured Tab Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_plus_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Tap '+ Create Featured Tab Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_datato_create_module_by_race_typeid(self):
        """
        DESCRIPTION: Fill in all required fields with valid data to create module by** <Race> typeID**
        EXPECTED: 
        """
        pass

    def test_004_set_positive_value_into_max_selections_to_display_field(self):
        """
        DESCRIPTION: Set positive value into '**Max Selections to Display**' field
        EXPECTED: 
        """
        pass

    def test_005_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_006_load_invictus_application_and_verify_number_of_selections_within_each_event_in_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify number of selections within each event in created Module
        EXPECTED: *   Number of selections within each event corresponds to value set in CMS
        EXPECTED: *   If there are less selections in a particular event, show available selections
        """
        pass

    def test_007_go_to_cms_featured_tab_modules___open_created_module_on_the_previous_steps(self):
        """
        DESCRIPTION: Go to CMS->Featured Tab Modules -> open created module on the previous steps
        EXPECTED: 
        """
        pass

    def test_008_set_negative_value_into_max_selections_to_display_field(self):
        """
        DESCRIPTION: Set negative value into '**Max Selections to Display**' field
        EXPECTED: 'Save Module' button in CMS is disabled
        """
        pass

    def test_009_leave_field_max_selections_to_display_blank(self):
        """
        DESCRIPTION: Leave field **'Max Selections to Display'** blank
        EXPECTED: 
        """
        pass

    def test_010_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: There is no restriction on the number of selections that are retrieved. Number of retrieved selections corresponds to number of available selections respectively to all filters set for module
        """
        pass

    def test_011_load_invictus_application_and_verify_number_of_selections_within_each_event_in_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify number of selections within each event in created Module
        EXPECTED: Number of selections corresponds to max number of selections available for each event retrieved in CMS
        """
        pass
