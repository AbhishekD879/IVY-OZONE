import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65940583_Verify_display_of_configured_SVG_icon_for_quick_link(Common):
    """
    TR_ID: C65940583
    NAME: Verify display of configured SVG icon for quick link
    DESCRIPTION: This test case is to validate display of configured SVG icon for quick link
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
    """
    keep_browser_open = True

    def test_001_launch_mobile_application(self):
        """
        DESCRIPTION: Launch mobile application.
        EXPECTED: Application should be loaded successfully. By default, home page should be loaded.
        """
        pass

    def test_002_verify_display_of_created_quick_link_on_fe(self):
        """
        DESCRIPTION: Verify display of created quick link on FE
        EXPECTED: Quick link should be displayed.
        EXPECTED: Quick link should not be displayed if current system date and time is less then configured date and time
        """
        pass

    def test_003_validate_display_of_svg_icon_of_configured_quick_link(self):
        """
        DESCRIPTION: Validate display of SVG icon of configured quick link
        EXPECTED: SVG icon should be displayed as per CMS configuration.
        """
        pass
