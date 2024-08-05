import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C874347_Coral_Only_Tennis_Visualization__IMG(Common):
    """
    TR_ID: C874347
    NAME: Coral Only: Tennis Visualization - IMG
    DESCRIPTION: This test case verifies Tennis Visualization for events with a linked IMG visualization.
    DESCRIPTION: Hint: When it comes to **prod** endpoints, usually only events with IMG provider stream have IMG visualization as well.
    PRECONDITIONS: * Oxygen App is opened; Tennis Event Details Page(EDP) is opened.
    PRECONDITIONS: * To check whether Tennis LIVE event has an IMG visualization please use **'vis'** value within Filter of 'XHR' request in Dev Tools - there should be a request containing *providerName: "img"* parameter/value:
    PRECONDITIONS: ![](index.php?/attachments/get/57235744)
    PRECONDITIONS: All information regarding data displayed within the visualization iframe is taken from WebSockets. User **'vis'** value within Filter of 'WS' web services in Dev Tools to find the web socket channel containing messages with data:
    PRECONDITIONS: ![](index.php?/attachments/get/57235745)
    PRECONDITIONS: * info related to OpenBet event (eventName, className, typeName etc) comes in **\"generic\"** packet. Use **'generic'** value within Regex filter under 'Messages' tab:
    PRECONDITIONS: ![](index.php?/attachments/get/57235755)
    PRECONDITIONS: * historic info about event comes in **"history\"** packet. Use **'history'** value within Regex filter under 'Messages' tab:
    PRECONDITIONS: ![](index.php?/attachments/get/57235757)
    PRECONDITIONS: * info about statistic comes in **"statistics\"** packet. Use **'statistics'** value within Regex filter under 'Messages' tab:
    PRECONDITIONS: ![](index.php?/attachments/get/57550422)
    PRECONDITIONS: * info about incidents comes in **"incident\"** packets. Use **'statistics'** value within Regex filter under 'Messages' tab:
    PRECONDITIONS: ![](index.php?/attachments/get/57668305)
    PRECONDITIONS: How to map visualization on *non-prod* environments: https://confluence.egalacoral.com/display/SPI/Tennis+User+Guides
    """
    keep_browser_open = True

    def test_001_verify_visualization_iframe_contents(self):
        """
        DESCRIPTION: Verify Visualization iframe contents
        EXPECTED: * Tennis Visualization iframe is loaded with 'Match Live' tab selected by default
        EXPECTED: * Court with match visualization is displayed and is loaded as 3D straight away
        EXPECTED: ![](index.php?/attachments/get/57668308)
        EXPECTED: * All UI elements are loaded at once
        """
        pass

    def test_002_verify_content_of_match_live_tab(self):
        """
        DESCRIPTION: Verify content of 'Match Live' tab
        EXPECTED: 'Match Live' tab consists of the following elements:
        EXPECTED: * Player Names with Flag icon
        EXPECTED: ![](index.php?/attachments/get/57668309)
        EXPECTED: * Score Box with score of current game
        EXPECTED: ![](index.php?/attachments/get/57668310)
        EXPECTED: * Message line
        EXPECTED: ![](index.php?/attachments/get/57668311)
        EXPECTED: * Score line with set's results
        EXPECTED: ![](index.php?/attachments/get/57668313)
        EXPECTED: * Court surface
        EXPECTED: ![](index.php?/attachments/get/57668314)
        """
        pass

    def test_003_verify_incidents_displaying(self):
        """
        DESCRIPTION: Verify incidents displaying
        EXPECTED: * Message line is updated with information about corresponding incident (comes in **"incident\"** packets)
        EXPECTED: * Corresponding animation is played on the court
        EXPECTED: ![](index.php?/attachments/get/57668475)
        EXPECTED: * Score box and line are updated
        """
        pass

    def test_004_navigate_to_match_stats_tab(self):
        """
        DESCRIPTION: Navigate to 'Match Stats' tab
        EXPECTED: 'Match Statistics' tab is opened
        EXPECTED: ![](index.php?/attachments/get/57668472)
        """
        pass

    def test_005_verify_content_of_match_stats_tab(self):
        """
        DESCRIPTION: Verify content of 'Match Stats' tab
        EXPECTED: 'Match Stats' tab consists of the following elements:
        EXPECTED: * Player Names with Flag icons
        EXPECTED: ![](index.php?/attachments/get/57668473)
        EXPECTED: * List of different statistiсs
        EXPECTED: ![](index.php?/attachments/get/57668474)
        """
        pass

    def test_006_verify_player_names_view(self):
        """
        DESCRIPTION: Verify Player Names view
        EXPECTED: Player Names are shown at the top of the page in format:
        EXPECTED: <player name 1> 'flag icon' 'Head to Head' 'flag icon' <player name 2>
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
        EXPECTED: Corresponding statistic values are displayed for each player (comes in **"statistics\"** packet)
        """
        pass
