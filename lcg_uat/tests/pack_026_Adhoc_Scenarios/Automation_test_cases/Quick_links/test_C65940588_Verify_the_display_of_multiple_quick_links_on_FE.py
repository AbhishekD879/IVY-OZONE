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
class Test_C65940588_Verify_the_display_of_multiple_quick_links_on_FE(Common):
    """
    TR_ID: C65940588
    NAME: Verify the display of multiple quick links on FE.
    DESCRIPTION: This test case is to validate that Multiple quick links should be displayed on FE as per CMS configuration
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
    PRECONDITIONS: Similarly create multiple quick links and note down there order.
    """
    keep_browser_open = True

    def test_001_launch_mobile_application(self):
        """
        DESCRIPTION: Launch mobile application.
        EXPECTED: Application should be loaded successfully. By default, home page should be loaded.
        """
        pass

    def test_002_verify_the_display_of_all_active_quick_links_on_fe(self):
        """
        DESCRIPTION: Verify the display of all active quick links on FE
        EXPECTED: All the active and running quick links should be displayed on FE.
        EXPECTED: Order of the quick links should be as per CMS
        """
        pass

    def test_003_in_cms_now_change_the_order_of_the_quick_links_in__quick_link_module_page(self):
        """
        DESCRIPTION: In CMS, now change the order of the quick links in  QUICK LINK MODULE page
        EXPECTED: Order should be changed in CMS.
        """
        pass

    def test_004_in_fe_validate_the_order_of_quick_links(self):
        """
        DESCRIPTION: In FE, validate the order of quick links
        EXPECTED: Quicklinks should be displayed in FE as per updated order in CMS
        """
        pass
