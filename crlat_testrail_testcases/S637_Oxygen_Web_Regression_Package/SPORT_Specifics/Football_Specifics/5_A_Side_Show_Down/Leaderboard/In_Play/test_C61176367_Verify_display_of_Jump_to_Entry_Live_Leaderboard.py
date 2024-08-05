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
class Test_C61176367_Verify_display_of_Jump_to_Entry_Live_Leaderboard(Common):
    """
    TR_ID: C61176367
    NAME: Verify display of Jump to Entry- Live Leaderboard
    DESCRIPTION: This test case verifies the display of My entries and Position Summary widget in Leaderboard when the match/event is Live
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
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

    def test_003_verify_the_display_of_my_entryonly_one_team_entered_in_the_showdown(self):
        """
        DESCRIPTION: Verify the display of 'My entry'
        DESCRIPTION: **Only one team entered in the Showdown**
        EXPECTED: * User should be able to view My Entry
        EXPECTED: * 'My Entry' section should be displayed at the top of the leaderboard
        """
        pass

    def test_004_tap_on_entry(self):
        """
        DESCRIPTION: Tap on Entry
        EXPECTED: * Detailed Team formation should be displayed
        EXPECTED: * Entry expands to show the detailed team progress with each leg of the bet displaying the following content:
        EXPECTED: * Selection Name
        EXPECTED: * Badge of Team
        EXPECTED: * Progress Bar
        EXPECTED: * Stat Count
        EXPECTED: * Win or Lost indicator (Tick or Cross)
        EXPECTED: * Ladbrokes 5-A-Side Watermark
        EXPECTED: * 'Jump To Entry' should be displayed
        EXPECTED: * Team progress should follow all logic that is part of the My Bets Stat Tracking feature
        EXPECTED: * Team progress should be updated dynamically as per the update logic
        EXPECTED: ![](index.php?/attachments/get/161000425)
        """
        pass

    def test_005_click_on_jump_to_entry(self):
        """
        DESCRIPTION: Click on 'Jump To Entry'
        EXPECTED: * Team should be collapsed
        EXPECTED: * User should be navigated down to that team within the Leaderboard
        EXPECTED: * Jump to Entry should be GA tagged
        """
        pass

    def test_006_verify_the_display_of_my_entriesmultiple_teams_entered_in_the_showdown(self):
        """
        DESCRIPTION: Verify the display of 'My Entries'
        DESCRIPTION: **Multiple teams entered in the Showdown**
        EXPECTED: * 'My Entries' section should be displayed at the top of the leaderboard
        EXPECTED: * Top performing entry (ranked by position) should be displayed among all the entries of the user
        EXPECTED: * 'Jump To Entry' button should be displayed on expansion of the entry
        EXPECTED: **NOTE: The team shown may change over time if another team becomes ranked higher**
        EXPECTED: ![](index.php?/attachments/get/161000427)
        """
        pass

    def test_007_click_on_jump_to_entry(self):
        """
        DESCRIPTION: Click on 'Jump To Entry'
        EXPECTED: * Team should be collapsed
        EXPECTED: * User should be navigated down to that team within the Leaderboard
        EXPECTED: * Jump to Entry should be GA tagged
        """
        pass

    def test_008_verify_the_display_of_position_summary_widgetonly_one_team_entered_in_the_showdown(self):
        """
        DESCRIPTION: Verify the display of Position Summary Widget
        DESCRIPTION: **Only one team entered in the Showdown**
        EXPECTED: * Position Summary Widget should be displayed as per designs
        EXPECTED: * Positions of that team should be reflected by a circle plotted on a horizontal bar with 1st position on the right hand side
        EXPECTED: * The horizontal bar is split into to Colors - the green representing the positions in the prizes and the red representing the other positions
        EXPECTED: * The position should updated dynamically in line with the update logic
        EXPECTED: ![](index.php?/attachments/get/130377903)
        """
        pass

    def test_009_verify_the_display_of_position_summary_widgetmultiple_teams_entered_in_the_showdown(self):
        """
        DESCRIPTION: Verify the display of Position Summary Widget
        DESCRIPTION: **Multiple teams entered in the Showdown**
        EXPECTED: * Position Summary Widget should be displayed as per designs
        EXPECTED: * The positions of all the teams are reflected by circles plotted on a horizontal bar with 1st position on the right hand side
        EXPECTED: * The horizontal bar is split into to colors - the green representing the positions in the prizes and the red representing the other positions
        EXPECTED: * The positions are updated dynamically in line with the update logic
        EXPECTED: * 'View All Entries' Button should be displayed
        EXPECTED: ![](index.php?/attachments/get/130377916)
        EXPECTED: ![](index.php?/attachments/get/161000388)
        EXPECTED: ![](index.php?/attachments/get/130377914)
        """
        pass

    def test_010_tap_on_the_position_summary_widget_area_the_whole_areamultiple_teams_entered_in_the_showdown(self):
        """
        DESCRIPTION: Tap on the Position Summary widget area (the whole area)
        DESCRIPTION: **Multiple teams entered in the Showdown**
        EXPECTED: * The widget should expand to an overlay
        EXPECTED: * This tap should be **GA tracked**
        EXPECTED: * The title should be 'All My Entries (X)' where X=number of entries
        EXPECTED: * All the users teams should be displayed on a personal leaderboard in order of position
        EXPECTED: * All information displayed on the main leaderboard should be displayed for each team
        EXPECTED: * Personal Leaderboard updates as per usual update logic
        EXPECTED: * User should be able to tap on each team to view Detailed Team Progress (follow usual rules of only one team expanded at a time)
        EXPECTED: * 'Jump to Entry' button is present for each team
        EXPECTED: ![](index.php?/attachments/get/161000389)
        EXPECTED: ![](index.php?/attachments/get/130377914)
        """
        pass

    def test_011_click_on_jump_to_entry(self):
        """
        DESCRIPTION: Click on 'Jump To Entry'
        EXPECTED: * Team should be collapsed
        EXPECTED: * Position Summary Widget Overlay (All My Entries [X]) should be Collapsed
        EXPECTED: * User should be navigated down to that team within the Leaderboard
        EXPECTED: * Jump to Entry should be GA tagged
        """
        pass
