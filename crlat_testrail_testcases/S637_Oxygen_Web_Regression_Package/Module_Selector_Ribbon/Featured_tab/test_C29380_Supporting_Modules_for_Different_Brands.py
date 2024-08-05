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
class Test_C29380_Supporting_Modules_for_Different_Brands(Common):
    """
    TR_ID: C29380
    NAME: Supporting Modules for Different Brands
    DESCRIPTION: This test case verifies Supporting Modules for Different Brands.
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

    def test_002_tap_new_module_button(self):
        """
        DESCRIPTION: Tap 'New module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_go_to_publish_to_channels_section(self):
        """
        DESCRIPTION: Go to '**Publish to Channels**' section
        EXPECTED: *   List of supported brands is shown
        EXPECTED: *   It is possible to select/unselect with the check-box
        """
        pass

    def test_005_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_006_load_application_for_eachbrand(self):
        """
        DESCRIPTION: Load application for each brand
        EXPECTED: Module is shown / not shown depending on selected / unselected checkbox
        """
        pass
