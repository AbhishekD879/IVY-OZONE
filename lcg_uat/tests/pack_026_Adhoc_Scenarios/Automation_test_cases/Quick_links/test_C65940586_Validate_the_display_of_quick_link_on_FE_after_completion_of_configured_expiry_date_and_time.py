import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65940586_Validate_the_display_of_quick_link_on_FE_after_completion_of_configured_expiry_date_and_time(Common):
    """
    TR_ID: C65940586
    NAME: Validate the display of quick link on FE after completion of configured expiry date and time.
    DESCRIPTION: This test case is to verify that Quick link should not be displayed on FE after completion of end date and time
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
        """
        pass

    def test_003_wait_for_the_completion_of_configured_quick_link_end_date_and_time(self):
        """
        DESCRIPTION: Wait for the completion of configured quick link end date and time.
        EXPECTED: Quick link should be displayed until the completion of end date and time
        """
        pass

    def test_004_validate_the_display_of_quick_link_on_fe(self):
        """
        DESCRIPTION: Validate the display of quick link on FE
        EXPECTED: Quick link should not be displayed after completion of configured end time
        """
        pass
