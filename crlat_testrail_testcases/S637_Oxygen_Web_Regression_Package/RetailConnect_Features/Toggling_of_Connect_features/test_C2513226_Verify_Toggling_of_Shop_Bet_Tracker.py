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
class Test_C2513226_Verify_Toggling_of_Shop_Bet_Tracker(Common):
    """
    TR_ID: C2513226
    NAME: Verify Toggling of 'Shop Bet Tracker'
    DESCRIPTION: This test case verify that Shop Bet Tracker can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> shop Bet Tracker
    PRECONDITIONS: 1. Load CMS and make sure Shop Bet Tracker is turned off: System configuration -> Connect -> shop Bet Tracker = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in
    """
    keep_browser_open = True

    def test_001__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * There is no 'Shop Bet Tracker' item in 'Connect' section
        """
        pass

    def test_002__open_rhm_menu_verify_connect_section(self):
        """
        DESCRIPTION: * Open RHM menu
        DESCRIPTION: * Verify 'Connect' section
        EXPECTED: * RHM menu is opened
        EXPECTED: * There is no 'Shop Bet Tracker' item in 'Connect' section
        """
        pass

    def test_003_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_004__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * There is no 'Shop Bet Tracker' item in the list
        """
        pass

    def test_005_verify_navigation_to_shop_bet_tracker_by_direct_link_httpscoralcoukbet_tracker(self):
        """
        DESCRIPTION: Verify navigation to 'Shop Bet Tracker' by direct link https://***.coral.co.uk/bet-tracker
        EXPECTED: Home page is opened instead
        """
        pass

    def test_006__load_cms_turn_shop_bet_tracker_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'shop Bet Tracker' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_008__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Shop Bet Tracker' item is in 'Connect' section
        """
        pass

    def test_009_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: Tap 'Shop Bet Tracker' item
        EXPECTED: Bet Tracker page is loaded
        """
        pass

    def test_010__open_rhm_menu_verify_connect_section(self):
        """
        DESCRIPTION: * Open RHM menu
        DESCRIPTION: * Verify 'Connect' section
        EXPECTED: * RHM menu is opened
        EXPECTED: * 'Shop Bet Tracker' item is in 'Connect' section
        """
        pass

    def test_011_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: Tap 'Shop Bet Tracker' item
        EXPECTED: Bet Tracker page is loaded
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
        EXPECTED: * 'Shop Bet Tracker' item is present in the list
        """
        pass

    def test_014_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: Tap 'Shop Bet Tracker' item
        EXPECTED: Bet Tracker page is loaded
        """
        pass
