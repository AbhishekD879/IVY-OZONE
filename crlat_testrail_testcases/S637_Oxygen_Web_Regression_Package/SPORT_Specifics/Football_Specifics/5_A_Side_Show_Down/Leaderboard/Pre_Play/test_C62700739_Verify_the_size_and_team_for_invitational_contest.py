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
class Test_C62700739_Verify_the_size_and_team_for_invitational_contest(Common):
    """
    TR_ID: C62700739
    NAME: Verify the size and team for invitational contest.
    DESCRIPTION: This test case verifies the size and team of a contest
    PRECONDITIONS: """""""1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contest should be created in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: Contest Criteria
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: Invitation contest creation :
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: 6. Invitation toggle should be enabled in contest creation page.
    PRECONDITIONS: 7. Standard Leaderboard URL will be generated once the contest is saved.
    PRECONDITIONS: Asset Management
    PRECONDITIONS: 1: Team Flags can be configured in CMS &gt; BYB &gt; ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.""
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_1_login_to_fe_ladbrokes_application(self):
        """
        DESCRIPTION: 1. Login to FE Ladbrokes application
        EXPECTED: 1. User should be able to login successfully
        """
        pass

    def test_002_2_navigate_through_standard_leaderboard_url_or_from_football_landing_page_and_click_on_build_team(self):
        """
        DESCRIPTION: 2. Navigate through Standard Leaderboard URL or from Football Landing page and click on Build team
        EXPECTED: 2. It will navigate to 5-A-Side pitch
        """
        pass

    def test_003_3_build_a_team_and_click_on_placebet_and_select_freebet(self):
        """
        DESCRIPTION: 3. Build a team and click on placebet and select Freebet
        EXPECTED: 3. Entry confirmation message is displayed after placing the bet with eligible stake.
        """
        pass

    def test_004_4_verify_the_entry_confirmation_message(self):
        """
        DESCRIPTION: 4. Verify the entry confirmation message
        EXPECTED: 4. The same message that is configured in the contest level should be displayed in FE in Betslip.
        """
        pass

    def test_005_5_check_if_teams_are_entered_into_the_same_contest_after_the_contest_and_team_size_are_full(self):
        """
        DESCRIPTION: 5. Check if teams are entered into the same contest after the contest and team size are full.
        EXPECTED: 5. After contest and team size is met with the configured value in CMS, then No entry confirmation message from the same contest should be displayed anymore, but should be placed normally.
        """
        pass
