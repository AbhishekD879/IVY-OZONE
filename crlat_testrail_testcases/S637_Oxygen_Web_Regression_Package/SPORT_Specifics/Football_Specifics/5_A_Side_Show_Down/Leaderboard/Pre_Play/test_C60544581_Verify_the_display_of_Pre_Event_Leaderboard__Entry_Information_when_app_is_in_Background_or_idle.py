import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C60544581_Verify_the_display_of_Pre_Event_Leaderboard__Entry_Information_when_app_is_in_Background_or_idle(Common):
    """
    TR_ID: C60544581
    NAME: Verify the display of Pre-Event Leaderboard - Entry Information when app is in Background or idle.
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

    def test_004_verify_the_display_my_entrieswhen_user_has_more_than_one_entry_in_showdown(self):
        """
        DESCRIPTION: Verify the display My Entries
        DESCRIPTION: **When User has more than One Entry in showdown**
        EXPECTED: * All entries should be displayed under My Entries [X/Y]
        EXPECTED: Where X is User entries in that Contest and Y is Maximum Entries per User (Defined in CMS > Contest Details Page > Teams)
        EXPECTED: * When Maximum entries per User (Teams) is not configured in CMS
        EXPECTED: My Entries [X] should be displayed where X is User entries in that Contest
        EXPECTED: * Entries should be ordered based on Odds/Price - Higher odds entry should be displayed first
        EXPECTED: * Positions should be displayed 1,2,3..
        EXPECTED: The position reflects the position of that team within that
        EXPECTED: user's own personal leaderboard. E.G. If they have 5 teams
        EXPECTED: at different prices, then they will be ranked on price and
        EXPECTED: have positions 1,2,3,4,5 ranked accordingly. Teams of the
        EXPECTED: same odds will have a tied position.
        EXPECTED: * Username should be displayed with last three characters marked as ***
        EXPECTED: * Price /Odds should be displayed *@2/1* below Username
        EXPECTED: * Progress bar should be displayed as 0%
        """
        pass

    def test_005_verify_the_display_of_my_entrieswhen_user_entries_have_tied_position(self):
        """
        DESCRIPTION: Verify the display of My Entries
        DESCRIPTION: **When User entries have Tied Position**
        EXPECTED: **Tied Position**
        EXPECTED: Tie should be displayed as 'X='
        EXPECTED: where X is the entry highest position
        """
        pass

    def test_006_click_anywhere_on_the_expanded_entry_except_on_team_progress(self):
        """
        DESCRIPTION: Click anywhere on the expanded entry (Except on Team Progress)
        EXPECTED: Entry should be Collapsed
        """
        pass

    def test_007_move_the_app_or_desktop_to_idle_position_or_to_background_for_some_timethen_move_the_app_to_foreground_after_sometime(self):
        """
        DESCRIPTION: Move the app or Desktop to idle position or to background for some time.
        DESCRIPTION: Then move the app to foreground after sometime.
        EXPECTED: * All the data should be updated and present on the screen, No data should be lost & all the data should be updated.
        """
        pass
