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
class Test_C2513555_Verify_Toggling_of_Shop_Locator(Common):
    """
    TR_ID: C2513555
    NAME: Verify Toggling of 'Shop Locator'
    DESCRIPTION: This test case verify that Shop Locator can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> shop Locator
    PRECONDITIONS: 1. Load CMS and make sure Shop Locator is turned off: System configuration -> Connect -> shop Locator = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in
    """
    keep_browser_open = True

    def test_001_mobile_from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: **MOBILE:**
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * There is no 'Shop Locator' item in 'Connect' section
        """
        pass

    def test_002_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_003_desktop_from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: **DESKTOP:**
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * There is no 'Locator' item in the list
        """
        pass

    def test_004_verify_navigation_to_shop_locator_by_direct_link_httpscoralcoukshop_locator(self):
        """
        DESCRIPTION: Verify navigation to 'Shop Locator' by direct link https://***.coral.co.uk/shop-locator
        EXPECTED: Home page is opened instead
        """
        pass

    def test_005__load_cms_turn_shop_locator_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'shop Locator' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_007_mobile_from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: **MOBILE:**
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Shop Locator' item is in 'Connect' section
        """
        pass

    def test_008_tap_shop_locator_item(self):
        """
        DESCRIPTION: Tap 'Shop Locator' item
        EXPECTED: Shop Locator Map is loaded
        """
        pass

    def test_009_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_010_desktop_from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: **DESKTOP:**
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * 'Shop Locator' item is present in the list
        """
        pass

    def test_011_tap_shop_locator_item(self):
        """
        DESCRIPTION: Tap 'Shop Locator' item
        EXPECTED: Shop Locator Map is loaded
        """
        pass

    def test_012_verify_navigation_to_shop_locator_by_direct_link_httpscoralcoukshop_locator(self):
        """
        DESCRIPTION: Verify navigation to 'Shop Locator' by direct link https://***.coral.co.uk/shop-locator
        EXPECTED: Shop Locator Map is loaded
        """
        pass
