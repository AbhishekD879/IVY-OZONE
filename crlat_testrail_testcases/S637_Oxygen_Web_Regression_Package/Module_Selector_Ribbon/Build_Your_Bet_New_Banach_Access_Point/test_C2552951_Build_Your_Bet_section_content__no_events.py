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
class Test_C2552951_Build_Your_Bet_section_content__no_events(Common):
    """
    TR_ID: C2552951
    NAME: 'Build Your Bet' section content - no events
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) on the homepage within mobile, tablet and desktop.
    PRECONDITIONS: **No leagues received from CMS (disabled in CMS) or no Banach events returned today and in the next 5 days**
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=6&tz=time_zone_value
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=YYYY-MM-DDT00:00:00.000Z&dateTo=YYYY-MM-DDT00:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    """
    keep_browser_open = True

    def test_001_open_build_your_bet_sectiontab_when_no_events_are_available_today_and_in_the_next_5_days(self):
        """
        DESCRIPTION: Open Build Your Bet section/tab when no events are available today and in the next 5 days
        EXPECTED: Build Your Bet tab is not displayed
        """
        pass
