import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C2553032_Desktop_Build_Your_Bet_section_content_and_layout(Common):
    """
    TR_ID: C2553032
    NAME: Desktop: Build Your Bet section content and layout
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) tab content and layout of event cards on desktop
    DESCRIPTION: AUTOTEST [C2696906]
    PRECONDITIONS: Check the following requests in Dev tools > Network > XHR:
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop:
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    PRECONDITIONS: **Build Your Bet module ribbon tab is opened**
    """
    keep_browser_open = True

    def test_001_verify_accordions_and_events_within_todayupcoming_sections(self):
        """
        DESCRIPTION: Verify accordions and events within Today/Upcoming sections
        EXPECTED: - 2 league accordions are expanded by default
        EXPECTED: - "Today" section with events received from "Banach" starting today
        EXPECTED: - "Upcoming" section with events received from "Banach" within the next 5 days
        """
        pass

    def test_002_verify_expanding_a_league_accordion(self):
        """
        DESCRIPTION: Verify expanding a league accordion
        EXPECTED: - League accordion is expanded
        EXPECTED: - Accordion chevron is in expanded state
        EXPECTED: - Request for Banach events of particular league for defined period of time from preconditions is sent after expanding a league accordion
        """
        pass

    def test_003_verify_collapsing_a_league_accordion(self):
        """
        DESCRIPTION: Verify collapsing a league accordion
        EXPECTED: - Accordion is collapsed
        EXPECTED: - Accordion chevron is in collapsed state
        """
        pass

    def test_004_verify_events_cards_layout_within_accordions(self):
        """
        DESCRIPTION: Verify events cards layout within accordions
        EXPECTED: - Event cards are displayed in 3 columns if there are 3 and more events in the accordion
        EXPECTED: - The last (the only) event card is stretched to the width of the accordion (when there is an number of events which is divided by 3 with remainder 1 )
        EXPECTED: - 2 last events are stretched to the width of the accordion (when there is an number of events which is divided by 3 with remainder 2 )
        """
        pass

    def test_005_verify_event_card_information(self):
        """
        DESCRIPTION: Verify event card information
        EXPECTED: Event card contains:
        EXPECTED: - Match name
        EXPECTED: - Match date and time
        EXPECTED: - "Add to favorite" button (ONLY for Coral)
        EXPECTED: - "Go to event" link
        """
        pass
