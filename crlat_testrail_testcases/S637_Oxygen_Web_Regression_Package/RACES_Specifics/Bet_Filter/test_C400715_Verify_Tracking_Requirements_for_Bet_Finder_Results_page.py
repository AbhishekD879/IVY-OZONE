import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C400715_Verify_Tracking_Requirements_for_Bet_Finder_Results_page(Common):
    """
    TR_ID: C400715
    NAME: Verify Tracking Requirements for Bet Finder Results page
    DESCRIPTION: This test case verifies Tracking Requirements for Bet Finder Results. Sorting by Odds/Time is available only for Sportsbook version of Bet Finder.
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-2439 Web: Results page
    PRECONDITIONS: Use
    PRECONDITIONS: Sportsbook/Coral:
    PRECONDITIONS: https://connect-invictus.coral.co.uk/#/horseracing
    PRECONDITIONS: https://connect-invictus.coral.co.uk/#/bet-finder/
    PRECONDITIONS: NOTE: Open browser console (F12) -> Network -> request 'collect?v' -> Headers might not be available for connect-invictus.coral.co.uk
    """
    keep_browser_open = True

    def test_001_load_httpsconnect_invictuscoralcoukhorseracing(self):
        """
        DESCRIPTION: Load https://connect-invictus.coral.co.uk/#/horseracing
        EXPECTED: Horse Racing page is loaded
        """
        pass

    def test_002_tap_bet_filter_link_on_the_breadcrumb__tap_find_betsopen_browser_console_f12___network___request_collectv___headers(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link on the breadcrumb > Tap 'Find Bets'.
        DESCRIPTION: Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        EXPECTED: User is redirected to Bet Filter Results screen.
        EXPECTED: Check values of following parameters:
        EXPECTED: dl:https://connect-app-tst1.coral.co.uk/
        EXPECTED: dp:/bet-finder/results
        """
        pass

    def test_003_verify_sort_by_odds_tracking_tap_sort_by_odds1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_second_last_object(self):
        """
        DESCRIPTION: Verify Sort by ODDS tracking. Tap Sort by ODDS.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand second last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:sorting
        EXPECTED: el:sort - by odds
        EXPECTED: 2. Verify:
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction:"sorting"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"sort - by odds"
        """
        pass

    def test_004_verify_sort_by_time_tracking_tap_sort_by_time1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_second_last_object(self):
        """
        DESCRIPTION: Verify Sort by TIME tracking. Tap Sort by TIME.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand second last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:ea:sorting
        EXPECTED: el:sort - by time
        EXPECTED: 2. Verify:
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction:"sorting"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"sort - by time"
        """
        pass
