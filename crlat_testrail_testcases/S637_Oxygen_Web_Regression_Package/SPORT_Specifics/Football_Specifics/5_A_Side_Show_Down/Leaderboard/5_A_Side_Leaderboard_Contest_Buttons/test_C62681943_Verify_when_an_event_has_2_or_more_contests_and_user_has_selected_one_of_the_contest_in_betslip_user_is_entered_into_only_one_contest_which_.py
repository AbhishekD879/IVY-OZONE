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
class Test_C62681943_Verify_when_an_event_has_2_or_more_contests_and_user_has_selected_one_of_the_contest_in_betslip_user_is_entered_into_only_one_contest_which_is_selected_in_betslip(Common):
    """
    TR_ID: C62681943
    NAME: Verify when an event has 2 or more contests and user has selected one of the contest in betslip, user is entered into only one contest which is selected in betslip
    DESCRIPTION: 
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label. 5-A-Side Showdown
    PRECONDITIONS: Path. /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create two contests for same event
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

    def test_003_navigate_to_5_a_sideide_lobbygt_and_select_one_of_the_contest_out_of_two_contests_which_are_created_for_same_eventas_mentioned_in_pre_conditions_and_click_build_team(self):
        """
        DESCRIPTION: Navigate to 5-A-Sideide lobby&gt; and select one of the contest out of two contests which are created for same event(as mentioned in pre-conditions) and click Build Team
        EXPECTED: User should be taken to 5-A-Sideide pitch and add 5 legs to betslip
        """
        pass

    def test_004_verify_whether_that_particular_contest_entry_button_is_highlighted_in_betslip(self):
        """
        DESCRIPTION: Verify whether that particular contest entry button is highlighted in betslip
        EXPECTED: That particular contest entry button should be blue color highlighted in betslip
        """
        pass

    def test_005_click_on_place_bet_by_giving_eligible_stake_and_check_the_entry_confirmation_message(self):
        """
        DESCRIPTION: Click on place bet by giving eligible stake and check the entry confirmation message
        EXPECTED: User should be able to place bet and enter the showdown
        """
        pass

    def test_006_check_if_placed_bet_entered_into_only_that_contest_but_not_to_the_other_contest_of_the_same_event(self):
        """
        DESCRIPTION: Check if placed bet entered into only that contest but not to the other contest of the same event
        EXPECTED: User should enter into only one contest with one bet though that event has multiple contests
        """
        pass
