import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.build_your_bet
@vtest
class Test_C2745409_Changing_display_and_order_for_BYB_leagues_in_CMS(Common):
    """
    TR_ID: C2745409
    NAME: Changing display and order for BYB leagues in CMS
    DESCRIPTION: This testcase verifies that changing order and disabling YourCall leagues in CMS is reflected on Build Your Bet tab on Homepage
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available on Build Your Bet tab when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    """
    keep_browser_open = True

    def test_001_in_cms_your_call__yourcall_leagues_move_one_league_above_any_other_leagues_in_cmsyourcallyourcall_leagues_which_is_available_on_build_your_bet_tab_from_preconditions(self):
        """
        DESCRIPTION: In CMS >Your Call > YourCall leagues move one League above any other Leagues in CMS>YourCall>YourCall Leagues which is available on Build Your Bet tab from preconditions
        EXPECTED: On Oxygen landing page verify the order of leagues which appear in BYB is defined by the order defined in CMS>YourCall>YourCall Leagues
        """
        pass

    def test_002_disable_all_leagues_that_are_happening_today_or_within_the_next_5_days_in_cmsyourcallyourcall_leagues(self):
        """
        DESCRIPTION: Disable all leagues that are happening today or within the next 5 days in CMS>YourCall>YourCall Leagues
        EXPECTED: Only one section of BYB component ("Today's" or "Upcoming") is displayed depending on whether this events are happening today or within 5 next day.
        """
        pass

    def test_003_disable_all_leagues_that_are_happening_today_and_within_the_next_5_days_in_cmsyourcallyourcall_leagues(self):
        """
        DESCRIPTION: Disable all leagues that are happening today and within the next 5 days in CMS>YourCall>YourCall Leagues
        EXPECTED: "Today's" and "Upcoming" section of BYB component should disappear.
        """
        pass

    def test_004_verify_when_no_events_for_the_league_received(self):
        """
        DESCRIPTION: Verify when no events for the league received
        EXPECTED: Leagues are not appearing when no events for that league have been received for the timeframe being viewed corresponding to Request for Banach upcoming leagues/Banach events of particular league for defined period of time from precondition
        """
        pass
