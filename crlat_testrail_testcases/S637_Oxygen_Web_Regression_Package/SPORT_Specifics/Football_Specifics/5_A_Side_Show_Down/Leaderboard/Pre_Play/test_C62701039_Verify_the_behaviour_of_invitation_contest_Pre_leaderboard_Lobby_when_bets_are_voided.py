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
class Test_C62701039_Verify_the_behaviour_of_invitation_contest_Pre_leaderboard_Lobby_when_bets_are_voided(Common):
    """
    TR_ID: C62701039
    NAME: Verify the behaviour of invitation contest Pre leaderboard & Lobby when bets are voided.
    DESCRIPTION: This test case verifies the voided bets behaviour
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
    PRECONDITIONS: 8. Place bets before Line-ups and few should be voided.
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

    def test_002_2_navigate_to_pre_leaderboard_through_lobby_and__check_for_voided_bets(self):
        """
        DESCRIPTION: 2. Navigate to Pre-Leaderboard through lobby and  check for voided bets
        EXPECTED: 2. Team voided should not be displayed in Pre-Leaderboard anymore.
        """
        pass

    def test_003_3_verify_the_contest_and_team_size(self):
        """
        DESCRIPTION: 3. Verify the contest and team size.
        EXPECTED: 3. The voided bet count should be reduced from Contest and Team size accurately.
        """
        pass
