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
class Test_C65940593_Verify_Quick_links_for_Pre_and_Post_login_Users(Common):
    """
    TR_ID: C65940593
    NAME: Verify Quick links for Pre and Post login Users
    DESCRIPTION: This test case is to validate Quick links for Pre and Post login Users
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

    def test_002_verify_quick_links_for_pre_and_post_login_users(self):
        """
        DESCRIPTION: Verify Quick links for Pre and Post login Users
        EXPECTED: Quicklinks should  be displayed for Pre and Post login Users
        """
        pass
