import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28608_Verify_Favourite_Matches_icon_for_Logged_out_user(Common):
    """
    TR_ID: C28608
    NAME: Verify 'Favourite Matches' icon for Logged out user
    DESCRIPTION: This Test Case verify 'Favourite Matches' icon for Logged out user
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7986 ''Favourite Matches' functionality for Logged out players'
    PRECONDITIONS: 1. User is logged out
    PRECONDITIONS: 2. User is on Football landing page
    PRECONDITIONS: **NOTE**: Favourites should be turned off for Ladbrokes
    """
    keep_browser_open = True

    def test_001_tap_on_football_event(self):
        """
        DESCRIPTION: Tap on Football Event
        EXPECTED: *   Event details page is opened
        EXPECTED: *   Event details page contains the 'Favourite Matches' icon below visualization/scoreboard
        """
        pass

    def test_002_tap_on_the_favourite_matches_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon
        EXPECTED: Oxygen app loads the 'Log in' overlay where the user can log in
        """
        pass

    def test_003_enter_user_credentials_and_press_log_in(self):
        """
        DESCRIPTION: Enter user credentials and press 'Log In'
        EXPECTED: *   user is redirect to the previous page
        EXPECTED: *   favourite event is displayed in the 'Favourite Matches' page (for mobile)/widget (for desktop)
        """
        pass

    def test_004_log_out_from_the_application_and_verify_favourite_matches_icon_and_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Log out from the application and verify 'Favourite Matches' icon and 'Favourite Matches' page/widget
        EXPECTED: * User is logged out and redirected to the homepage
        EXPECTED: * Favorite icon is no longer checked
        EXPECTED: * Favourite Matches on Sports landing page is equal to '0'
        EXPECTED: * Event from Step 3 is not displayed on 'Favourite Matches' page/widget
        """
        pass

    def test_005_repeat_steps_1_5_for____in_play_tab___matches_tab___coupons_tab___jackpot_tab_if_jackpot_pool_is_available(self):
        """
        DESCRIPTION: Repeat steps 1-5 for :​
        DESCRIPTION: *   'In-Play' tab
        DESCRIPTION: *   'Matches' tab
        DESCRIPTION: *   'Coupons' tab
        DESCRIPTION: *   'Jackpot' tab if Jackpot Pool is available
        EXPECTED: 
        """
        pass
