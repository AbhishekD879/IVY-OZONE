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
class Test_C146287_Verify_Module_Header_displaying_when_Module_is_created_by_Selection_ID(Common):
    """
    TR_ID: C146287
    NAME: Verify Module Header displaying when Module is created by Selection ID
    DESCRIPTION: This test case verifies Module Header displaying when Module contains Special/Enhanced offers.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) Create Featured Module by 'Selection ID' and choose for 'Badge' parameter None/Special/Enhanced value in CMS.
    PRECONDITIONS: 2) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is loaded
        EXPECTED: * Featured section is present on the page
        """
        pass

    def test_002_select_featured_module_by_selection_id_with_badge_parameter_value__none_set_in_cmsverify_header_displaying_for_the_module(self):
        """
        DESCRIPTION: Select Featured Module by 'Selection ID' with 'Badge' parameter value = 'None' (set in CMS)
        DESCRIPTION: Verify Header displaying for the Module
        EXPECTED: **For Mobile/Tablet and Desktop:**
        EXPECTED: * Header background color is the same as for all other Featured Tab Modules types
        EXPECTED: * Any additional badges are not displayed in the Header
        EXPECTED: * Module is expandable/collapsible
        """
        pass

    def test_003_select_featured_module_by_selection_id_with_badge_parameter_value__special_set_in_cmsverify_header_displaying_for_the_module(self):
        """
        DESCRIPTION: Select Featured Module by Selection ID with 'Badge' parameter value = 'Special' (set in CMS)
        DESCRIPTION: Verify Header displaying for the Module
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Header background color is the same as for all other Featured Tab Modules types
        EXPECTED: * 'Special' badge is displayed in the Header on the right side
        EXPECTED: * Module is expandable/collapsible
        EXPECTED: **For Desktop:**
        EXPECTED: * Header background color is the same as for all other Featured Tab Modules types
        EXPECTED: * 'SPECIAL' badge is displayed in the Header on the left side
        EXPECTED: * Module is NOT expandable/collapsible
        """
        pass

    def test_004_select_featured_module_by_selection_id_with_badge_parameter_value__enhanced_set_in_cmsverify_header_displaying_for_the_module(self):
        """
        DESCRIPTION: Select Featured Module by Selection ID with 'Badge' parameter value = 'Enhanced' (set in CMS)
        DESCRIPTION: Verify Header displaying for the Module
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Header background color is the same as for all other Featured Tab Modules types
        EXPECTED: * 'Enhanced' badge is displayed in the Header on the right side
        EXPECTED: * Module is expandable/collapsible
        EXPECTED: **For Desktop:**
        EXPECTED: * Header background color is the same as for all other Featured Tab Modules types
        EXPECTED: * 'ENHANCED' badge is displayed in the Header on the left side
        EXPECTED: * Module is NOT expandable/collapsible
        """
        pass

    def test_005_verify_featured_tab_module_with_any_other_select_events_by_parameter_value(self):
        """
        DESCRIPTION: Verify Featured Tab Module with any other 'Select Events by' parameter value
        EXPECTED: **For Mobile/Tablet and Desktop:**
        EXPECTED: * Header background color is the same as for all other Featured Tab Modules types
        EXPECTED: * Any additional badges are not displayed in the Header
        EXPECTED: * Module is expandable/collapsible
        """
        pass
