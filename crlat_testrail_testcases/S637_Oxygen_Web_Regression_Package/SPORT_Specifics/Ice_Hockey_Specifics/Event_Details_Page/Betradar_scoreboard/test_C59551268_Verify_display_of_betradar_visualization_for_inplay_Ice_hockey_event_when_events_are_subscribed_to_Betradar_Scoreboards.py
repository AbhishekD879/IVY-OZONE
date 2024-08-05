import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C59551268_Verify_display_of_betradar_visualization_for_inplay_Ice_hockey_event_when_events_are_subscribed_to_Betradar_Scoreboards(Common):
    """
    TR_ID: C59551268
    NAME: Verify display of betradar visualization for inplay Ice hockey event when event(s) are subscribed to Betradar Scoreboards
    DESCRIPTION: This test case verifies display of betradar visualization for an inplay Ice hockey event.
    DESCRIPTION: How to check event is mapped to betradar or not?
    DESCRIPTION: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    DESCRIPTION: Confluence link:
    DESCRIPTION: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    PRECONDITIONS: Make sure you have LIVE Ice Hockey Event which is subscribed to Betradar Scoreboards
    """
    keep_browser_open = True

    def test_001_navigate_to_ice_hockey_inplay_event_landing_page_from_a_z_menu___table_tennis___inplay_taborhome___inplay___ice_hockey(self):
        """
        DESCRIPTION: Navigate to Ice hockey inplay event landing page from A-Z menu - table tennis - inplay tab
        DESCRIPTION: Or
        DESCRIPTION: Home - Inplay - Ice hockey
        EXPECTED: Ice hockey event landing page should display with list of inplay events
        EXPECTED: Live now tab(# of inplay events)
        """
        pass

    def test_002_verify_ice_hockey_inplay_landing_page(self):
        """
        DESCRIPTION: verify Ice hockey inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1. Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Fall back score board with live score should display
        EXPECTED: 3. Ball indication(Coral beside player name and Lads beside to fallback scoreboard) should display
        EXPECTED: 4. Odds should update as per feed from OB
        EXPECTED: 5. markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_verify_scoreboard_in_edp_page(self):
        """
        DESCRIPTION: Verify Scoreboard in EDP page
        EXPECTED: + Event Name with 'Live' icon, date and time format(day,dd-MMM-YY HH:MM) is displayed in EDP header
        EXPECTED: + Scoreboard and Ice hockey court with match visualizations(betradar) should be displayed in Event details page
        """
        pass
