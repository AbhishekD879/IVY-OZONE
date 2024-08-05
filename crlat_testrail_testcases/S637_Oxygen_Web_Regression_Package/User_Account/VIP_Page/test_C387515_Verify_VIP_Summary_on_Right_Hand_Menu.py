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
class Test_C387515_Verify_VIP_Summary_on_Right_Hand_Menu(Common):
    """
    TR_ID: C387515
    NAME: Verify VIP Summary on Right Hand Menu
    DESCRIPTION: This test case verifies VIP Summary on Right Hand Menu
    DESCRIPTION: AUTOTEST [C528025]
    PRECONDITIONS: **VIP IMS Level Configuration**
    PRECONDITIONS: * Non-VIP players = IMS VIP Level _1 - 10_
    PRECONDITIONS: * **Bronze** players = IMS VIP Level _11_
    PRECONDITIONS: * **Silver** players = IMS VIP Level _12_
    PRECONDITIONS: * **Gold** players = IMS VIP Level _13_
    PRECONDITIONS: * **Platinum** players = IMS VIP Level _14_
    PRECONDITIONS: * In order to grant the user a VIP level, contact UAT for assistance
    PRECONDITIONS: * VIP point API information: https://confluence.egalacoral.com/display/SPI/VIP+Points+API
    """
    keep_browser_open = True

    def test_001_log_in_as_not_a_vip_user_check_preconditions_for_vip_level_details(self):
        """
        DESCRIPTION: Log in as NOT a VIP user (check Preconditions for VIP level details)
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_the_balance_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the balance button in order to open the Right Hand Menu
        EXPECTED: Right Hand Menu slides out
        """
        pass

    def test_003_check_the_right_hand_menu(self):
        """
        DESCRIPTION: Check the Right Hand Menu
        EXPECTED: * The menu does not include a VIP summary
        EXPECTED: * The menu does not include VIP Points
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

    def test_006_tap_on_the_balance_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the balance button in order to open the Right Hand Menu
        EXPECTED: Right Hand Menu slides out
        """
        pass

    def test_007_check_the_right_hand_menu(self):
        """
        DESCRIPTION: Check the Right Hand Menu
        EXPECTED: * VIP Summary is shown for the user
        EXPECTED: * VIP Points is shown for the user
        """
        pass

    def test_008_verify_vip_summary(self):
        """
        DESCRIPTION: Verify VIP Summary
        EXPECTED: The VIP User is able to view the following:
        EXPECTED: * Real Balance in the VIP User's account currency (displayed by default)
        EXPECTED: * Real Balance hide/show switcher (enabled by default)
        EXPECTED: * VIP User's First and Last Name
        EXPECTED: * VIP level background
        EXPECTED: * 'VIP Level' label
        EXPECTED: * VIP level, depending on the level of the user, who is logged in
        EXPECTED: * 'More Info' link
        EXPECTED: * Total Points & Points Meter
        """
        pass

    def test_009_tap_the_hideshow_hide_vip_status_from_my_account_menu_checkbox(self):
        """
        DESCRIPTION: Tap the hide/show 'Hide VIP Status from My Account Menu' checkbox
        EXPECTED: Total Points Balance is hidden
        """
        pass

    def test_010_tap_the_hideshow_hide_vip_status_from_my_account_menu_checkbox_again(self):
        """
        DESCRIPTION: Tap the hide/show 'Hide VIP Status from My Account Menu' checkbox again
        EXPECTED: Total Points Balance is displayed
        """
        pass

    def test_011_verify_users_vip_level(self):
        """
        DESCRIPTION: Verify user's VIP level
        EXPECTED: VIP Level is one of the following:
        EXPECTED: * Bronze
        EXPECTED: * Silver
        EXPECTED: * Gold
        EXPECTED: * Platinum
        EXPECTED: (check Preconditions for details)
        """
        pass

    def test_012_verify_vip_points(self):
        """
        DESCRIPTION: Verify VIP Points
        EXPECTED: * Total number of VIP Points is shown (Sports+Gaming)
        EXPECTED: * Range bar with Sports points and Gaming points is shown
        EXPECTED: * 'Sport' label with total number of sports points are shown
        EXPECTED: * 'Gaming' label with total number of gaming points are shown
        """
        pass

    def test_013_tap_the_more_info_link(self):
        """
        DESCRIPTION: Tap the 'More Info' link
        EXPECTED: VIP User is redirected to the VIP page
        """
        pass

    def test_014_repeat_steps_5_13_for_the_following_users_bronze_players__ims_vip_level__11__silver_players__ims_vip_level__12__gold_players__ims_vip_level__13__platinum_players__ims_vip_level__14_(self):
        """
        DESCRIPTION: Repeat steps #5-13 for the following users:
        DESCRIPTION: * Bronze players = IMS VIP Level _11_
        DESCRIPTION: * Silver players = IMS VIP Level _12_
        DESCRIPTION: * Gold players = IMS VIP Level _13_
        DESCRIPTION: * Platinum players = IMS VIP Level _14_
        EXPECTED: 
        """
        pass
