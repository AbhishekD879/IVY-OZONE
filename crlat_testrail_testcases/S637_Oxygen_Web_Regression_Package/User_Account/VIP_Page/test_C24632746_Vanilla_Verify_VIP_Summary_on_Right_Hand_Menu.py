import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C24632746_Vanilla_Verify_VIP_Summary_on_Right_Hand_Menu(Common):
    """
    TR_ID: C24632746
    NAME: [Vanilla] Verify VIP Summary on Right Hand Menu
    DESCRIPTION: This test case verifies VIP Summary on Right Hand Menu
    DESCRIPTION: Note: as for now:
    DESCRIPTION: 1) according to VANO-616 there will be no Platinum+ users.
    DESCRIPTION: 2) according to VANO-656 - Promotions were removed from menu for VIP users.
    PRECONDITIONS: **VIP IMS Level Configuration**
    PRECONDITIONS: * Non-VIP players = IMS VIP Level _1 - 10_
    PRECONDITIONS: * **Bronze** players = IMS VIP Level _11_
    PRECONDITIONS: * **Silver** players = IMS VIP Level _12_
    PRECONDITIONS: * **Gold** players = IMS VIP Level _13_
    PRECONDITIONS: * **Platinum** players = IMS VIP Level _14_
    PRECONDITIONS: * **Platinum+ ** players = IMS VIP Level _15_
    PRECONDITIONS: * In order to grant the user a VIP level, contact GCV team for assistance
    """
    keep_browser_open = True

    def test_001_log_in_as_not_a_vip_user_check_preconditions_for_vip_level_details(self):
        """
        DESCRIPTION: Log in as NOT a VIP user (check Preconditions for VIP level details)
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_the_my_account_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the My Account button in order to open the Right Hand Menu
        EXPECTED: Right Hand Menu slides out
        """
        pass

    def test_003_check_the_right_hand_menu(self):
        """
        DESCRIPTION: Check the Right Hand Menu
        EXPECTED: The menu does not include **VIP** option
        """
        pass

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_005_log_in_as_a_vip_user_check_preconditions_for_vip_level_details(self):
        """
        DESCRIPTION: Log in as a VIP user (check Preconditions for VIP level details)
        EXPECTED: User is logged in
        """
        pass

    def test_006_tap_on_the_my_account_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the My Account button in order to open the Right Hand Menu
        EXPECTED: Right Hand Menu slides out
        """
        pass

    def test_007_check_the_right_hand_menu(self):
        """
        DESCRIPTION: Check the Right Hand Menu
        EXPECTED: The menu does not include **VIP** option
        """
        pass

    def test_008_tap_on_vip_option(self):
        """
        DESCRIPTION: Tap on **VIP** option
        EXPECTED: **VIP** menu is open
        """
        pass

    def test_009_check_vip_menu(self):
        """
        DESCRIPTION: Check **VIP** menu
        EXPECTED: **VIP** menu contains following options:
        EXPECTED: * MY VIP
        EXPECTED: * VIP BENEFITS
        EXPECTED: * PROMOTIONS
        EXPECTED: * CONTACT US
        """
        pass

    def test_010_tap_on_my_vip_option(self):
        """
        DESCRIPTION: Tap on **MY VIP** option
        EXPECTED: **VIP** page is open with following tabs:
        EXPECTED: * My VIP (open by default)
        EXPECTED: * VIP Benefits
        EXPECTED: * Promotions
        EXPECTED: * Contact Us
        """
        pass
