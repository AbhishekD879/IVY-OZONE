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
class Test_C2358024_Verify_flow_for_In_Shop_user_upgrade_if_system_has_only_card_number_stored_in_memory(Common):
    """
    TR_ID: C2358024
    NAME: Verify flow for In-Shop user upgrade if system has only card number stored in memory
    DESCRIPTION: This test case verifies flow for In-Shop user upgrade if the system has only card number stored in memory
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: To emulate situation when only card number stored in memory and PIN is not:
    PRECONDITIONS: Home page -> Sports Menu Ribbon -> 'A-Z Sports' button -> Connect -> Use Connect Online -> 'Enter Coral Connect card details' page is opened -> reload the page -> now only card number is saved in the memory and PIN is lost
    PRECONDITIONS: An in-shop user should be logged into the system (5000000000979448/ 1234)
    """
    keep_browser_open = True

    def test_001_home_page___sports_menu_ribbon___a_z_sports_button___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Sports Menu Ribbon -> 'A-Z Sports' button -> Connect -> Use Connect Online
        EXPECTED: * Upgrade Page - Card number/PIN is opened
        EXPECTED: * Carn number field is populated
        """
        pass

    def test_002_home_page___sports_menu_ribbon___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Sports Menu Ribbon -> Connect -> Use Connect Online
        EXPECTED: * Upgrade Page - Card number/PIN is opened
        EXPECTED: * Carn number field is populated
        """
        pass

    def test_003_home_page___right_hand_menu___connect___use_connect_online(self):
        """
        DESCRIPTION: Home page -> Right Hand Menu -> Connect -> Use Connect Online
        EXPECTED: * Upgrade Page - Card number/PIN is opened
        EXPECTED: * Carn number field is populated
        """
        pass

    def test_004_home_page___add_some_bets_to_betslip___open_betslip___tap_upgrade_your_account__bet_now(self):
        """
        DESCRIPTION: Home page -> Add some bets to betslip -> open betslip -> tap 'Upgrade Your Account & Bet Now'
        EXPECTED: * Upgrade Page - Card number/PIN is opened
        EXPECTED: * Carn number field is populated
        """
        pass
