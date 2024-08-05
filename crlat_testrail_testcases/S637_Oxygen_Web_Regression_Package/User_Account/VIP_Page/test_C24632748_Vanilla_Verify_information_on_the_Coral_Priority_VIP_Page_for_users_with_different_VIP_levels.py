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
class Test_C24632748_Vanilla_Verify_information_on_the_Coral_Priority_VIP_Page_for_users_with_different_VIP_levels(Common):
    """
    TR_ID: C24632748
    NAME: [Vanilla} Verify information on the Coral Priority (VIP) Page for users with different VIP levels
    DESCRIPTION: This test case verifies levels information according to the user's VIP level on the VIP Page
    DESCRIPTION: Note: as for now:
    DESCRIPTION: 1) according to VANO-616 there will be no Platinum+ users.
    DESCRIPTION: 2) according to VANO-656 - Promotions were removed from menu for VIP users.
    PRECONDITIONS: User must be logged in
    PRECONDITIONS: User must be a VIP (see below)
    PRECONDITIONS: In order to run this test case, you need users of Bronze, Silver, Gold and Platinum types
    PRECONDITIONS: **VIP IMS Level Configuration**
    PRECONDITIONS: * Non-VIP players = IMS VIP Level _1 - 10_
    PRECONDITIONS: * Bronze players = IMS VIP Level _11_
    PRECONDITIONS: * Silver players = IMS VIP Level _12_
    PRECONDITIONS: * Gold players = IMS VIP Level _13_
    PRECONDITIONS: * Platinum players = IMS VIP Level _14_
    PRECONDITIONS: * Platinum+ players = IMS VIP Level _15_
    PRECONDITIONS: In order to grant the user a VIP level, contact GVC team for assistance
    """
    keep_browser_open = True

    def test_001_log_in_as_a_bronze_vip_level_user(self):
        """
        DESCRIPTION: Log in as a **Bronze** VIP Level user
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_my_account_button_in_order_to_open_right_hand_menu(self):
        """
        DESCRIPTION: Tap My Account button in order to open Right Hand Menu
        EXPECTED: Right Hand Menu is opened
        """
        pass

    def test_003_tap_vip_option(self):
        """
        DESCRIPTION: Tap **VIP** option
        EXPECTED: User is redirected to the VIP page and **My VIP** tab is open
        """
        pass

    def test_004_verify_the_level_information_accordions_visible_to_the_user_in_priority_points_progress_section(self):
        """
        DESCRIPTION: Verify the level information accordions, visible to the user in PRIORITY POINTS PROGRESS section
        EXPECTED: Bronze level user is able to see current BRONZE level and level, previous level: CLUB, next level: SILVER
        """
        pass

    def test_005_check_the_level_information_in_club_section(self):
        """
        DESCRIPTION: Check the level information in **CLUB** section
        EXPECTED: Information in CLUB level:
        EXPECTED: * Previous level: PREVIOUS LEVEL CLUB
        EXPECTED: * Information how to avoid downgrade to CLUB level
        EXPECTED: Note: Previous Level section is not displayed on mobile
        """
        pass

    def test_006_check_the_level_information_in_bronze_level_section(self):
        """
        DESCRIPTION: Check the level information in **BRONZE** level section
        EXPECTED: Information in BRONZE level:
        EXPECTED: * Current level: CURRENT LEVEL BRONZE
        EXPECTED: * Collected points in current months (months points/total points) with SPORT and GAMING distinction
        """
        pass

    def test_007_check_the_level_information_in_silver_section(self):
        """
        DESCRIPTION: Check the level information in **SILVER** section
        EXPECTED: Information in SILVER level:
        EXPECTED: * Next level: NEXT LEVEL SILVER
        EXPECTED: * Information how to upgrade to SILVER level (under level section on mobile)
        """
        pass

    def test_008_log_out_and_log_back_in_as_a_silver_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Silver** VIP Level user
        EXPECTED: User is logged in
        """
        pass

    def test_009_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Silver level user is able to see current SILVER level and level, previous level: BRONZE, next level: GOLD
        """
        pass

    def test_010_check_the_level_information_in_bronze_section(self):
        """
        DESCRIPTION: Check the level information in **BRONZE** section
        EXPECTED: Information in BRONZE level:
        EXPECTED: * Previous level: PREVIOUS LEVEL BRONZE
        EXPECTED: * Information how to avoid downgrade to BRONZE level
        EXPECTED: Note: Previous Level section is not displayed on mobile
        """
        pass

    def test_011_check_the_level_information_in_silver_section(self):
        """
        DESCRIPTION: Check the level information in **SILVER** section
        EXPECTED: Information in SILVER level:
        EXPECTED: * Current level: CURRENT LEVEL SILVER
        EXPECTED: * Collected points in current months (months points/total points) with SPORT and GAMING distinction
        """
        pass

    def test_012_check_the_level_information_in_gold_section(self):
        """
        DESCRIPTION: Check the level information in **GOLD** section
        EXPECTED: Information in GOLD level:
        EXPECTED: * Next level: NEXT LEVEL GOLD
        EXPECTED: * Information how to upgrade to GOLD level (under level section on mobile)
        """
        pass

    def test_013_log_out_and_log_back_in_as_a_gold_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Gold** VIP Level user
        EXPECTED: User is logged in
        """
        pass

    def test_014_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Gold level user is able to see current GOLD level and level, previous level: SILVER, next level: PLATINUM
        """
        pass

    def test_015_check_the_level_information_in_silver_section(self):
        """
        DESCRIPTION: Check the level information in **SILVER** section
        EXPECTED: Information in SILVER level:
        EXPECTED: * Previous level: PREVIOUS LEVEL SILVER
        EXPECTED: * Information how to avoid downgrade to SILVER level
        EXPECTED: Note: Previous Level section is not displayed on mobile
        """
        pass

    def test_016_check_the_level_information_in_gold_section(self):
        """
        DESCRIPTION: Check the level information in **GOLD** section
        EXPECTED: Information in GOLD level:
        EXPECTED: * Current level: CURRENT LEVEL GOLD
        EXPECTED: * Collected points in current months (months points/total points) with SPORT and GAMING distinction
        """
        pass

    def test_017_check_the_level_information_in_platinum_section(self):
        """
        DESCRIPTION: Check the level information in **PLATINUM** section
        EXPECTED: Information in PLATINUM level:
        EXPECTED: * Next level: NEXT LEVEL PLATINUM
        """
        pass

    def test_018_log_out_and_log_back_in_as_a_platinum_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Platinum** VIP Level user
        EXPECTED: User is logged in
        """
        pass

    def test_019_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Platinum level user is able to see current PLATINUM level only
        """
        pass

    def test_020_log_out_and_log_back_in_as_a_platinum_plus_vip_level_user(self):
        """
        DESCRIPTION: Log out and log back in as a **Platinum Plus** VIP Level user
        EXPECTED: User is logged in
        """
        pass

    def test_021_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Platinum level user is able to see current PLATINUM+ level only
        """
        pass
