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
class Test_C61176330_Verify_Entry_Confirmation_is_not_displayed_when_Criteria_is_not_met(Common):
    """
    TR_ID: C61176330
    NAME: Verify Entry Confirmation is not displayed when Criteria is not met
    DESCRIPTION: This test case verifies the entry confirmation message displayed on Bet receipt
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: **To Qualify for Leaderboard**
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: **The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.**
    """
    keep_browser_open = True

    def test_001_log_into_ladbrokes_application(self):
        """
        DESCRIPTION: Log into Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002__navigate_to_football_edp__5_a_side_click_on_build_a_team(self):
        """
        DESCRIPTION: * Navigate to Football EDP > 5-A Side
        DESCRIPTION: * Click on Build a Team
        EXPECTED: * User should be navigated to Football EDP
        EXPECTED: * User should be navigated to 5-A Side tab
        EXPECTED: * User should be navigated to 5-A Side Pitch view
        """
        pass

    def test_003_place_a_5_a_side_bet_which_does_not_meet_the_criteria_for_entering_showdown(self):
        """
        DESCRIPTION: Place a 5-A Side bet which does not meet the criteria for entering showdown
        EXPECTED: * Normal 5-A Side bet receipt should be displayed
        EXPECTED: * No Entry Notification should be displayed
        EXPECTED: * Bet should be displayed in Open Bets
        """
        pass
