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
class Test_C387555_Verify_information_on_the_Coral_Priority_VIP_Page_for_users_with_different_VIP_levels(Common):
    """
    TR_ID: C387555
    NAME: Verify information on the Coral Priority (VIP) Page for users with different VIP levels
    DESCRIPTION: This test case verifies levels information according to the user's VIP level on the VIP Page
    DESCRIPTION: AUTOTEST [C527662]
    PRECONDITIONS: User must be logged in
    PRECONDITIONS: User must be a VIP (see below)
    PRECONDITIONS: In order to run this test case, you need users of Bronze, Silver, Gold and Platinum types
    PRECONDITIONS: **VIP IMS Level Configuration**
    PRECONDITIONS: * Non-VIP players = IMS VIP Level _1 - 10_
    PRECONDITIONS: * Bronze players = IMS VIP Level _11_
    PRECONDITIONS: * Silver players = IMS VIP Level _12_
    PRECONDITIONS: * Gold players = IMS VIP Level _13_
    PRECONDITIONS: * Platinum players = IMS VIP Level _14_
    PRECONDITIONS: In order to grant the user a VIP level, contact UAT for assistance
    """
    keep_browser_open = True

    def test_001_log_in_as_a_bronze_vip_level_user(self):
        """
        DESCRIPTION: Log in as a **Bronze** VIP Level user
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_the_balance_button_in_order_to_open_right_hand_menu(self):
        """
        DESCRIPTION: Tap the balance button in order to open Right Hand Menu
        EXPECTED: Right Hand Menu is opened
        """
        pass

    def test_003_tap_more_info_link_on_the_vip_summary(self):
        """
        DESCRIPTION: Tap 'More Info' link on the VIP Summary
        EXPECTED: User is redirected to the VIP page
        """
        pass

    def test_004_verify_the_level_information_accordions_visible_to_the_user(self):
        """
        DESCRIPTION: Verify the level information accordions, visible to the user
        EXPECTED: * Bronze level user is able to see the Bronze and Silver accordions and Level Information
        EXPECTED: * All accordions can be expanded and collapsed
        """
        pass

    def test_005_check_the_level_information_for_bronze_level_section(self):
        """
        DESCRIPTION: Check the level information for 'Bronze Level' section
        EXPECTED: Text for Bronze level:
        EXPECTED: * Enhanced Comp Point Redemption
        EXPECTED: * Dedicated Customer Service Team
        EXPECTED: * Exclusive Bronze Promotions
        """
        pass

    def test_006_check_the_level_information_for_silver_level_section(self):
        """
        DESCRIPTION: Check the level information for 'Silver Level' section
        EXPECTED: Text for Silver level:
        EXPECTED: * Priority Customer Service
        EXPECTED: * Hospitality Prize Draws
        EXPECTED: * Enhanced Comp Point Redemption
        EXPECTED: * Weekly Enhanced Prices
        EXPECTED: * Further Exclusive Silver Promotions
        """
        pass

    def test_007_log_out_and_log_back_in_as_a_silver_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Silver** VIP Level user
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: * Silver level user is able to see Silver and Gold accordions and Level information
        EXPECTED: * All accordions can be expanded and collapsed
        """
        pass

    def test_009_check_the_level_information_for_silver_level(self):
        """
        DESCRIPTION: Check the level information for Silver level
        EXPECTED: Text for Silver level same as in step #6
        """
        pass

    def test_010_check_the_level_information_for_gold_level(self):
        """
        DESCRIPTION: Check the level information for Gold level
        EXPECTED: Text for Gold level:
        EXPECTED: * Priority Customer Service
        EXPECTED: * Monthly Account Reviews
        EXPECTED: * Hospitality Invitations and Prize Draws
        EXPECTED: * Enhanced Comp Point Redemption
        EXPECTED: * Weekly Enhanced Prices – Higher Stakes
        EXPECTED: * Exclusive Gold Promotions
        """
        pass

    def test_011_log_out_and_log_back_in_as_a_gold_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Gold** VIP Level user
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: * Gold level user is able to see the Gold and Platinum accordions and Level Information
        EXPECTED: * All accordions can be expanded and collapsed
        """
        pass

    def test_013_check_the_level_information_for_gold_level(self):
        """
        DESCRIPTION: Check the level information for Gold level
        EXPECTED: Text for Gold level same as in step #10
        """
        pass

    def test_014_check_the_level_information_for_platinum_level(self):
        """
        DESCRIPTION: Check the level information for Platinum level
        EXPECTED: Text for Platinum level:
        EXPECTED: * Personal Account Manager
        EXPECTED: * Enhanced Rewards and Bonuses
        EXPECTED: * Comprehensive Tailored Priority Programme
        EXPECTED: * Exclusive Platinum Promotions
        EXPECTED: * Bespoke Hospitality Invitations
        EXPECTED: * Faster Withdrawals
        EXPECTED: * Enhanced Comp Point Redemption
        """
        pass

    def test_015_log_out_and_log_back_in_as_a_platinum_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Platinum** VIP Level user
        EXPECTED: * Platinum level user is able to see only the Platinum accordion and Level Information
        EXPECTED: * Text for Platinum level is the same as in step #14
        """
        pass
