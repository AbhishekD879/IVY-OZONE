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
class Test_C62681947_verify_whether_the_user_is_entering_to_the_specific_contest_selected_on_betslip_on_placing_the_eligible_5_A_Sideide_bet_with_free_bet_and_stake_and_check_if_entry_confirmation_is_shown(Common):
    """
    TR_ID: C62681947
    NAME: verify whether the user is entering to the specific contest selected on betslip on placing the eligible 5-A-Sideide bet with free bet and stake and check if entry confirmation is shown
    DESCRIPTION: 
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
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
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
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
        EXPECTED: User should be taken to 5-A-Sideide pitch and add 5 legs to betslip
        """
        pass

    def test_004_verify_whether_the_active_and_opted_contest_entry_buttons_are_shown_on_betslip(self):
        """
        DESCRIPTION: Verify whether the active and opted contest entry buttons are shown on betslip
        EXPECTED: Active and opted contest entry buttons should be present in betslip with the CMS contest creation priority order
        """
        pass

    def test_005_select_an_active_contest_from_the_displayed_contest_entry_button_and_place_an_eligible_5_a_side_bet_for_that_contest_with_freebetplusstakemake_sure_freebet_allowed_field_is_checked_in_cms_as_mentioned_in_pre_condition(self):
        """
        DESCRIPTION: Select an active contest from the displayed contest entry button and place an eligible 5-A-Side bet for that contest with freebet+stake(Make sure freebet allowed field is checked in cms as mentioned in pre condition)
        EXPECTED: User should be able to place a 5-A-Side bet with freebet+stake
        """
        pass

    def test_006_check_if_the_entry_confirmation_message_is_shown_after_placing_the_eligible_5_a_side_bet_with_freebetplusstake(self):
        """
        DESCRIPTION: Check if the entry confirmation message is shown after placing the eligible 5-A-Side bet with freebet+stake
        EXPECTED: Entry confirmation message should be shown on placing eligible bet with freebet+stake
        """
        pass
