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
class Test_C62681887_Verify_default_5_a_side_green_glassy_background_Image_is_displayed_in_Pre_live_leader_board_Contests(Common):
    """
    TR_ID: C62681887
    NAME: Verify default 5-a-side green glassy background Image is displayed in Pre-live  leader board Contests
    DESCRIPTION: Verify default 5-a-side green glassy background Image is displayed in Pre-live leader board Contests
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2)  user should not placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_event_and_add_5_legs_to_bet_slip_or_navigate_to_5_a_side_lobby___pre_leaderboard_and_add_5_legs(self):
        """
        DESCRIPTION: Navigate to 5-a-side event and add 5 legs to bet slip or Navigate to 5-a-side lobby -> Pre-leaderboard and add 5 legs
        EXPECTED: User should be able to add 5 legs to bet slip
        """
        pass

    def test_003_enter_valid_stake_for_active_conteststake_should_be__contest_stake(self):
        """
        DESCRIPTION: "Enter valid stake for active contest.
        DESCRIPTION: Stake should be >= contest stake."
        EXPECTED: Entry confirmation message is displayed in bet receipt
        """
        pass

    def test_004_validate_green_glassy_background_in_prelive_leader_boards(self):
        """
        DESCRIPTION: Validate green glassy background in pre/live leader boards
        EXPECTED: Green glassy background in pre/live leader boards should display
        """
        pass
