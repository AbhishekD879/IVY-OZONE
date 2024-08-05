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
class Test_C62681944_Verify_when_user_has_selected_one_contest_and_has_entered_stake_less_than_entry_stake_then_normal_bet_is_placed_on_clicking_place_bet_and_should_not_enter_into_any_contest(Common):
    """
    TR_ID: C62681944
    NAME: Verify when user has selected one contest and has entered stake less than  entry stake , then normal bet is placed on clicking place bet and should not enter into any contest
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

    def test_003_navigate_to_5_a_sideide_lobbygt_and_select_one_of_the_contest_and_click_build_team(self):
        """
        DESCRIPTION: Navigate to 5-A-Sideide lobby&gt; and select one of the contest and click Build Team
        EXPECTED: User should be taken to 5-A-Side pitch and add 5 legs to betslip
        """
        pass

    def test_004_verify_whether_that_particular_contest_entry_button_is_highlighted_in_betslip(self):
        """
        DESCRIPTION: Verify whether that particular contest entry button is highlighted in betslip
        EXPECTED: That particular contest entry button should be highlighted in betslip
        """
        pass

    def test_005_click_on_place_bet_by_giving_stake_less_than_the_entry_stake(self):
        """
        DESCRIPTION: Click on place bet by giving stake less than the entry stake
        EXPECTED: Stake provided should be less than the contest entry stake
        """
        pass

    def test_006_check_if_the_normal_5_a_side_bet_is_placed(self):
        """
        DESCRIPTION: Check if the normal 5-A-Side bet is placed
        EXPECTED: Normal 5-A-Side bet should be placed on giving less stake than entry stake
        """
        pass

    def test_007_check_if_the_bet_has_entered_any_contest(self):
        """
        DESCRIPTION: Check if the bet has entered any contest
        EXPECTED: Bet shouldn't enter to the contest and entry confirmation message shouldn't be shown
        """
        pass
