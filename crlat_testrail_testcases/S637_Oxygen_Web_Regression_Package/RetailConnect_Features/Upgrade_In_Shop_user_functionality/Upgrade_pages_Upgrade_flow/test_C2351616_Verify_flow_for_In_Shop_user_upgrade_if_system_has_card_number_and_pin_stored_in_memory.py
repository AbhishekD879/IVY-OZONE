import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2351616_Verify_flow_for_In_Shop_user_upgrade_if_system_has_card_number_and_pin_stored_in_memory(Common):
    """
    TR_ID: C2351616
    NAME: Verify flow for In-Shop user upgrade if system has card number and pin stored in memory
    DESCRIPTION: This test case verifies flow for In-Shop user upgrade if the system has card number and pin credentials stored in memory
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: An in-shop user should be logged into the system
    PRECONDITIONS: Local Storage shouldn't be cleared and the home page shouldn't be reloaded when an in-shop user is logged in
    """
    keep_browser_open = True

    def test_001_home_page___sports_menu_ribbon___a_z_sports_button___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Sports Menu Ribbon -> 'A-Z Sports' button -> Connect -> Use Connect Online
        EXPECTED: The Upgrade Page - Users details is opened
        """
        pass

    def test_002_home_page___sports_menu_ribbon___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Sports Menu Ribbon -> Connect -> Use Connect Online
        EXPECTED: The Upgrade Page - Users details is opened
        """
        pass

    def test_003_home_page___right_hand_menu___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Right Hand Menu -> Connect -> Use Connect Online
        EXPECTED: The Upgrade Page - Users details is opened
        """
        pass

    def test_004_home_page___add_some_bets_to_betslip___open_betslip___tap_upgrade_your_account__bet_now_button(self):
        """
        DESCRIPTION: Home page -> Add some bets to betslip -> open betslip -> tap 'Upgrade Your Account & Bet Now' button
        EXPECTED: The Upgrade Page - Users details is opened
        """
        pass

    def test_005_log_in_to_the_system_as_an_in_shop_user_for_the_first_timeimitate_it_empty_local_storage_cache_cookies_and_hard_reload_the_page(self):
        """
        DESCRIPTION: Log in to the system as an in-shop user for the first time
        DESCRIPTION: (imitate it: empty local storage, cache, cookies and hard reload the page)
        EXPECTED: * The user is successfully logged in
        EXPECTED: * Pop-up 'Upgrade your account' appears
        """
        pass

    def test_006_tap_upgrade_button_on_the_pop_up_upgrade_your_account(self):
        """
        DESCRIPTION: Tap Upgrade button on the pop-up 'Upgrade your account'
        EXPECTED: The Upgrade Page - Users details is opened
        """
        pass
