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
class Test_C61618997_Verify_the_entry_to_Contest_when_Multiple_Contests_are_with_Same_Event_ID(Common):
    """
    TR_ID: C61618997
    NAME: Verify the entry to Contest when Multiple Contests are with Same Event ID
    DESCRIPTION: This test case verifies the entry to Contest when there are Multiple Contest with Same Event ID
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
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
    PRECONDITIONS: 6: **TEST ACCOUNT** should be enabled in CMS for one of the Contest
    PRECONDITIONS: 7: **REAL ACCOUNTS** should be enabled in CMS for the other Contest
    PRECONDITIONS: 8: For both the Contest Same Event ID should be configured
    PRECONDITIONS: **Asset Management**
    PRECONDITIONS: 1: Team Flags can be configured in CMS > BYB > ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: **To Qualify for Leaderboard**
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

    def test_001_login_to_ladbrokes_with_test_user(self):
        """
        DESCRIPTION: Login to Ladbrokes with Test User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_lobby(self):
        """
        DESCRIPTION: Navigate to 5-A Side Lobby
        EXPECTED: * User should be able to view Real Account enabled Contest and Test Account enabled Contest
        """
        pass

    def test_003_click_on_any_one_of_the_contestboth_contest_should_have_same_event_id(self):
        """
        DESCRIPTION: Click on any one of the Contest
        DESCRIPTION: (Both Contest should have same Event ID)
        EXPECTED: User should be navigated to Leaderboard Page(Pre)
        """
        pass

    def test_004_click_on_build_team(self):
        """
        DESCRIPTION: Click on Build Team
        EXPECTED: User should be navigated to 5-A Side Pitch View
        """
        pass

    def test_005_place_qualifying_bet_eligible_for_both_contest(self):
        """
        DESCRIPTION: Place qualifying bet eligible for both Contest
        EXPECTED: * User should be able to Place bet successfully
        EXPECTED: * User should be displayed entry confirmation from the Contest with Test Account Enabled
        """
        pass

    def test_006_navigate_to_leaderboard_page_of_the_contest_with_test_account_enabled(self):
        """
        DESCRIPTION: Navigate to Leaderboard page of the Contest (with Test Account Enabled)
        EXPECTED: * User should be able to see the Entry in My Entry section
        """
        pass

    def test_007_navigate_to_leaderboard_page_of_the_contest_with_real_account_enabled(self):
        """
        DESCRIPTION: Navigate to Leaderboard page of the Contest (with Real Account Enabled)
        EXPECTED: * User should not see the entry to the Contest
        """
        pass
