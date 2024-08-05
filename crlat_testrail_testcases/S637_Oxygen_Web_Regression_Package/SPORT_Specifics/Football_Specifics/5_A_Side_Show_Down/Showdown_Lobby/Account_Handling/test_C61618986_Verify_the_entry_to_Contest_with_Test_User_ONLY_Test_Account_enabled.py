import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C61618986_Verify_the_entry_to_Contest_with_Test_User_ONLY_Test_Account_enabled(Common):
    """
    TR_ID: C61618986
    NAME: Verify the entry to Contest with Test User ONLY Test Account enabled
    DESCRIPTION: This test case verifies the entry into the Contest when logged in with Test User (ONLY Test Account Enabled in CMS)
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
    PRECONDITIONS: 6: **TEST ACCOUNT** should be enabled in CMS
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

    def test_001_launch_ladbrokes(self):
        """
        DESCRIPTION: Launch Ladbrokes
        EXPECTED: User should be able to launch ladbrokes application successfully
        """
        pass

    def test_002_login_with_a_test_user(self):
        """
        DESCRIPTION: Login with a Test User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_003_navigate_to_5_a_side_lobby(self):
        """
        DESCRIPTION: Navigate to 5-A Side lobby
        EXPECTED: User should be able to view the Lobby
        """
        pass

    def test_004_navigate_to_the_contest_displayed_in_lobby_and_click_on_the_cardcontest_in_cms_should_have_test_account_enabled(self):
        """
        DESCRIPTION: Navigate to the Contest displayed in Lobby and click on the Card
        DESCRIPTION: **CONTEST in CMS should have Test Account Enabled**
        EXPECTED: User should be navigated to Leaderboard page (Pre)
        """
        pass

    def test_005_click_on_build_team(self):
        """
        DESCRIPTION: Click on Build Team
        EXPECTED: User should be navigated to 5-A Side Pitch view
        """
        pass

    def test_006_place_qualifying_bet_to_the_contest(self):
        """
        DESCRIPTION: Place qualifying bet to the Contest
        EXPECTED: * User should be able to place the bet successfully
        EXPECTED: * User should be displayed Entry Confirmation
        EXPECTED: * User should enter the Contest
        """
        pass

    def test_007_navigate_to_leaderboard_page_pre(self):
        """
        DESCRIPTION: Navigate to Leaderboard Page (Pre)
        EXPECTED: * My Entry section should be displayed
        EXPECTED: * User entry should be displayed
        """
        pass
