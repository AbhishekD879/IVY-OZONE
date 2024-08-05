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
class Test_C61618970_Verify_the_display_Entry_Expansion_Pre_Event_Leaderboard_page(Common):
    """
    TR_ID: C61618970
    NAME: Verify the display Entry Expansion_Pre-Event Leaderboard page
    DESCRIPTION: This Test case verifies the display of Entry Information on Pre-Event Leaderbaord.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: 4: Event should be in Pre-Play
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: **Contest Criteria**
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: Asset Management
    PRECONDITIONS: 1: Team Flags can be configured in CMS > BYB > ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: **To Qualify for Showdown**
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

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_showdown__contest__leaderboard(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown > Contest > Leaderboard
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_verify_the_display_my_entrieswhen_user_entry_is_expanded_in_showdown(self):
        """
        DESCRIPTION: Verify the display My Entries
        DESCRIPTION: **When User Entry is expanded in showdown**
        EXPECTED: * My Entry should be displayed
        EXPECTED: * User Entry should be displayed
        EXPECTED: * Position should be displayed as 1
        EXPECTED: * Progress bar should be displayed as 0%
        EXPECTED: * Username should be displayed with last three characters marked as ***
        EXPECTED: * Price /Odds should be displayed *@2/1* below Username
        EXPECTED: ![](index.php?/attachments/get/130405345)
        """
        pass

    def test_004_verify_the_display_of_my_entrieswhen_user_entries_have_tied_position(self):
        """
        DESCRIPTION: Verify the display of My Entries
        DESCRIPTION: **When User entries have Tied Position**
        EXPECTED: **Tied Position**
        EXPECTED: Tie should be displayed as 'X='
        EXPECTED: where X is the entry highest position
        """
        pass

    def test_005_click_anywhere_on_the_expanded_entry_except_on_team_progress(self):
        """
        DESCRIPTION: Click anywhere on the expanded entry (Except on Team Progress)
        EXPECTED: Entry should be Collapsed
        """
        pass
