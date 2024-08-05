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
class Test_C24632747_Vanilla_Verify_Coral_Priority_VIP_Page_general(Common):
    """
    TR_ID: C24632747
    NAME: [Vanilla] Verify Coral Priority (VIP) Page (general)
    DESCRIPTION: This test case verifies Coral Priority (VIP) Page, accessible ONLY for logged in VIP users
    DESCRIPTION: Note: as for now:
    DESCRIPTION: 1) according to VANO-616 there will be no Platinum+ users.
    DESCRIPTION: 2) according to VANO-656 - Promotions were removed from menu for VIP users.
    PRECONDITIONS: User must be logged in
    PRECONDITIONS: User must be a VIP (see below)
    PRECONDITIONS: **VIP IMS Level Configuration**
    PRECONDITIONS: * Non-VIP players = IMS VIP Level _1 - 10_
    PRECONDITIONS: * Bronze players = IMS VIP Level _11_
    PRECONDITIONS: * Silver players = IMS VIP Level _12_
    PRECONDITIONS: * Gold players = IMS VIP Level _13_
    PRECONDITIONS: * Platinum players = IMS VIP Level _14_
    PRECONDITIONS: * Platinum+ players = IMS VIP Level _15_
    PRECONDITIONS: * In order to grant the user a VIP level, contact GVC team for assistance
    """
    keep_browser_open = True

    def test_001_tap_on_the_my_account_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the My Account button in order to open the Right Hand Menu
        EXPECTED: Right Hand Menu slides out
        """
        pass

    def test_002_tap_on_vip_option(self):
        """
        DESCRIPTION: Tap on **VIP** option
        EXPECTED: **VIP** menu is open
        """
        pass

    def test_003_tap_on_my_vip_option(self):
        """
        DESCRIPTION: Tap on **MY VIP** option
        EXPECTED: **VIP** page is open with following tabs:
        EXPECTED: * My VIP (open by default)
        EXPECTED: * VIP Benefits
        EXPECTED: * Promotions
        EXPECTED: * Contact Us
        """
        pass

    def test_004_verify_back__button_only_on_mobile(self):
        """
        DESCRIPTION: Verify 'Back' ('<') button (only on mobile)
        EXPECTED: The 'back' button redirects the user to their previous page
        """
        pass

    def test_005_check_my_vip_tab_content(self):
        """
        DESCRIPTION: Check **My VIP** tab content
        EXPECTED: The My VIP page contains following sections:
        EXPECTED: * PRIORITY POINTS PROGRESS
        EXPECTED: * PRIORITY POINTS BALANCE
        EXPECTED: * HOW TO EARN POINTS
        EXPECTED: * TEMRS & CONDITIONS
        """
        pass

    def test_006_verify_priority_points_progress_section(self):
        """
        DESCRIPTION: Verify PRIORITY POINTS PROGRESS section
        EXPECTED: Section contains:
        EXPECTED: * VIP label
        EXPECTED: * VIP level (depending on user from preconditions)
        EXPECTED: * Bronze
        EXPECTED: * Silver
        EXPECTED: * Gold
        EXPECTED: * Platinum
        EXPECTED: * Collected point during current months (months points/total points) with SPORTS and GAMING distinction.
        """
        pass

    def test_007_verify_your_priority_points_balance_section(self):
        """
        DESCRIPTION: Verify YOUR PRIORITY POINTS BALANCE section
        EXPECTED: Section contains information about point balance of:
        EXPECTED: * Total points balance
        EXPECTED: * Slots, scratches & bingo
        EXPECTED: * Other casino games
        EXPECTED: * Sports single bets
        EXPECTED: * Sports multiple bets
        """
        pass

    def test_008_verify_how_to_earn_points_section(self):
        """
        DESCRIPTION: Verify HOW TO EARN POINTS section
        EXPECTED: Section contains:
        EXPECTED: * Information about ways to earn Priority Points
        EXPECTED: * Information about requirements for qualifying to Priority Program on different levels
        """
        pass

    def test_009_verify_terms__conditions_section(self):
        """
        DESCRIPTION: Verify TERMS & CONDITIONS section
        EXPECTED: Section contains:
        EXPECTED: * Information about terms $ conditions
        """
        pass

    def test_010_open_vip_benefits_tab_and_check_content(self):
        """
        DESCRIPTION: Open **VIP Benefits** tab and check content
        EXPECTED: The **VIP Benefits** page contains following sections:
        EXPECTED: * WELCOME TO CORAL VIP contains:
        EXPECTED: * UPDATE COMMUNICATION PREFERENCES link
        EXPECTED: * VIP LEVELS
        EXPECTED: * TERMS & CONDITIONS
        """
        pass

    def test_011_open_promotions_tab_and_check_content(self):
        """
        DESCRIPTION: Open **Promotions** tab and check content
        EXPECTED: Section contains:
        EXPECTED: * EXCLUSIVE VIP PROMOTIONS
        """
        pass

    def test_012_open_contact_us_tab_and_check_content(self):
        """
        DESCRIPTION: Open **Contact Us** tab and check content
        EXPECTED: Section contains:
        EXPECTED: * GET IN TOUCH contains:
        EXPECTED: * Phone number
        EXPECTED: * Email address
        EXPECTED: * FAQ VIP1 contains some questions
        """
        pass

    def test_013_repeat_steps_5_13_for_the_following_users_bronze_players__ims_vip_level__11__silver_players__ims_vip_level__12__gold_players__ims_vip_level__13__platinum_players__ims_vip_level__14__platinumplus_players__ims_vip_level__15_(self):
        """
        DESCRIPTION: Repeat steps #5-13 for the following users:
        DESCRIPTION: * Bronze players = IMS VIP Level _11_
        DESCRIPTION: * Silver players = IMS VIP Level _12_
        DESCRIPTION: * Gold players = IMS VIP Level _13_
        DESCRIPTION: * Platinum players = IMS VIP Level _14_
        DESCRIPTION: * Platinum+ players = IMS VIP Level _15_
        EXPECTED: 
        """
        pass
