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
class Test_C2351618_Verify_flow_for_In_Shop_user_upgrade_if_system_doesnt_have_card_number_and_pin_stored_in_memory(Common):
    """
    TR_ID: C2351618
    NAME: Verify flow for In-Shop user upgrade if system doesn't have card number and pin stored in memory
    DESCRIPTION: This test case verifies flow for In-Shop user upgrade if the system doesn't have card number and pin credentials stored in memory
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: An in-shop user should be logged into the system
    PRECONDITIONS: Local Storage should be cleared and the home page should be reloaded when an in-shop user is logged in
    """
    keep_browser_open = True

    def test_001_home_page___sports_menu_ribbon___a_z_sports_button___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Sports Menu Ribbon -> 'A-Z Sports' button -> Connect -> Use Connect Online
        EXPECTED: Upgrade Page - Card number/PIN is opened
        """
        pass

    def test_002_home_page___sports_menu_ribbon___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Sports Menu Ribbon -> Connect -> Use Connect Online
        EXPECTED: Upgrade Page - Card number/PIN is opened
        """
        pass

    def test_003_home_page___right_hand_menu___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Right Hand Menu -> Connect -> Use Connect Online
        EXPECTED: Upgrade Page - Card number/PIN is opened
        """
        pass

    def test_004_home_page___add_some_bets_to_betslip___open_betslip___tap_upgrade_your_account__bet_now(self):
        """
        DESCRIPTION: Home page -> Add some bets to betslip -> open betslip -> tap 'Upgrade Your Account & Bet Now'
        EXPECTED: Upgrade Page - Card number/PIN is opened
        """
        pass
