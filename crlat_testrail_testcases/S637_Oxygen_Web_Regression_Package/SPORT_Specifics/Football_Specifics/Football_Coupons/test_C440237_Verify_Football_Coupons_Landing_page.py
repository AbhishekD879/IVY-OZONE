import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C440237_Verify_Football_Coupons_Landing_page(Common):
    """
    TR_ID: C440237
    NAME: Verify Football Coupons Landing page
    DESCRIPTION: This test case verifies Football Coupons Landing page
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment - 'Featured Coupon' section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    PRECONDITIONS: 1. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 2. List of Coupons depends on TI tool configuration data for Coupons. All available Coupons from OB response will be displayed on the page
    PRECONDITIONS: Load Oxygen app - Homepage is opened
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * **Featured Coupons**(CMS configurable) and **Popular Coupons**(all the rest of available coupons) sections are shown on the Coupons Landing page
        EXPECTED: * List of coupons is displayed on the Coupons Landing page according to related section
        EXPECTED: * It is possible to navigate on Coupons Details page by tapping a row from the list
        """
        pass

    def test_003_verify_list_of_coupons(self):
        """
        DESCRIPTION: Verify list of coupons
        EXPECTED: List of coupons includes:
        EXPECTED: * UK Coupon
        EXPECTED: * Odds on Coupon
        EXPECTED: * European Coupon
        EXPECTED: * Euro Elite Coupon
        EXPECTED: * Televised Matches
        EXPECTED: * Top Leagues Coupon
        EXPECTED: * International Coupon
        EXPECTED: * Rest of the World Coupon
        EXPECTED: * Goalscorer Coupon
        EXPECTED: ( All available Coupons from OB response will be displayed on the page)
        """
        pass
