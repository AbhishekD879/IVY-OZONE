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
class Test_C2513571_Verify_Toggling_of_Upgrade_from_In_Shop_user_to_Multi_channel_feature(Common):
    """
    TR_ID: C2513571
    NAME: Verify Toggling of 'Upgrade from In-Shop user to Multi-channel' feature
    DESCRIPTION: This test case verify that Upgrade feature can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> upgrade
    PRECONDITIONS: 1. Load CMS and make sure 'Upgrade' is turned off: System configuration -> Connect -> upgrade = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in with In-Shop user for the firs time (to emulate it clear Local Storage and Cookies before Log In)
    """
    keep_browser_open = True

    def test_001__in_shop_user_is_logged_in_for_the_first_time_verify_there_is_no_upgrade_your_account_dialog_is_shown(self):
        """
        DESCRIPTION: * In-Shop user is Logged in for the first time
        DESCRIPTION: * Verify there is no 'Upgrade your account' dialog is shown
        EXPECTED: * 'Upgrade your account' dialog is not shown
        """
        pass

    def test_002__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * There is no 'Use Connect Online' item in 'Connect' section
        """
        pass

    def test_003__open_rhm_menu_verify_connect_section(self):
        """
        DESCRIPTION: * Open RHM menu
        DESCRIPTION: * Verify 'Connect' section
        EXPECTED: * RHM menu is opened
        EXPECTED: * There is no 'Use Connect Online' item in 'Connect' section
        """
        pass

    def test_004_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_005__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * There is no 'Use Connect Online' item in the list
        """
        pass

    def test_006_verify_navigation_to_shop_bet_tracker_by_direct_link_httpscoralcoukconnectregistration(self):
        """
        DESCRIPTION: Verify navigation to 'Shop Bet Tracker' by direct link https://***.coral.co.uk/connect/registration
        EXPECTED: Home page is opened instead
        """
        pass

    def test_007__load_cms_turn_upgrade_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'upgrade' feature on
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
        EXPECTED: * 'Use Connect Online'  item is in 'Connect' section
        """
        pass

    def test_010_tap_use_connect_online__item(self):
        """
        DESCRIPTION: Tap 'Use Connect Online'  item
        EXPECTED: Registration page is loaded
        """
        pass

    def test_011__open_rhm_menu_verify_connect_section(self):
        """
        DESCRIPTION: * Open RHM menu
        DESCRIPTION: * Verify 'Connect' section
        EXPECTED: * RHM menu is opened
        EXPECTED: * 'Use Connect Online' item is in 'Connect' section
        """
        pass

    def test_012_tap_use_connect_online_item(self):
        """
        DESCRIPTION: Tap 'Use Connect Online' item
        EXPECTED: Registration page is loaded
        """
        pass

    def test_013_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_014__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * 'Use Connect Online' item is present in the list
        """
        pass

    def test_015_tap_use_connect_online_item(self):
        """
        DESCRIPTION: Tap 'Use Connect Online' item
        EXPECTED: Registration page is loaded
        """
        pass
