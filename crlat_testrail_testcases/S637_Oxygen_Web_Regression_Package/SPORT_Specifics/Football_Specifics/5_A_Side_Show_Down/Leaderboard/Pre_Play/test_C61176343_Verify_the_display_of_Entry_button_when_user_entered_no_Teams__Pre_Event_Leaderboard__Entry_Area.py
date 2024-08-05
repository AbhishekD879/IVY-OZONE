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
class Test_C61176343_Verify_the_display_of_Entry_button_when_user_entered_no_Teams__Pre_Event_Leaderboard__Entry_Area(Common):
    """
    TR_ID: C61176343
    NAME: Verify the display of Entry button when user entered no Teams - Pre-Event Leaderboard - Entry Area
    DESCRIPTION: This test case verifies the display of Rules , Entry area information and CTA button
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
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
    PRECONDITIONS: **Asset Management**
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

    def test_001_verify_the_display_of_sub_header__blurb(self):
        """
        DESCRIPTION: Verify the display of Sub Header & Blurb
        EXPECTED: * Title should be *5-A-Side Showdown*
        EXPECTED: * The game blurb should be displayed as configured in CMS(it can be multiple lines)
        """
        pass

    def test_002_verify_the_display_of_rules_icons_text(self):
        """
        DESCRIPTION: Verify the display of Rules Icons/ Text
        EXPECTED: * **Stake information** - "Place a minimum [Entry Stake] 5-A-Side bet with 5 players" where  [Entry Stake] is pulled from the CMS
        EXPECTED: * **Winning method** - "Teams are ranked by the highest to lowest riced winning bets, then all losing bets by the highest percentage complete". This text should be added in the CMS (perhaps in the Static Blocks area), note - it is not contest specific text.
        EXPECTED: * **Maximum Entries per User** - "Maximum [Teams] entries per user (X/[Teams])" where  [Teams]  is pulled from the 'Teams' field in the CMS. If 'Teams' field is empty, then do not display this rule.  X=number of entries customer has already entered (can be 0)
        EXPECTED: * **Maximum Entries** - "Maximum [Entries] total entries (Y/[Entries])" where [Entries] is pulled from the 'Size' field in the CMS. If 'Size' field is empty, then do not display this rule. Y=number of entries currently entered into the Showdown when the page was loaded.
        EXPECTED: **NOTE: Information "Maximum Entries per User" + "Maximum Entries" are displayed against the same icon** (see designs)
        EXPECTED: ![](index.php?/attachments/get/134277361)
        EXPECTED: **When *Size* and *Teams* field are left blank in CMS**
        EXPECTED: * **Maximum Entries per User** and **Maximum Entries** should not be displayed
        EXPECTED: ![](index.php?/attachments/get/134277368)
        """
        pass

    def test_003_verify_the_display_of_rules_button_and_ga_tag_for_the_same(self):
        """
        DESCRIPTION: Verify the display of Rules button and GA tag for the same
        EXPECTED: * Rules button is displayed as per the designs
        EXPECTED: *Tap on Rules button*
        EXPECTED: * Rules overlay should be opened
        EXPECTED: * Rules button should be GA tagged
        """
        pass

    def test_004_entry_button_when_customer_has_not_entereduser_did_not_enter_a_team_in_showdown_contest_navigate_to_pre_event_leaderboard_verify_the_display_of_entry_button(self):
        """
        DESCRIPTION: **Entry Button when customer has not entered**
        DESCRIPTION: **User did not enter a Team in Showdown contest**
        DESCRIPTION: * Navigate to Pre-Event Leaderboard
        DESCRIPTION: * Verify the display of Entry button
        EXPECTED: * **Build Team** CTA should be displayed
        EXPECTED: Click on Build Team
        EXPECTED: * User should be navigated to 5-A Side Pitch view
        EXPECTED: ![](index.php?/attachments/get/134277356)
        """
        pass

    def test_005_entry_button_in_logged_out_statecontest_maximum_entries_should_not_be_full(self):
        """
        DESCRIPTION: **Entry Button in logged out state**
        DESCRIPTION: *Contest maximum entries should not be full*
        EXPECTED: * **Build Team** button should be displayed
        EXPECTED: Click on Build Team
        EXPECTED: * User should be navigated to 5-A Side Pitch view
        """
        pass

    def test_006_validate_the_ga_tag_for_build_team(self):
        """
        DESCRIPTION: Validate the GA tag for Build Team
        EXPECTED: * Build Team should be GA tagged
        """
        pass