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
class Test_C2496193_CMS_Featured__Verify_Active_Upcoming_Disabled_Expired_grid_view(Common):
    """
    TR_ID: C2496193
    NAME: CMS: Featured - Verify Active/Upcoming/Disabled/Expired grid view
    DESCRIPTION: This test case verifies view of 'Featured Tab Modules' page
    PRECONDITIONS: 1) There are Featured Modules created in CMS:
    PRECONDITIONS: * Active (Published time within current time)
    PRECONDITIONS: * Upcoming ('Visible from' is in future)
    PRECONDITIONS: * Disabled
    PRECONDITIONS: * Expired ('Visible to' is in past)
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3)
    PRECONDITIONS: * Modules where **'Enabled'** option is checked **AND** where current date and time are **within** time interval set in 'Visible from', 'Visible to' fields are displayed within **'Active'** group (modules that are published on front-end)
    PRECONDITIONS: * Modules where values set in 'Visible from', 'Visible to' fields are from the past are displayed within **'Expired'** group
    PRECONDITIONS: * Modules where **'Enabled'** option is **UNchecked AND** where current date and time are within time interval set in 'Visible from', 'Visible to' fields are displayed within **'Disabled'** group
    PRECONDITIONS: * Modules where values set in 'Visible from', 'Visible to' fields are from the future are displayed within **'Upcoming'** group
    """
    keep_browser_open = True

    def test_001_verify_grids_order(self):
        """
        DESCRIPTION: Verify Grids order
        EXPECTED: Grids are located in such order:
        EXPECTED: * Active
        EXPECTED: * Upcoming
        EXPECTED: * Disabled
        EXPECTED: * Expired
        """
        pass

    def test_002_verify_groups_headers(self):
        """
        DESCRIPTION: Verify groups' headers
        EXPECTED: Groups' headers have different backgrounds (Active - default green, Upcoming - bright green, Disabled - red, Expired - orange)
        """
        pass
