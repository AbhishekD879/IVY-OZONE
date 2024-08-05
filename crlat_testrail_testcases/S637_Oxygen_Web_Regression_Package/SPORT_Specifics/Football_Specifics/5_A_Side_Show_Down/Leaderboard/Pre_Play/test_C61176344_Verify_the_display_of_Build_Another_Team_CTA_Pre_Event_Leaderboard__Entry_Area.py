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
class Test_C61176344_Verify_the_display_of_Build_Another_Team_CTA_Pre_Event_Leaderboard__Entry_Area(Common):
    """
    TR_ID: C61176344
    NAME: Verify the display of Build Another Team CTA- Pre-Event Leaderboard - Entry Area
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

    def test_002_entry_button_when_customer_has_entered_and_can_enter_againuser_has_entered_teams_in_showdown_contest_but_did_not_exceed_the_maximum_entries_navigate_to_pre_event_leaderboard_verify_the_display_of_entry_button(self):
        """
        DESCRIPTION: **Entry Button when customer has entered and can enter again**
        DESCRIPTION: **User has entered Teams in Showdown Contest but did not exceed the maximum entries**
        DESCRIPTION: * Navigate to Pre-Event Leaderboard
        DESCRIPTION: * Verify the display of Entry button
        EXPECTED: * **Build Another Team** CTA should be displayed
        EXPECTED: Click on Build Another Team
        EXPECTED: * User should be navigated to 5-A Side Pitch view
        EXPECTED: ![](index.php?/attachments/get/134277355)
        """
        pass

    def test_003_validate_the_ga_tag_for_build_another_team(self):
        """
        DESCRIPTION: Validate the GA tag for Build Another Team
        EXPECTED: * Build Another Team should be GA tagged
        """
        pass
