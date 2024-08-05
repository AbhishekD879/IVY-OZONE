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
class Test_C29378_CMS_Featured__Verify_Active_Upcoming_Disabled_Expired_Modules_changing_grid_depending_on_Published_time(Common):
    """
    TR_ID: C29378
    NAME: CMS: Featured - Verify Active/Upcoming/Disabled/Expired Modules changing grid depending on Published time
    DESCRIPTION: This test case verifies Active/Upcoming/Disabled/Expired Modules changing grid depending on Published time
    PRECONDITIONS: 1) Featured Modules created in CMS:
    PRECONDITIONS: * At least 1 Active (Published time within current time)
    PRECONDITIONS: * At least 1 Upcoming ('Visible from' is in future)
    PRECONDITIONS: * At least 1 Disabled
    PRECONDITIONS: * At least 1  Expired ('Visible to' is in past)
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3)
    PRECONDITIONS: * Modules where **'Enabled'** option is checked **AND** where current date and time are **within** time interval set in 'Visible from', 'Visible to' fields are displayed within **'Active'** group (modules that are published on front-end)
    PRECONDITIONS: * Modules where values set in 'Visible from', 'Visible to' fields are from the past are displayed within **'Expired'** group
    PRECONDITIONS: * Modules where **'Enabled'** option is **UNchecked AND** where current date and time are within time interval set in 'Visible from', 'Visible to' fields are displayed within **'Disabled'** group
    PRECONDITIONS: * Modules where values set in 'Visible from', 'Visible to' fields are from the future are displayed within **'Upcoming'** group
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_tab_modules_page(self):
        """
        DESCRIPTION: Go to CMS -> 'Featured Tab Modules' page
        EXPECTED: 
        """
        pass

    def test_002_verify_modules_list_displayed_on_the_page(self):
        """
        DESCRIPTION: Verify modules list displayed on the page
        EXPECTED: Modules are displayed within three groups on the same page in respective order:
        EXPECTED: *   Active
        EXPECTED: *   Upcoming
        EXPECTED: *   Disabled
        EXPECTED: *   Expired
        """
        pass

    def test_003_choose_module_from_upcoming_grid___wait_till_it_should_be_published(self):
        """
        DESCRIPTION: Choose module from 'Upcoming' grid -> Wait till it should be published
        EXPECTED: Module is moved from 'Upcoming' to 'Active' grid
        """
        pass

    def test_004_choose_module_from_active_grid___wait_till_its_publishing_time_ends(self):
        """
        DESCRIPTION: Choose module from 'Active' grid -> Wait till it's publishing time ends
        EXPECTED: Module is moved from 'Active' to 'Expired' grid
        """
        pass

    def test_005_enable_a_module_from_disabled_grid_from_module_edit_page(self):
        """
        DESCRIPTION: Enable a module from 'Disabled' grid (from Module edit page)
        EXPECTED: Module is moved to 'Active' grid
        """
        pass

    def test_006_choose_module_from_disabled_grid___wait_till_its_publishing_time_ends(self):
        """
        DESCRIPTION: Choose module from 'Disabled' grid -> Wait till it's publishing time ends
        EXPECTED: Module is moved from 'Disabled' to 'Expired' grid
        """
        pass
