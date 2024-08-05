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
class Test_C62681939_Verify_display_of_contest_using_real_user_when_that_contest_has_test_accounts_checked_in_cms(Common):
    """
    TR_ID: C62681939
    NAME: Verify display of contest using real user when that contest has test accounts checked in cms
    DESCRIPTION: 
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label. 5-A-Side Showdown
    PRECONDITIONS: Path. /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1.Few Contests should be created for future events with real account checked
    PRECONDITIONS: 2. Few contests should be created for future events with test account checked
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

    def test_001_login_to_ladbrokes_application_with_real_account(self):
        """
        DESCRIPTION: Login to ladbrokes application with real account
        EXPECTED: User should be logged in successfully with real account
        """
        pass

    def test_002_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest
        EXPECTED: User should be optin to that contest and contest should be added to the lobby
        """
        pass

    def test_003_navigate_to_5_a_side_event_and_add_5_legs_to_betslip_or_navigate_to_5_a_side_lobby_gt_navigate_to_contest_pre_leaderboard_page_gt_click_on_build_team(self):
        """
        DESCRIPTION: Navigate to 5-A-Side event and add 5 legs to betslip or Navigate to 5-A-Side lobby-&gt; Navigate to contest Pre-Leaderboard page-&gt; click on Build Team
        EXPECTED: User should be taken to 5-A-Side pitch and add 5 legs to betslip
        """
        pass

    def test_004_verify_whether_only__real_account_contest_entry_buttons_are_shown_in_betslip(self):
        """
        DESCRIPTION: Verify whether only  real account contest entry buttons are shown in betslip
        EXPECTED: Only real account contest should be displayed on betslip
        """
        pass

    def test_005_verify_if_any_test_account_contest_entry_buttons_are_displayed_in_betslip(self):
        """
        DESCRIPTION: Verify if any test account contest entry buttons are displayed in betslip
        EXPECTED: There shouldn't  be any test account contest entry buttons displayed
        """
        pass
