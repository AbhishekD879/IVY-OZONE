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
class Test_C61176353_Verify_whether_restricted_5_A_Side_bets_which_did_not_enter_Leaderboard_due_to_Team_size_limit_previously_should_be_not_add_automatically_after_bets_are_voided(Common):
    """
    TR_ID: C61176353
    NAME: Verify whether restricted 5-A Side bets which did not enter Leaderboard due to Team size limit previously should be not add automatically after bets are voided
    DESCRIPTION: 
    PRECONDITIONS: 1: User should place 5-A side bet that meets the criteria for entering Showdown
    PRECONDITIONS: 2: User 5-A Side bet should be voided
    PRECONDITIONS: **To Qualify Leaderboard**
    PRECONDITIONS: 1: Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3: The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4: The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS. The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: 5: 5 A Side bets which entered the showdown contest should be voided
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_5_a_side_bet_is_voidednavigate_to_leaderboard_page(self):
        """
        DESCRIPTION: **5-A Side bet is Voided**
        DESCRIPTION: Navigate to Leaderboard page
        EXPECTED: * User should not be able view the entry
        EXPECTED: * Previously displayed entry which is now voided should no longer be displayed in Leaderboard Contest
        """
        pass

    def test_003_verify_the_entry_added_automatically_to_leaderboard_contestuser_has_already_placed_more_than_the_maximum_amounts_of_bets_allowed_on_that_eventexample_team_size_is_configured_as_5_in_cmsuser_placed_6___5_a_side_betsfirst_placed_5___5_a_side_bets_are_qualified_for_leaderboard_and_the_entries_are_displayed_in_leaderboard_page6th___5_a_side_bet_was_restricted_to_enter_leaderboard_due_to_team_size_configured(self):
        """
        DESCRIPTION: Verify the entry added automatically to Leaderboard Contest
        DESCRIPTION: *User has already placed more than the maximum amounts of bets allowed on that event*
        DESCRIPTION: **Example:** Team size is configured as **5** in CMS
        DESCRIPTION: User placed **6** - 5-A Side bets
        DESCRIPTION: First placed **5** - 5-A Side bets are qualified for Leaderboard and the entries are displayed in leaderboard page
        DESCRIPTION: **6th** - 5-A Side bet was restricted to enter Leaderboard due to Team Size configured
        EXPECTED: **Entered Leaderboard 5-A Side bets are Voided**
        EXPECTED: * Voided 5-A Side bets Entry are removed from Leaderboard
        EXPECTED: * Restricted 5-A Side bets which did not enter Leaderboard due to Team size limit previously should not be added after existing entries got removed from Leaderboard
        """
        pass
