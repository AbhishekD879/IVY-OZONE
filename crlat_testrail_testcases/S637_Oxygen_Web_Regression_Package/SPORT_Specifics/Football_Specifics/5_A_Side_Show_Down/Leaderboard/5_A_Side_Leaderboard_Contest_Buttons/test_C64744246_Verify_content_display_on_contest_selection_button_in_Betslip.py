import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C64744246_Verify_content_display_on_contest_selection_button_in_Betslip(Common):
    """
    TR_ID: C64744246
    NAME: Verify content display on contest selection button in Betslip
    DESCRIPTION: This testcase verifies the content present on the contest selection button
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label. 5-A-Side Showdown
    PRECONDITIONS: Path. /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create multiple contests for different events
    PRECONDITIONS: 2. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest
        EXPECTED: User should be optin to that contest and contest should be added to the lobby
        """
        pass

    def test_003_navigate_to_5_a_side_event_and_add_5_legs_to_betslip_or_navigate_to_5_a_side_lobby_gt_navigate_to_contest_pre_leaderboard_page_gt_click_on_build_team(self):
        """
        DESCRIPTION: Navigate to 5-A-Side event and add 5 legs to betslip or Navigate to 5-A-Side lobby-&gt; Navigate to contest Pre-Leaderboard page-&gt; click on Build Team
        EXPECTED: User should be taken to 5-A-Side pitch and add 5 legs to betslip
        """
        pass

    def test_004_verify_whether_the_active_and_opted_contest_entry_buttons_are_shown_on_betslip(self):
        """
        DESCRIPTION: Verify whether the active and opted contest entry buttons are shown on betslip
        EXPECTED: Active and opted contest entry buttons should be present in betslip with the CMS contest creation priority order, first button should be default selected with blue color highlighting.
        """
        pass

    def test_005_verify_grey_color_box_is_displaying_for_freebet_ticket_and_voucher_prizes_for_blue_color_highlighting_contest_selection_button(self):
        """
        DESCRIPTION: Verify grey color box is displaying for Freebet, Ticket and voucher prizes for blue color highlighting contest selection button
        EXPECTED: Gery color box should display for Freebet, Ticket and voucher prizes for blue color highlighting contest selection button
        """
        pass

    def test_006_verify_contest_selection_button_fields1contest_name2entry_stake3prize_iconfreebet_icon_for_freebet_ticket_and_ticket_icon_for_voucher_and_no_icon_for_cash4first_price_cms_config_of_1st_prize_in_prize_table(self):
        """
        DESCRIPTION: Verify contest selection button fields
        DESCRIPTION: 1.Contest name
        DESCRIPTION: 2.Entry stake
        DESCRIPTION: 3.prize Icon(Freebet icon for Freebet, Ticket and Ticket icon for voucher and no icon for cash)
        DESCRIPTION: 4.First price (CMS config of 1st prize in prize table)
        EXPECTED: 1.Contest name should be displayed on the top of the contest selection button
        EXPECTED: 2.Entry stake and First prize should display with comma (,) separated
        EXPECTED: (Decimal values of entry stake, First price of pounds are displayed like numeric value ex: 0.1=10p, 0.01=100p etc...)
        """
        pass

    def test_007_verify_icons_displayed_on_contest_selection_button_for_first_prizes_of_freebet_ticket_voucher_and_no_icon_for_cash(self):
        """
        DESCRIPTION: Verify Icons displayed on contest selection button for First prizes of Freebet, Ticket, Voucher and no icon for cash.
        EXPECTED: ![](index.php?/attachments/get/d1ad2ab9-a23e-48a4-baf1-cd611b4b580d)
        EXPECTED: Icons should be displayed for First prizes of Freebet, Ticket, Voucher only, no icon for cash.
        """
        pass
