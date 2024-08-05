import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C65940591_Verify_display_of_Quick_link_for_Universal_segmentation_configuration(Common):
    """
    TR_ID: C65940591
    NAME: Verify display of Quick link for Universal segmentation configuration
    DESCRIPTION: This test case is to validate Quick link for Universal segmentation configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Navigate to Sportspage->Home-> Module order ->quick link-> Click on create quick link button
    PRECONDITIONS: 3) Check the Active check box
    PRECONDITIONS: 4) Enter the valid data for following fields
    PRECONDITIONS: a. Enter title
    PRECONDITIONS: b. Enter destination
    PRECONDITIONS: c. Select start and end date.
    PRECONDITIONS: d.Select SVG icon
    PRECONDITIONS: e.Select segment (by default universal will be selected)
    PRECONDITIONS: f.Click on create button.
    PRECONDITIONS: Quick link should be in running state.
    """
    keep_browser_open = True

    def test_001_launch_the_application_on_desktop(self):
        """
        DESCRIPTION: Launch the application on desktop
        EXPECTED: Application should be loaded successfully.
        """
        pass

    def test_002_verify_quick_link_for_universal_segmentation_configuration(self):
        """
        DESCRIPTION: Verify Quick link for Universal segmentation configuration
        EXPECTED: Quicklinks should  be displayed on for all users.
        """
        pass
