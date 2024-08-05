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
class Test_C62681923_Verify_whether_the_active_and_eligible_contests_that_are_setup_in_cms_are_shown_in_betslip_while_placing_a_5_A_Side_bet(Common):
    """
    TR_ID: C62681923
    NAME: Verify whether the active and eligible contests that are setup in cms are shown in betslip while placing a 5-A-Side bet
    DESCRIPTION: 
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label. 5-A-Side Showdown
    PRECONDITIONS: Path. /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create multiple contests for different events
    PRECONDITIONS: 2. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest
        EXPECTED: User should be optin to that contest and contest should be added to the lobby
        """
        pass

    def test_003_navigate_to_5_a_side_event_and_click_build_team(self):
        """
        DESCRIPTION: Navigate to 5-A-Side event and click Build Team
        EXPECTED: User should be taken to 5-A-Side pitch and add 5 legs to betslip
        """
        pass

    def test_004_verify_whether_the_active_and_opted_contest_entry_buttons_are_shown_on_betslip(self):
        """
        DESCRIPTION: Verify whether the active and opted contest entry buttons are shown on betslip
        EXPECTED: Active and opted contest entry buttons should be present in betslip with the CMS contest creation priority order, first button should be default selected with blue color highlighting.
        """
        pass
