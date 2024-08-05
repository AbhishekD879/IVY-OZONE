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
class Test_C62700733_Verify_the_navigation_when_user_clicks_on_Standard_Leaderboard_URL_in_third_party_application(Common):
    """
    TR_ID: C62700733
    NAME: Verify the navigation when user clicks on Standard Leaderboard URL in third party application.
    DESCRIPTION: This test case verifies the navigation of Standard Leaderboard URL
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
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.""""""
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_1_copy_the_standard_leaderboard_url_from_invitational_contest_cmssteps_mentioned_in_pre_conditions_and_share_it_in_teams(self):
        """
        DESCRIPTION: 1. Copy the Standard Leaderboard URL from invitational contest CMS,(Steps mentioned in Pre-conditions) and share it in teams
        EXPECTED: 1. Standard Leaderboard URL should be available.
        """
        pass

    def test_002_2_click_on_the_standard_leaderboard_url_shared_in_teams(self):
        """
        DESCRIPTION: 2. Click on the Standard Leaderboard URL shared in teams
        EXPECTED: 2. When navigated through the Standard Leaderboard URL in Teams, it should open Ladbrokes web and navigate to Pre-leaderboard of the contest configured.
        """
        pass

    def test_003_3_when_the_user_is_in_logged_out_state(self):
        """
        DESCRIPTION: 3. when the user is in Logged out state
        EXPECTED: 3 Pre-leaderboard with Login/Join CTA button should be available
        """
        pass

    def test_004_4_when_the_user_is_in_logged_in_state(self):
        """
        DESCRIPTION: 4. when the user is in Logged in state
        EXPECTED: 4. Pre-Leaderboard with Build team CTA button should be available.
        """
        pass