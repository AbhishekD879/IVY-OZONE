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
class Test_C60539987_Verify_entry_removed_from_Leaderboard_Contest_Page_for_Voided_Bet(Common):
    """
    TR_ID: C60539987
    NAME: Verify entry removed from Leaderboard  Contest Page for Voided Bet
    DESCRIPTION: This test case verifies that User entry is removed from Leaderboard when respective 5-A Side bet is voided
    PRECONDITIONS: 1: User should place 5-A side bet that meets the criteria for entering Leaderboard
    PRECONDITIONS: 2: User 5-A Side bet should be voided
    PRECONDITIONS: **To Qualify Leaderboard**
    PRECONDITIONS: 1: Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3: The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4: The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS. The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: 5: 5 A Side bets which entered the Leaderboard contest should be voided
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_before_bet_is_voidednavigate_to_leaderboard_page(self):
        """
        DESCRIPTION: **Before Bet is Voided**
        DESCRIPTION: Navigate to Leaderboard page
        EXPECTED: * User should be able to view the entry in Leaderboard
        EXPECTED: **Pre-Play**
        EXPECTED: ![](index.php?/attachments/get/161000387)
        """
        pass

    def test_003_5_a_side_bet_is_voidednavigate_to_leaderboard_page(self):
        """
        DESCRIPTION: **5-A Side bet is Voided**
        DESCRIPTION: Navigate to Leaderboard page
        EXPECTED: * User should not be able view the entry
        EXPECTED: * Previously displayed entry which is now voided should no longer be displayed in 5A-Side Contest
        """
        pass

    def test_004_navigate_to_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to Settled bets tab
        EXPECTED: * Voided 5-A Side bet should be displayed
        EXPECTED: * GO TO 5-A Side button should be displayed
        """
        pass

    def test_005_click_on_go_to_5_a_side_button(self):
        """
        DESCRIPTION: Click on GO TO 5-A Side button
        EXPECTED: * User should be re-directed to 5-A Side Pitch View
        EXPECTED: * User should be able to add players and place bet
        """
        pass

    def test_006_all_entries_5_a_side_bets_in_the_leaderboard_are_voidedplace_5_a_side_bet_indexphpattachmentsget160999973bet_should_qualify_for_leaderboard(self):
        """
        DESCRIPTION: **All entries 5-A Side bets in the Leaderboard are voided**
        DESCRIPTION: Place 5-A Side bet ![](index.php?/attachments/get/160999973)
        DESCRIPTION: **Bet should Qualify for Leaderboard**
        EXPECTED: * Entry Confirmation notification should be displayed below the 'Bet Placed Successfully' Header
        EXPECTED: * 5-A Side Ladbrokes image should be displayed (Configured in CMS > Image Manager)
        EXPECTED: * **Your team has been entered into a 5-A-Side Leaderboard!** message should be displayed as title header
        EXPECTED: * Secondary message should be displayed **[Configured in CMS > Contest Details page > 'Entry Confirmation Text']**
        EXPECTED: * **VIEW ENTRY** CTA button should be displayed
        EXPECTED: ![](index.php?/attachments/get/160999974)
        """
        pass

    def test_007_verify_the_entry_added_automatically_to_showdown_contestuser_has_already_placed_more_than_the_maximum_amounts_of_bets_allowed_on_that_eventexample_team_size_is_configured_as_5_in_cmsuser_placed_6___5_a_side_betsfirst_placed_5___5_a_side_bets_are_qualified_for_leaderboard_and_the_entries_are_displayed_in_leaderboard_page6th___5_a_side_bet_was_restricted_to_enter_leaderboard_due_to_team_size_configured(self):
        """
        DESCRIPTION: Verify the entry added automatically to Showdown Contest
        DESCRIPTION: *User has already placed more than the maximum amounts of bets allowed on that event*
        DESCRIPTION: **Example:** Team size is configured as **5** in CMS
        DESCRIPTION: User placed **6** - 5-A Side bets
        DESCRIPTION: First placed **5** - 5-A Side bets are qualified for Leaderboard and the entries are displayed in Leaderboard page
        DESCRIPTION: **6th** - 5-A Side bet was restricted to enter Leaderboard due to Team Size configured
        EXPECTED: **Entered Leaderboard 5-A Side bets are Voided**
        EXPECTED: * Voided 5-A Side bets Entry are removed from Leaderboard
        EXPECTED: * Restricted 5-A Side bets which did not enter Leaderboard due to Team size limit previously should be now automatically added **(Since existing entries got removed from Leaderboard)**
        """
        pass

    def test_008_navigate_to_my_betsvalidate_the_5_a_side_bets_displayed_in_open_betsvalidate_the_5_a_side_bets_displayed_in_settled_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        DESCRIPTION: Validate the 5-A Side bets displayed in Open Bets
        DESCRIPTION: Validate the 5-A Side bets displayed in Settled bets
        EXPECTED: **Open Bets**
        EXPECTED: 1: User should be able to view the placed 5-A Side bets (Voided bets should not be displayed
        EXPECTED: **Settled Bets**
        EXPECTED: 2: User should be able to view only Voided 5-A Side bets
        """
        pass
