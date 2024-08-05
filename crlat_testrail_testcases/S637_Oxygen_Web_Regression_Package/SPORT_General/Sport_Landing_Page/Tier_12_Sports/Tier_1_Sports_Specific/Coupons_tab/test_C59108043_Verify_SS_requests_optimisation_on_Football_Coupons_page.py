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
class Test_C59108043_Verify_SS_requests_optimisation_on_Football_Coupons_page(Common):
    """
    TR_ID: C59108043
    NAME: Verify SS requests optimisation on Football Coupons page
    DESCRIPTION: This test case verifies that only one 'Coupon?simpleFilter=coupon' request is triggered when ACCAs/Coupons page/tab is opened.
    PRECONDITIONS: Note:
    PRECONDITIONS: - You should have a module "Coupons" created and enabled in CMS > Module Ribbon Tabs and also for sports in Sports Categories -> definite sport.
    PRECONDITIONS: - Make sure coupons toggle is turned on: System Configuration > Config/Structure > FeatureToggle > FootballCoupons
    PRECONDITIONS: - Load the app
    PRECONDITIONS: - Go to the Football Landing page
    """
    keep_browser_open = True

    def test_001_click_on_acca_ladbrokescoupons_coral_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Click on 'ACCA' (Ladbrokes)/'Coupons' (Coral) tab on Football Landing page
        EXPECTED: Tab content loads with list of coupons available
        """
        pass

    def test_002_verify_the_requests_sent_during_opening_the_tab(self):
        """
        DESCRIPTION: Verify the requests sent during opening the tab
        EXPECTED: Only 1 'Coupon?simpleFilter=coupon' request is triggered
        EXPECTED: ![](index.php?/attachments/get/113167516)
        EXPECTED: ![](index.php?/attachments/get/113189777)
        """
        pass

    def test_003_navigate_to_other_sports_with_coupons_available_and_repeat_steps_above(self):
        """
        DESCRIPTION: Navigate to other sports with coupons available and repeat steps above
        EXPECTED: Only 1 'Coupon?simpleFilter=coupon' request is triggered when loading Coupons/ACCAs tab content
        """
        pass

    def test_004_navigate_to_home_page_accacoupons_module_ribbon_tabs_mobile_view_and_verify_the_number_of_coupon_requests_triggered(self):
        """
        DESCRIPTION: Navigate to Home page: ACCA/Coupons module ribbon tabs (mobile view) and verify the number of coupon requests triggered
        EXPECTED: Only 1 'Coupon?simpleFilter=coupon' request is triggered when loading Coupons/ACCAs tab content
        """
        pass
