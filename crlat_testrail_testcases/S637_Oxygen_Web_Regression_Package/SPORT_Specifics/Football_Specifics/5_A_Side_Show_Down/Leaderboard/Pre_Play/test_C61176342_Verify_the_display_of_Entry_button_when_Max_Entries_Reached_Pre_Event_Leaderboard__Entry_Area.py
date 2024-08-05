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
class Test_C61176342_Verify_the_display_of_Entry_button_when_Max_Entries_Reached_Pre_Event_Leaderboard__Entry_Area(Common):
    """
    TR_ID: C61176342
    NAME: Verify the display of Entry button when Max Entries Reached- Pre-Event Leaderboard - Entry Area
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

    def test_002_entry_button_when_customer_has_entered_max_teamsuser_has_reached_his_teams_limit_to_enter_the_showdown_contestlets_say_a_user_enters_the_showdown_contest_with_10_teams_and_the_limit_is_10_teams_from_user_navigate_to_pre_event_leaderboard_verify_the_display_of_entry_button(self):
        """
        DESCRIPTION: **Entry Button when customer has entered max teams**
        DESCRIPTION: **User has reached his Teams limit to enter the Showdown Contest**
        DESCRIPTION: *Let's say A user enters the showdown contest with 10 teams and the limit is 10 teams from user*
        DESCRIPTION: * Navigate to Pre-Event Leaderboard
        DESCRIPTION: * Verify the display of Entry button
        EXPECTED: * **Max Entries Reached** *(<# Entries User entered/Max entries allowed per User)* Button should be inactive
        EXPECTED: * User should not be able to click on the CTA
        EXPECTED: ![](index.php?/attachments/get/134277330)
        """
        pass

    def test_003_entry_button_when_contest_is_fullshowdown_contest_entries_reached_maximum_limit_navigate_to_pre_event_leaderboard_verify_the_display_of_entry_button(self):
        """
        DESCRIPTION: **Entry Button when contest is full**
        DESCRIPTION: **Showdown Contest entries reached maximum limit**
        DESCRIPTION: * Navigate to Pre-Event Leaderboard
        DESCRIPTION: * Verify the display of Entry button
        EXPECTED: * **Contest Full** Button should be inactive
        EXPECTED: * User should not be able to click on the CTA
        EXPECTED: Note-- *For both Logged in Logged out customer Contest Full CTA should be displayed*
        EXPECTED: ![](index.php?/attachments/get/134277351)
        """
        pass

    def test_004_when_user_reached_max_entries_and_also_the_contest_is_full_navigate_to_pre_event_leaderboard_verify_the_display_of_entry_button(self):
        """
        DESCRIPTION: **When User reached Max entries and also the Contest is Full**
        DESCRIPTION: * Navigate to Pre-Event Leaderboard
        DESCRIPTION: * Verify the display of Entry button
        EXPECTED: * **Contest Full** Button should be inactive
        EXPECTED: * User should not be able to click on the CTA
        EXPECTED: ![](index.php?/attachments/get/134277351)
        """
        pass
