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
class Test_C2303506_Verify_showing_Upgrade_your_Connect_account_to_bet_online_menu_item_only_for_in_shop_users(Common):
    """
    TR_ID: C2303506
    NAME: Verify showing 'Upgrade your Connect account to bet online' menu item only for in-shop users
    DESCRIPTION: This test case verifies showing 'Use Connect Online' menu item only for in-shop users
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: To configure Connect Page content use CMS:
    PRECONDITIONS: https://CMS_ENDPOINT -> Menus -> Connect Menus
    PRECONDITIONS: Prepare three users:
    PRECONDITIONS: a) Multichannel user
    PRECONDITIONS: b) in-shop user
    PRECONDITIONS: c) online user without connect card
    PRECONDITIONS: 1. Load SportsBook App
    PRECONDITIONS: 2. The ways how to open Connect Feature list:
    PRECONDITIONS: * Homepage -> header ribbon -> CONNECT
    PRECONDITIONS: * Homepage -> header ribbon -> ALL SPORTS -> CONNECT section (Mobile)
    """
    keep_browser_open = True

    def test_001_log_in_to_the_app_as_in_shop_user(self):
        """
        DESCRIPTION: Log in to the app as in-shop user
        EXPECTED: The user is logged in
        """
        pass

    def test_002_open_connect_landing_page(self):
        """
        DESCRIPTION: Open CONNECT Landing page
        EXPECTED: The user sees '⤹⤴︎' icon and 'Upgrade your Connect account to bet online' menu item in CONNECT section
        """
        pass

    def test_003_tap_upgrade_your_connect_account_to_bet_online_item(self):
        """
        DESCRIPTION: Tap 'Upgrade your Connect account to bet online' item
        EXPECTED: The upgrade page with dialog for in-shop user is opened
        """
        pass

    def test_004_log_out_from_the_app___open_connect_page(self):
        """
        DESCRIPTION: Log out from the app -> open Connect page
        EXPECTED: * A user is successfully logged out
        EXPECTED: * 'Upgrade your Connect account to bet online' item is not displayed in Connect page
        """
        pass

    def test_005_log_in_to_the_app_as_multi_channel_user(self):
        """
        DESCRIPTION: Log in to the app as multi-channel user
        EXPECTED: User is logged in
        """
        pass

    def test_006_open_connect_page(self):
        """
        DESCRIPTION: Open Connect page
        EXPECTED: 'Upgrade your Connect account to bet online' item is not displayed in Connect page
        """
        pass

    def test_007_log_out_from_the_app(self):
        """
        DESCRIPTION: Log out from the app
        EXPECTED: User is logged out
        """
        pass

    def test_008_log_in_to_the_sb_app_as_online_user(self):
        """
        DESCRIPTION: Log in to the SB app as online user
        EXPECTED: User is logged in
        """
        pass

    def test_009_open_connect_page(self):
        """
        DESCRIPTION: Open Connect page
        EXPECTED: 'Upgrade your Connect account to bet online' item is not displayed in Connect page
        """
        pass
