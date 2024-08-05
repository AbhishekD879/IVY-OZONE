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
class Test_C2513214_Verify_Toggling_of_In_Shop_promotions(Common):
    """
    TR_ID: C2513214
    NAME: Verify Toggling of 'In-Shop promotions'
    DESCRIPTION: This test case verify that 'In-Shop promotions' can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> promotions
    PRECONDITIONS: 1. Load CMS and make sure 'In-Shop promotions' feature is turned off: System configuration -> Connect -> promotions = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in
    """
    keep_browser_open = True

    def test_001__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * There is no 'Shop Exclusive Promos' item in 'Connect' section
        """
        pass

    def test_002_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_003__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * There is no 'Shop Exclusive Promos' item in the list
        """
        pass

    def test_004_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_005__open_promotions_from_header_ribbon_verify_presence_of_shop_exclusive_tab(self):
        """
        DESCRIPTION: * Open 'Promotions' from header ribbon
        DESCRIPTION: * Verify presence of 'Shop Exclusive' tab
        EXPECTED: * 'Promotions' page is loaded
        EXPECTED: * 'Shop Exclusive' tab is absent
        EXPECTED: *  'All' tab is displayed and active
        """
        pass

    def test_006_verify_navigation_to_shop_exclusive_promos_by_direct_link_httpscoralcoukpromotionsretail(self):
        """
        DESCRIPTION: Verify navigation to 'Shop Exclusive' promos by direct link https://***.coral.co.uk/promotions/retail
        EXPECTED: Home page is opened instead
        """
        pass

    def test_007__load_cms_turn_promotions_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'promotions' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_008_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_009__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Shop Exclusive Promos' item is present in 'Connect' section
        """
        pass

    def test_010_tap_shop_exclusive_promos_item(self):
        """
        DESCRIPTION: Tap 'Shop Exclusive Promos' item
        EXPECTED: User is redirected to Promotions page -> Shop Exclusive tab
        """
        pass

    def test_011_tap_shop_exclusive_promos_item(self):
        """
        DESCRIPTION: Tap 'Shop Exclusive Promos' item
        EXPECTED: User is redirected to Promotions page -> Shop Exclusive tab
        """
        pass

    def test_012_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_013__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * 'Shop Exclusive Promos' item is present in the list
        """
        pass

    def test_014_tap_shop_exclusive_promos_item(self):
        """
        DESCRIPTION: Tap 'Shop Exclusive Promos' item
        EXPECTED: User is redirected to Promotions page -> Shop Exclusive tab
        """
        pass

    def test_015_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_016__open_promotions_from_header_ribbon_verify_presence_of_shop_exclusive_tab(self):
        """
        DESCRIPTION: * Open 'Promotions' from header ribbon
        DESCRIPTION: * Verify presence of 'Shop Exclusive' tab
        EXPECTED: * 'Promotions' page is loaded
        EXPECTED: * 'Shop Exclusive' tab is present (next to All tab)
        EXPECTED: *  'All' tab is active by default
        """
        pass

    def test_017_select_shop_exclusive_tab(self):
        """
        DESCRIPTION: Select 'Shop Exclusive' tab
        EXPECTED: * Tab is opened
        EXPECTED: * List of In-Shop promos (if exist) is displayed (promos with category with id=2)
        """
        pass
