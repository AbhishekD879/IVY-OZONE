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
class Test_C61176325_Verify_display_of_View_Entry_on_Entry_Confirmation_for_Leaderboard_in_Bet_Receipt(Common):
    """
    TR_ID: C61176325
    NAME: Verify display of View Entry on Entry Confirmation for Leaderboard in Bet Receipt
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

    def test_003_place_a_5_a_side_bet_satisfying_the_pre_conditions_mentioned(self):
        """
        DESCRIPTION: Place a 5-A side bet satisfying the pre-conditions mentioned
        EXPECTED: User should be able to place 5-A Side bet successfully
        """
        pass

    def test_004_verify_the_entry_confirmation_displayed_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Entry Confirmation displayed on the bet receipt
        EXPECTED: * Entry Confirmation notification should be displayed below the 'Bet Placed Successfully' Header
        EXPECTED: * 5-A Side Ladbrokes image should be displayed (Configured in CMS > Image Manager)
        EXPECTED: * **Your team has been entered into a 5-A-Side Entry!** message should be displayed as title header
        EXPECTED: * Secondary message should be displayed **[Configured in CMS > Contest Details page > 'Entry Confirmation Text']**
        EXPECTED: * **VIEW ENTRY** CTA button should be displayed
        EXPECTED: ![](index.php?/attachments/get/151963659)
        """
        pass

    def test_005__verify_view_entry_cta_click_on_view_entry_cta(self):
        """
        DESCRIPTION: * Verify View Entry CTA
        DESCRIPTION: * Click on View Entry CTA
        EXPECTED: * View Entry should be displayed
        EXPECTED: * User should be able to click View Entry button
        EXPECTED: * User should be navigated to Leaderboard page of that contest
        """
        pass
