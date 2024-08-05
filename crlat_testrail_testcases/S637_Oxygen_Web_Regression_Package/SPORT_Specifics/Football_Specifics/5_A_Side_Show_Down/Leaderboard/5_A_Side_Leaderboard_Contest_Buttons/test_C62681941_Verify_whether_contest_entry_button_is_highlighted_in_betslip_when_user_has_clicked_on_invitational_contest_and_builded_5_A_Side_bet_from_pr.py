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
class Test_C62681941_Verify_whether_contest_entry_button_is_highlighted_in_betslip_when_user_has_clicked_on_invitational_contest_and_builded_5_A_Side_bet_from_pre_leaderboard_page_in_logged_in_state(Common):
    """
    TR_ID: C62681941
    NAME: Verify whether contest entry button is highlighted in betslip when user has clicked on invitational contest and builded 5-A-Side bet from pre leaderboard page in logged in state
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
    PRECONDITIONS: How to enter team into a Invitational contest .
    PRECONDITIONS: 1. Navigate to CMS, magic link will be available in the contest created.
    PRECONDITIONS: 2. Copy the magic link and navigate through it.
    PRECONDITIONS: 3. User will be navigated to Pre- Leaderboard (if the event is not yet started).
    PRECONDITIONS: 4. Click on build team(will be available when logged in) and build a team and place bet will eligible stake.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_real_account(self):
        """
        DESCRIPTION: Login to ladbrokes application with real account
        EXPECTED: User should be logged in successfully with real account
        """
        pass

    def test_002_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest
        EXPECTED: User should be optin to that contest and contest should be added to the lobby
        """
        pass

    def test_003_user_should_be_taken_to_the_pre_leaderboard_page(self):
        """
        DESCRIPTION: User should be taken to the pre leaderboard page
        EXPECTED: User should be shown with pre leaderboard page
        """
        pass

    def test_004_build_the_team_from_pre_leaderboard_page(self):
        """
        DESCRIPTION: Build the team from pre leaderboard page
        EXPECTED: User should be taken to 5-A-Side pitch and able to add 5 legs
        """
        pass

    def test_005_check_if_this_particular_contest_entry__button_is_highlighted_by_default_in_betslip(self):
        """
        DESCRIPTION: Check if this particular contest entry  button is highlighted by default in betslip
        EXPECTED: Specific invitational contest from which the user is navigated should be default selected with blue color highlighting.
        """
        pass
