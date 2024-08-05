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
class Test_C44870296_2Customer_can_search_Bet_history_for_Sports_bets_using_From_and_To_date_range(Common):
    """
    TR_ID: C44870296
    NAME: 2.Customer can search Bet history for Sports bets using From and To date range
    DESCRIPTION: Used should be logged in
    DESCRIPTION: User should have some settled bets.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_user_shall_launch_test_appsite(self):
        """
        DESCRIPTION: User shall Launch Test App/Site
        EXPECTED: User successfully Launches Test App/Site
        """
        pass

    def test_002_user_shall_login_with_valid_credentials_who_has_some_settled_bets(self):
        """
        DESCRIPTION: User shall Login with valid credentials who has some settled bets.
        EXPECTED: User successfully Logins with credentials
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

    def test_004_verify_user_can_view_settled_bets_for_given_time_duration_by_setting_the_calendar_dates_from_and_to_dates(self):
        """
        DESCRIPTION: Verify user can view settled bets for given time duration by setting the Calendar dates (From and To Dates)
        EXPECTED: User is able to see all settled bets based on dates range set in calendar.
        """
        pass

    def test_005_verify_bet_history_of_sports_lottopools_tabs(self):
        """
        DESCRIPTION: Verify bet history of 'Sports', 'Lotto','Pools' tabs
        EXPECTED: User is able to see all settled bets based on dates range set in calendar for these different bets.
        """
        pass

    def test_006_verify_user_can_scroll_down_the_past_bet_history(self):
        """
        DESCRIPTION: Verify user can scroll down the past bet history
        EXPECTED: User is able to scroll down and see all bets.
        """
        pass
