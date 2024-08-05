import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2377242_Verify_ways_to_get_to_the_Shop_promotions_offers(Common):
    """
    TR_ID: C2377242
    NAME: Verify ways to get to the Shop promotions/offers
    DESCRIPTION: This test case verifies possible ways to get to the Shop promotions/offers
    PRECONDITIONS: **Note that on UI Retail page should be named as 'Connect' for Coral App and 'The Grid' for Ladbrokes**
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: Go to CMS and make sure there are some active promotions with Category = 'Connect Promotions', if there are no please create some
    PRECONDITIONS: Load the SB app
    """
    keep_browser_open = True

    def test_001_tap_promotions_in_the_header_ribbon_menu_on_the_homepage(self):
        """
        DESCRIPTION: Tap 'Promotions' in the header ribbon menu on the homepage
        EXPECTED: * Promotion page with two tabs ('All', 'Shop Exclusive') is opened
        EXPECTED: * Tab 'All' is active
        """
        pass

    def test_002_tap_the_shop_exclusive_tab(self):
        """
        DESCRIPTION: Tap the 'Shop Exclusive' tab
        EXPECTED: The 'Shop Exclusive' tab with active connect promotions is opened
        """
        pass

    def test_003_open_connect_or_the_grid_landing_page___shop_exclusive_promos(self):
        """
        DESCRIPTION: Open 'Connect' OR 'The Grid' landing page -> Shop exclusive promos
        EXPECTED: * Promotion page with two tabs ('All', 'Shop Exclusive') is opened
        EXPECTED: * Tab 'Shop Exclusive' is active
        """
        pass

    def test_004_tap_all_taband_verify_there_is_no_shop_exclusive_promos_on_it(self):
        """
        DESCRIPTION: Tap 'All' tab
        DESCRIPTION: and verify there is no 'Shop Exclusive' promos on it
        EXPECTED: Promotions with other categories than 'Connect Promotions' category are displayed
        """
        pass
