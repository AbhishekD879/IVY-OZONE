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
class Test_C62701299_Verify_when_logged_in_user_has_locked_the_device_and_after_unlocking_LB_widget_is_displayed_automatically(Common):
    """
    TR_ID: C62701299
    NAME: Verify when logged in user has locked the device and after unlocking, LB widget is displayed automatically
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: 4: Event should start and User should enter the contest for the Leaderboard widget to be displayed
    PRECONDITIONS: Configurations for Leaderboard widget
    PRECONDITIONS: 1: Home Page
    PRECONDITIONS: 2: Football Page
    PRECONDITIONS: 3: My Bets
    PRECONDITIONS: CMS admin user should be able to enable/ disable the above toggles
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_1login_to_sportsbook_application_with_user_that_has_entered_into_any_live_event_contest2navigate_to_fbhome_page3observe_lb_widget_is_displayed4lock_device_for_few_minutes_min_15min5unlock_device6observe_widget_is_displayed(self):
        """
        DESCRIPTION: "1.Login to sportsbook application with user that has entered into any live event contest
        DESCRIPTION: 2.Navigate to fb/home page
        DESCRIPTION: 3.Observe LB widget is displayed
        DESCRIPTION: 4.Lock device for few minutes (min 15min)
        DESCRIPTION: 5.Unlock device
        DESCRIPTION: 6.Observe widget is displayed"
        EXPECTED: "1.User should be loggedin
        EXPECTED: 2.User should be navigated to fb/home page
        EXPECTED: 3.LB widget should be displayed
        EXPECTED: 4.App/browser should be locked for minimum of 15min
        EXPECTED: 5.App/browser should be unlocked
        EXPECTED: 6.LB Widget should be displayed"
        """
        pass

    def test_002_navigate_to_fbhome_page(self):
        """
        DESCRIPTION: Navigate to fb/home page
        EXPECTED: User should be navigated to fb/home page
        """
        pass

    def test_003_observe_lb_widget_is_displayed(self):
        """
        DESCRIPTION: Observe LB widget is displayed
        EXPECTED: LB widget should be displayed
        """
        pass

    def test_004_lock_device_for_few_minutes_min_15min(self):
        """
        DESCRIPTION: Lock device for few minutes (min 15min)
        EXPECTED: App/browser should be locked for minimum of 15min
        """
        pass

    def test_005_unlock_device(self):
        """
        DESCRIPTION: Unlock device
        EXPECTED: App/browser should be unlocked
        """
        pass

    def test_006_observe_widget_is_displayed(self):
        """
        DESCRIPTION: Observe widget is displayed
        EXPECTED: LB Widget should be displayed
        """
        pass
