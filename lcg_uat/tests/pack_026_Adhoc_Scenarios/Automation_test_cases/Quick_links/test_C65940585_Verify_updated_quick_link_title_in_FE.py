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
class Test_C65940585_Verify_updated_quick_link_title_in_FE(Common):
    """
    TR_ID: C65940585
    NAME: Verify updated quick link title in FE
    DESCRIPTION: This test case is to validate the display of updated quick link title on FE
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

    def test_003_in_cms_now_update_the_title_of_the_quick_link(self):
        """
        DESCRIPTION: In CMS, now update the title of the quick link
        EXPECTED: Title should be updated successfully.
        """
        pass

    def test_004_validate_the_updated_quick_link_title_is_displayed_in_fe(self):
        """
        DESCRIPTION: Validate the updated quick link title is displayed in FE
        EXPECTED: Updated quick link title should be displayed on FE
        """
        pass
