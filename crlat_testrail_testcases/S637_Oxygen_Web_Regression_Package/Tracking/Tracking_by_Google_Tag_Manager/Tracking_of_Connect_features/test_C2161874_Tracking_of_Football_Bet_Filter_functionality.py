import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2161874_Tracking_of_Football_Bet_Filter_functionality(Common):
    """
    TR_ID: C2161874
    NAME: Tracking of Football Bet Filter functionality
    DESCRIPTION: Jira ticket:
    DESCRIPTION: HMN-3090 Coupon Buddy: Integrate Coupon Buddy into the Connect app
    DESCRIPTION: HMN-3184 Web: Coupon Buddy UI changes
    PRECONDITIONS: * Select 'Connect' from header sports ribbon -> Coupon landing page is opened
    PRECONDITIONS: * Tap Football Bet Filter -> 'You're betting' CTA is shown so user
    PRECONDITIONS: * Tap 'Online' OR 'In-Shop' button -> Football Bet Filter Page is opened
    """
    keep_browser_open = True

    def test_001_load_football_bet_filter_pageopen_browser_console_f12___network___request_collectv___headers(self):
        """
        DESCRIPTION: Load Football Bet Filter page
        DESCRIPTION: Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        EXPECTED: Football Bet Filter page is opened
        EXPECTED: Check values of following parameters:
        EXPECTED: dl:https://*****.coral.co.uk/bet-filter/filters/yourTeams
        EXPECTED: dp:/bet-filter/filters/yourTeams
        """
        pass

    def test_002_verify_tracking_added_to_info_button_open_browser_console_f12___network___request_collectv___headers_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify tracking added to Info button
        DESCRIPTION: * Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: * Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: * Check values of following parameter:
        EXPECTED: dl: https://******/bet-filter/filters/yourTeams
        EXPECTED: dp: /bet-filter/filters/yourTeams
        EXPECTED: ec: football filter
        EXPECTED: ea: info
        EXPECTED: * Verify:
        EXPECTED: betFilterStep:"<selected tab>" (yourTeams or The Opposition)
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"info"
        EXPECTED: eventCategory:"football filter"
        """
        pass

    def test_003_verify_tracking_added_to_all_the_betting_criteria_at_your_teams__playing_at__last_game__last_6_games_point_total__key_trends__league_positions__odds(self):
        """
        DESCRIPTION: Verify tracking added to all the betting criteria at YOUR TEAMS:
        DESCRIPTION: - Playing at
        DESCRIPTION: - Last game
        DESCRIPTION: - Last 6 games point total
        DESCRIPTION: - Key trends
        DESCRIPTION: - League positions
        DESCRIPTION: - Odds
        EXPECTED: * Check values of following parameter in Network (collect):
        EXPECTED: ec:[Criteria]
        EXPECTED: ea:[value]
        EXPECTED: e.g.
        EXPECTED: ea:Playing At
        EXPECTED: el:Home
        EXPECTED: * Verify:
        EXPECTED: betFilterStep:"Your Teams"
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"Playing At" [Criteria]
        EXPECTED: eventCategory:"football filter"
        EXPECTED: eventLabel:"Home" [value]
        EXPECTED: gtm.uniqueEventId:12
        EXPECTED: userAction:"selected"
        """
        pass

    def test_004_verify_tracking_added_to_reset_button_open_browser_console_f12___network___request_collectv___headers_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify tracking added to RESET button
        DESCRIPTION: * Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: * Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: * Check values of following parameters:
        EXPECTED: ec:football filter
        EXPECTED: ea:reset
        EXPECTED: * Verify:
        EXPECTED: betFilterStep:"Your Teams"
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"reset"
        EXPECTED: eventCategory:"football filter"
        """
        pass

    def test_005_verify_tracking_added_to_screen_tabsswitch_between1_your_teams_and_2_the_opposition_open_browser_console_f12___network___request_collectv___headers_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify tracking added to screen tabs.
        DESCRIPTION: Switch between
        DESCRIPTION: 1. YOUR TEAMS and 2. THE OPPOSITION
        DESCRIPTION: * Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: * Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: * Check values of following parameter:
        EXPECTED: dp:/bet-filter/filters/opposition {yourTeams}
        EXPECTED: * Verify:
        EXPECTED: event:"content-view"
        EXPECTED: gtm.uniqueEventId:6
        EXPECTED: screen_name:"/bet-filter/filters/yourTeams"  OR   "/bet-filter/filters/opposition"
        """
        pass

    def test_006_verify_tracking_added_to_all_the_betting_criteria_at_the_opposition__last_game__last_6_games_point_total__key_trends__league_positions(self):
        """
        DESCRIPTION: Verify tracking added to all the betting criteria at THE OPPOSITION:
        DESCRIPTION: - Last game
        DESCRIPTION: - Last 6 games point total
        DESCRIPTION: - Key trends
        DESCRIPTION: - League positions
        EXPECTED: * Check values of following parameter in Network (collect):
        EXPECTED: ec:[Criteria]
        EXPECTED: ea:[value]
        EXPECTED: * Verify:
        EXPECTED: betFilterStep:"The Opposition"
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"Last Game" [Criteria]
        EXPECTED: eventCategory:"football filter"
        EXPECTED: eventLabel:"Win" [value]
        EXPECTED: gtm.uniqueEventId:12
        EXPECTED: userAction:"selected"
        """
        pass

    def test_007_verify_tracking_added_to_find_bets(self):
        """
        DESCRIPTION: Verify tracking added to FIND BETS
        EXPECTED: * Check values of following parameter in Network (collect):
        EXPECTED: ec:football filter
        EXPECTED: ea:find bets
        EXPECTED: and in the next collect request:
        EXPECTED: dp:/coupon-buddy
        EXPECTED: * Verify in Console:
        EXPECTED: betFilterStep:"The Opposition"
        EXPECTED: couponSelection:""
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"find bets"
        EXPECTED: eventCategory:"football filter"
        EXPECTED: eventLabel:1
        EXPECTED: gtm.uniqueEventId:38
        EXPECTED: oppositionSelection:"7 - 12 points"
        EXPECTED: teamSelection:"Home|Win|High Scoring|Top Half|Favourite"
        EXPECTED: AND
        EXPECTED: redirect to "/coupon-buddy" in the next object
        """
        pass
