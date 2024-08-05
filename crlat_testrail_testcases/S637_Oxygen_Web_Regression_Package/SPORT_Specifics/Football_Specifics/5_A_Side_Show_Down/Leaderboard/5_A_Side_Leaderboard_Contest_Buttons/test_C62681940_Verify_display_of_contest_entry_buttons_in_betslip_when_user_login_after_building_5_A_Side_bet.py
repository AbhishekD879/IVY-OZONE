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
class Test_C62681940_Verify_display_of_contest_entry_buttons_in_betslip_when_user_login_after_building_5_A_Side_bet(Common):
    """
    TR_ID: C62681940
    NAME: Verify display of contest entry buttons in betslip when user login after building 5-A-Side bet
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

    def test_001_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest
        EXPECTED: User should be optin to that contest and contest should be added to the lobby
        """
        pass

    def test_002_navigate_to_5_a_side_event_and_add_5_legs_to_betslip_or_navigate_to_5_a_side_lobby_gtnavigate_to_contest_pre_leaderboard_page_gt_and_click_on_loginjoin_to_enter_in_logged_out_state(self):
        """
        DESCRIPTION: Navigate to 5-A-Side event and add 5 legs to betslip or Navigate to 5-A-Side lobby-&gt;Navigate to contest Pre-Leaderboard page-&gt; and click on Login/Join to Enter in logged out state
        EXPECTED: User should be taken to 5-A-Side pitch and add 5 legs to betslip in logged out state
        """
        pass

    def test_003_click_on_place_bet(self):
        """
        DESCRIPTION: Click on place bet
        EXPECTED: User should be able to click place bet
        """
        pass

    def test_004_check_if_you_are_prompted_to_loginregister_page(self):
        """
        DESCRIPTION: Check if you are prompted to login/register page
        EXPECTED: User should be prompted to login/register page
        """
        pass

    def test_005_login_to_the_application_now(self):
        """
        DESCRIPTION: Login to the application now
        EXPECTED: User should be able to login now
        """
        pass

    def test_006_check_if_the_contest_entry_buttons_are_displayed_in_betslip(self):
        """
        DESCRIPTION: Check if the contest entry buttons are displayed in betslip
        EXPECTED: Eligible and active contest entry buttons should be present in betslip with the CMS contest creation priority order, first button should be default selected with blue color highlighting.
        """
        pass
