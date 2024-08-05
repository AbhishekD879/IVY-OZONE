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
class Test_C61618940_Verify_the_display_of_Entry_Information_Single_Entry__Pre_Event_Leaderboard(Common):
    """
    TR_ID: C61618940
    NAME: Verify the display of Entry Information_Single Entry - Pre Event Leaderboard
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

    def test_003_verify_the_display_my_entrieswhen_user_has_only_one_entry_in_showdown(self):
        """
        DESCRIPTION: Verify the display My Entries
        DESCRIPTION: **When User has Only One Entry in showdown**
        EXPECTED: * My Entry should be displayed
        EXPECTED: * User Entry should be displayed
        EXPECTED: * Position should be displayed as 1
        EXPECTED: * Progress bar should be displayed as 0%
        EXPECTED: * Username should be displayed with last three characters marked as ***
        EXPECTED: * Price /Odds should be displayed *@2/1* below Username
        EXPECTED: ![](index.php?/attachments/get/130405345)
        """
        pass

    def test_004_tap_on_one_entry(self):
        """
        DESCRIPTION: Tap on one Entry
        EXPECTED: * Entry should be Expanded displaying all the selections for the Team
        """
        pass

    def test_005_tap_on_another_entry(self):
        """
        DESCRIPTION: Tap on another entry
        EXPECTED: * Entry should expand
        EXPECTED: * Already opened entry should be collapsed
        """
        pass

    def test_006_click_anywhere_on_the_expanded_entry_except_on_team_progress(self):
        """
        DESCRIPTION: Click anywhere on the expanded entry (Except on Team Progress)
        EXPECTED: Entry should be Collapsed
        """
        pass
