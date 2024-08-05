import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C61176323_Verify_display_of_Entry_Confirmation_for_Leaderboard_in_Bet_Receipt(Common):
    """
    TR_ID: C61176323
    NAME: Verify display of Entry Confirmation for Leaderboard in Bet Receipt
    DESCRIPTION: This test case verifies the entry confirmation message displayed on Bet receipt
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: **To Qualify for Leaderboard**
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: **The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.**
    """
    keep_browser_open = True

    def test_001_log_into_ladbrokes_application(self):
        """
        DESCRIPTION: Log into Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002__navigate_to_football_edp__5_a_side_click_on_build_a_team(self):
        """
        DESCRIPTION: * Navigate to Football EDP > 5-A Side
        DESCRIPTION: * Click on Build a Team
        EXPECTED: * User should be navigated to Football EDP
        EXPECTED: * User should be navigated to 5-A Side tab
        EXPECTED: * User should be navigated to 5-A Side Pitch view
        """
        pass

    def test_003_place_a_5_a_side_bet_satisfying_the_pre_conditions_mentioned(self):
        """
        DESCRIPTION: Place a 5-A side bet satisfying the pre-conditions mentioned
        EXPECTED: User should be able to place 5-A Side bet successfully
        """
        pass

    def test_004_verify_the_entry_confirmation_displayed_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Entry Confirmation displayed on the bet receipt
        EXPECTED: * Entry Confirmation notification should be displayed below the 'Bet Placed Successfully' Header
        EXPECTED: * 5-A Side Ladbrokes image should be displayed (Configured in CMS > Image Manager)
        EXPECTED: * **Your team has been entered into a 5-A-Side Leaderboard!** message should be displayed as title header
        EXPECTED: * Secondary message should be displayed **[Configured in CMS > Contest Details page > 'Entry Confirmation Text']**
        EXPECTED: * **VIEW ENTRY** CTA button should be displayed
        EXPECTED: ![](index.php?/attachments/get/151963659)
        """
        pass

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet receipt
        EXPECTED: * Regular Bet Receipt with Win Only alerts should be displayed
        EXPECTED: **Note : None of the regular Bet Receipt content changes, including Win Alerts**
        """
        pass

    def test_006__validate_the_secondary_text_in_entry_confirmation_notification_configured_in_cms__contest_details_page__entry_confirmation_text_enter_longer_textmore_than_three_lines_in_fe_in_entry_confirmation_text_field_and_save_enter_textupto_three_lines_in_fe_in_entry_confirmation_text_field_and_save(self):
        """
        DESCRIPTION: * Validate the secondary text in Entry Confirmation Notification
        DESCRIPTION: * *[Configured in CMS > Contest Details page > 'Entry Confirmation Text']*
        DESCRIPTION: * *Enter longer text(**More than three lines in FE**) in Entry Confirmation Text field and save*
        DESCRIPTION: * *Enter text(**upto three lines in FE**) in Entry Confirmation Text field and save*
        EXPECTED: * **For more than three lines** Text will be truncated and displayed as (...)
        EXPECTED: * **Upto 3 lines** Text will be displayed as below
        EXPECTED: ![](index.php?/attachments/get/160999796)
        """
        pass

    def test_007_validate_the_entry_confirmation_text_in_bet_receipt_when_user_entered_all_eligible_contests_more_than_one(self):
        """
        DESCRIPTION: Validate the entry confirmation Text in Bet receipt when user entered **all eligible Contests** more than one
        EXPECTED: * Entry Confirmation notification should be displayed below the 'Bet Placed Successfully' Header
        EXPECTED: * 5-A Side Ladbrokes image should be displayed (Configured in CMS > Image Manager)
        EXPECTED: * **Your team has been entered into a 5-A-Side Leaderboard!** message should be displayed as title header
        EXPECTED: **Same Entry Stake**
        EXPECTED: * Secondary message should be displayed **[Configured in CMS > Contest Details page > 'Entry Confirmation Text']** Text should be displayed from the Contest as per the priority of the Contest configured in CMS
        EXPECTED: * **VIEW ENTRY** CTA button should be displayed
        EXPECTED: * Click on **VIEW ENTRY** - User should be navigated to the Contest Landing Page (To the Contest having the highest priority in CMS)
        EXPECTED: **Different Entry stake**
        EXPECTED: * Secondary message should be displayed **[Configured in CMS > Contest Details page > 'Entry Confirmation Text']** Text should be displayed from the Contest which has the highest Entry Stake
        EXPECTED: * **VIEW ENTRY** CTA button should be displayed
        EXPECTED: * Click on **VIEW ENTRY** - User should be navigated to the Contest Landing Page (To the Contest having the highest Entry Stake)
        """
        pass

    def test_008_validate_the_css_styles_as_per_zeplinhttpsappzeplinioproject60103c71f2dbeb25375e487bscreen60103d338d869d0b3738548e(self):
        """
        DESCRIPTION: Validate the CSS styles as per Zeplin
        DESCRIPTION: https://app.zeplin.io/project/60103c71f2dbeb25375e487b/screen/60103d338d869d0b3738548e
        EXPECTED: * CSS styles for the image , title, secondary text, View ENTRY CTA should be as per Zeplin
        """
        pass

    def test_009__verify_view_entry_cta_click_on_view_entry_cta(self):
        """
        DESCRIPTION: * Verify View ENTRY CTA
        DESCRIPTION: * Click on View ENTRY CTA
        EXPECTED: * View entry should be displayed
        EXPECTED: * User should be able to click View Entry button
        EXPECTED: * User should be navigated to Leaderboard page of that contest
        """
        pass

    def test_010_verify_ga_tracking_for_view_entry_cta(self):
        """
        DESCRIPTION: Verify GA tracking for View ENTRY CTA
        EXPECTED: * GA tracking should be there for View Entry
        """
        pass

    def test_011_place_a_5_a_side_bet_which_does_not_meet_the_criteria_for_entering_leaderboard(self):
        """
        DESCRIPTION: Place a 5-A Side bet which does not meet the criteria for entering leaderboard
        EXPECTED: * Normal 5-A Side bet receipt should be displayed
        EXPECTED: * No Entry Notification should be displayed
        EXPECTED: * Bet should be displayed in Open Bets
        """
        pass

    def test_012_place_a_5_a_side_bet_using_free_bet_satisfying_the_pre_conditions_mentionedfree_bet_toggle_is_enabled_in_cms__5_a_side_showdown__contest(self):
        """
        DESCRIPTION: Place a 5-A Side bet using free bet satisfying the pre-conditions mentioned
        DESCRIPTION: **Free bet toggle is enabled in CMS > 5-A Side Showdown > Contest**
        EXPECTED: * Entry Confirmation notification should be displayed below the 'Bet Placed Successfully' Header
        EXPECTED: * 5-A Side Ladbrokes image should be displayed (Configured in CMS > Image Manager)
        EXPECTED: * **Your team has been entered into a 5-A-Side Leaderboard!** message should be displayed as title header
        EXPECTED: * Secondary message should be displayed **[Configured in CMS > Contest Details page > 'Entry Confirmation Text']**
        EXPECTED: The secondary description text should be three lines and the rest will be truncated. It will be displayed '..." if we have more than 3 lines.
        EXPECTED: * **VIEW ENTRY** CTA button should be displayed
        EXPECTED: ![](index.php?/attachments/get/151963659)
        """
        pass

    def test_013_place_a_5_a_side_bet_using_free_bet_satisfying_the_pre_conditions_mentionedfree_bet_toggle_is_disabled_in_cms__5_a_side_showdown__contest(self):
        """
        DESCRIPTION: Place a 5-A Side bet using free bet satisfying the pre-conditions mentioned
        DESCRIPTION: **Free bet toggle is disabled in CMS > 5-A Side Showdown > Contest**
        EXPECTED: * Normal 5-A Side bet receipt should be displayed
        EXPECTED: * No Entry Notification should be displayed
        EXPECTED: * Bet should be displayed in Open Bets
        """
        pass
