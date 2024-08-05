import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870295_1Customer_taps_on_Bet_History_on_my_accounts_to_check_the_history_tracked_under_this_tab(Common):
    """
    TR_ID: C44870295
    NAME: 1.Customer taps on Bet History  on my accounts to check the history tracked under this tab
    DESCRIPTION: It is verify Bet History and its contents.
    PRECONDITIONS: Used should be logged in
    PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
    PRECONDITIONS: User should have some settled bets.
    """
    keep_browser_open = True

    def test_001_launch_the_siteapp(self):
        """
        DESCRIPTION: Launch the site/App
        EXPECTED: The site is launched
        """
        pass

    def test_002_log_in_with_user_credentials_that_have_previous_bets_placed_and_navigate_to_my_bets(self):
        """
        DESCRIPTION: Log in with user credentials that have previous bets placed and navigate to My bets
        EXPECTED: User is logged in and previous bets are displayed on My Bets
        """
        pass

    def test_003_verify_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: Cashout/Open bets/Settled bets/Shop bets
        EXPECTED: All bets must be displayed with the right details
        EXPECTED: for all types of bets - single, multiple, E/W, cashed out bets, HR etc
        """
        pass

    def test_004_verify_functionality_of_date_picker_today_last_7_days_and_last_30_days_from_bet_history_via_my_account_overlay(self):
        """
        DESCRIPTION: Verify functionality of Date Picker Today, Last 7 days and Last 30 days from Bet History via My Account overlay
        EXPECTED: Date Picker Today, Last 7 days and Last 30 days must be functional and working as per design implementation
        """
        pass
