import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2009887_Displaying_and_ordering_of_leagues_in_the_BYB_tab(Common):
    """
    TR_ID: C2009887
    NAME: Displaying and ordering of leagues in the BYB tab
    DESCRIPTION: This test case verifies displaying and ordering of leagues in the BYB tab
    DESCRIPTION: AUTOTEST [C2727319]
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

    def test_001_verify_ordering_of_leagues_in_today__upcoming_tab(self):
        """
        DESCRIPTION: Verify ordering of leagues in 'Today' / 'Upcoming' tab
        EXPECTED: The order of leagues which appear in BYB is defined by the order defined in CMS>YourCall>YourCall Leagues
        """
        pass

    def test_002_verify_correctness_of_leagues_and_their_events_displaying_in_today_section(self):
        """
        DESCRIPTION: Verify correctness of leagues and their events displaying in 'Today' section
        EXPECTED: Events happening 'Today' appear within their League in the 'Today' section of BYB corresponding to Request for Banach upcoming leagues/Banach events of particular league for defined period of time from precondition
        """
        pass

    def test_003_verify_correctness_of_leagues_and_their_events_displaying_in_upcoming_section(self):
        """
        DESCRIPTION: Verify correctness of leagues and their events displaying in "Upcoming" section
        EXPECTED: Events happening in the future appear within their League in the 'Upcoming' section of BYB corresponding Request for Banach upcoming leagues/Banach events of particular league for defined period of time from precondition
        """
        pass
