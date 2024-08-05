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
class Test_C1317507_Tennis_Visualization_iframe_content(Common):
    """
    TR_ID: C1317507
    NAME: Tennis Visualization iframe content
    DESCRIPTION: This test case verifies content of Tennis Visualization iframe on Tennis Event Details page
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * Make sure you have LIVE tennis events with available Tennis Visualizations mapped (IMG provider)
    PRECONDITIONS: All information is taken from WebSockets:
    PRECONDITIONS: * info related to OpenBet event (eventName, className, typeName etc) comes in **generic** packet
    PRECONDITIONS: * historic info about event comes in **history** packet
    PRECONDITIONS: * info about statistic comes in **statistics** packet
    PRECONDITIONS: * info about incidents comes in **incident** packets
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_live_tennis_events_with_available_visualizations_mapped(self):
        """
        DESCRIPTION: Navigate to Event Details Page of LIVE tennis events with available Visualizations mapped
        EXPECTED: * Event Details Page is opened
        EXPECTED: * Tennis Visualization iframe is loaded with 'Match Live' tab selected by default
        EXPECTED: * Court with match visualization is displayed and is loaded as 3D straight away
        EXPECTED: * All UI elements are loaded at once
        """
        pass

    def test_002_verify_content_of_match_live_tab(self):
        """
        DESCRIPTION: Verify content of 'Match Live' tab
        EXPECTED: 'Match Live' tab consists of the following elements:
        EXPECTED: * Player Names with Flag icon
        EXPECTED: * Score Box with score of current game
        EXPECTED: * Message line
        EXPECTED: * Score line with set's results
        EXPECTED: * Court surface
        """
        pass

    def test_003_verify_incidents_displaying(self):
        """
        DESCRIPTION: Verify incidents displaying
        EXPECTED: * Message line is updated with information about corresponding incident (comes in **incident** packets )
        EXPECTED: * Corresponding animation is played on the court
        EXPECTED: * Score box and line are updated
        """
        pass

    def test_004_navigate_to_match_stats_tab(self):
        """
        DESCRIPTION: Navigate to 'Match Stats' tab
        EXPECTED: 'Match Statistics' tab is opened
        """
        pass

    def test_005_verify_content_of_match_statistics_tab(self):
        """
        DESCRIPTION: Verify content of 'Match Statistics' tab
        EXPECTED: 'Match Statistics' tab consists of the following elements:
        EXPECTED: * Player Names with Flag icons
        EXPECTED: * List of different statistiсs
        """
        pass

    def test_006_verify_player_names_view(self):
        """
        DESCRIPTION: Verify Player Names view
        EXPECTED: Player Names are shown at the top of the page in format:
        EXPECTED: <player name 1> 'flag icon' 'HEAD TO HEAD' 'flag icon' <player name 2>
        """
        pass

    def test_007_verify_list_of_different_statistis(self):
        """
        DESCRIPTION: Verify list of different statistiсs
        EXPECTED: The following types of statistic are displayed for both players:
        EXPECTED: * ACES
        EXPECTED: * DOUBLE FAULTS
        EXPECTED: * BREAKS/BREAK POINTS(%)
        EXPECTED: * MAX POINTS IN A ROW
        EXPECTED: * MAX GAMES IN A ROW
        EXPECTED: * SERVICE POINTS (W/L/All)
        EXPECTED: * SERVICE GAMES (W/L/All)
        EXPECTED: Corresponding statistic values are displayed for each player (comes in **statistics** packet)
        """
        pass
