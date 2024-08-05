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
class Test_C2552950_Build_Your_Bet_section_content__only_Upcoming_events(Common):
    """
    TR_ID: C2552950
    NAME: 'Build Your Bet' section content - only Upcoming events
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) on the homepage within mobile, tablet and desktop.
    PRECONDITIONS: Banach events are receiving only for future (the next 5 days), no Today's events
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/table:
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: desktop:
    PRECONDITIONS: Widgets -> 'Build Your Bet';  'Build Your Bet' is active;
    PRECONDITIONS: Leagues is available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    """
    keep_browser_open = True

    def test_001_open_build_your_bet_sectiontab(self):
        """
        DESCRIPTION: Open Build Your Bet section/tab
        EXPECTED: *  Only "Upcoming" section is displayed
        EXPECTED: *  There is no "Today" section, there is no switcher between Today and Upcoming
        """
        pass