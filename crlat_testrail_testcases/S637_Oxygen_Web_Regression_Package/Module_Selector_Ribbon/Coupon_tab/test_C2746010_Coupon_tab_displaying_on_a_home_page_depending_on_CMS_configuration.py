import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2746010_Coupon_tab_displaying_on_a_home_page_depending_on_CMS_configuration(Common):
    """
    TR_ID: C2746010
    NAME: Coupon tab displaying on a home page depending on CMS configuration
    DESCRIPTION: This test case verifies displaying of Coupon/Acca tab on a home page
    DESCRIPTION: Note: cannot automate as we are not automating switching off items in CMS as it may affect other tests
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - You should have a module "Coupons" created and enabled in CMS > Module Ribbon Tabs
    PRECONDITIONS: - You should be on a home page
    PRECONDITIONS: NOTE: Coral brand uses name Coupons and Ladbrokes uses name ACCAs
    """
    keep_browser_open = True

    def test_001_verify_coupons_tab_displaying(self):
        """
        DESCRIPTION: Verify "Coupons" tab displaying
        EXPECTED: "Coupons" tab is shown in module ribbon
        """
        pass

    def test_002___in_cms__module_ribbon_tabs_deactivate_coupons_module_and_save_changes(self):
        """
        DESCRIPTION: - In CMS > Module Ribbon Tabs deactivate "Coupons" module and save changes.
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_page_in_application_and_verify_displaying_of_a_coupons_tab_on_a_home_page(self):
        """
        DESCRIPTION: Refresh the page in application and verify displaying of a "Coupons" tab on a home page.
        EXPECTED: "Coupons" tab is not shown in module ribbon after page refresh
        """
        pass
