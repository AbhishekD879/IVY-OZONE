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
class Test_C62969674_Verify_only_enabled_modules_are_displayed_in_module_drop_down_list(Common):
    """
    TR_ID: C62969674
    NAME: Verify only enabled modules are displayed in module drop down list
    DESCRIPTION: This test case verifies module drop down list items
    PRECONDITIONS: 1) User should have admin access to BI reports
    PRECONDITIONS: 2) CMS config should be done for all modules
    PRECONDITIONS: 3) Segments should be created in Optimove and respective config should added to CMS modules
    """
    keep_browser_open = True

    def test_001_login_to_bi_reports_with_admin_access_andnavigate_to_retro_reports_tbd(self):
        """
        DESCRIPTION: Login to BI reports with admin access and navigate to retro Reports (TBD)
        EXPECTED: Retro Reports page should display
        """
        pass

    def test_002_click_on_module_drop_down_and_verify(self):
        """
        DESCRIPTION: Click on module drop down and verify
        EXPECTED: Below 6 module should display
        EXPECTED: Super Button
        EXPECTED: Surface Bet
        EXPECTED: Footer Menu
        EXPECTED: Quick Links
        EXPECTED: Highlights Carousel
        EXPECTED: Featured module
        """
        pass

    def test_003_navigate_to_cms___sports_pages___home_page_and_disable_any_one_or_two_module_and_verify_module_drop_down_list(self):
        """
        DESCRIPTION: Navigate to CMS - Sports Pages - Home Page and disable any one or two module and verify module drop down list
        EXPECTED: Disabled modules should not display in modules drop down
        """
        pass

    def test_004_enable_any_one_module_which_was_disabled_in_above_step(self):
        """
        DESCRIPTION: Enable any one module which was disabled in above step
        EXPECTED: All enabled modules should display in list
        """
        pass
