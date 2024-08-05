import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28652_Verify_goalscorers_displaying_on_Results_page_widget(Common):
    """
    TR_ID: C28652
    NAME: Verify goalscorers displaying on 'Results' page/widget
    DESCRIPTION: This test case verifies goalscorers displaying within event section on 'Results' page/widget.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: Results Widget is available ONLY for Football sport
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request to get Spark id for competition user is viewing (see value in “competitionId”):
    PRECONDITIONS: **{domain}/brcompetitionseason/XX/YY/ZZZ**,
    PRECONDITIONS: where
    PRECONDITIONS: * XX - OB category id (e.g. Football - id=16)
    PRECONDITIONS: * YY - OB class id (e.g. Football England - id=97)
    PRECONDITIONS: * ZZZ - OB type id (e.g. Premier League - id=442)
    PRECONDITIONS: A list of seasons with their IDs for selected competition:
    PRECONDITIONS: **{domain}/seasons/1/XX/YY**,
    PRECONDITIONS: where
    PRECONDITIONS: * 1 - Spark category id for Football
    PRECONDITIONS: * XX - Spark country id
    PRECONDITIONS: * YY - Spark competitions id
    PRECONDITIONS: Results for the selected season:
    PRECONDITIONS: **{domain}/season/XXXXX/matches/?skip=0&limit=4** for desktop OR **limit=8** for mobile,
    PRECONDITIONS: where
    PRECONDITIONS: * XXXXX - Spark season id
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_pageopen_development_tool_in_browser_network_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        DESCRIPTION: Open development tool in browser> 'Network' tab
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        """
        pass

    def test_002_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        pass

    def test_003_choose_some_competition_from_expanded_class_accordion_and_clicktap_it(self):
        """
        DESCRIPTION: Choose some competition from expanded 'Class' accordion and click/tap it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' tab/switcher is selected by default
        EXPECTED: * 'Results' widget is displayed (if applicable) for **Desktop**
        """
        pass

    def test_004_for_mobiletabletselect_results_tab(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Select 'Results' tab
        EXPECTED: * 'Results' tab is selected
        EXPECTED: * Data received from response is displayed on the page
        EXPECTED: * The latest results accordion is expanded by default
        """
        pass

    def test_005_verify_player_name_and_time_displaying_when_a_goal_was_scored(self):
        """
        DESCRIPTION: Verify player name and time displaying when a goal was scored
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Player name and minute are displayed next to team name for each team (if data is available)
        EXPECTED: **For Desktop:**
        EXPECTED: * Player name and minute are displayed below team name for each team (if data is available)
        EXPECTED: * Player names and minutes are displayed in several rows if it doesn't fit in one row
        """
        pass

    def test_006_verify_player_name_correctness(self):
        """
        DESCRIPTION: Verify player name correctness
        EXPECTED: Player name corresponds to **[i]goals.playerName** attribute from **?skip=0&limit=8** response,
        EXPECTED: where **[i] playerName
        EXPECTED: ![](index.php?/attachments/get/118619998)
        """
        pass

    def test_007_verify_the_time_when_a_goal_was_scored(self):
        """
        DESCRIPTION: Verify the time when a goal was scored
        EXPECTED: Minute corresponds to **[i].goals.[k].time** attribute from **?skip=0&limit=8** response
        EXPECTED: where
        EXPECTED: *   **i** - number of result for particular event
        EXPECTED: *   **k** - number of goals
        EXPECTED: ![](index.php?/attachments/get/118630687)
        """
        pass

    def test_008_check_in_network_tab_that_player_request_is_missing_to_stats_centrerequest_url_httpsstats_centrecoralcoukapiplayer(self):
        """
        DESCRIPTION: Check in Network tab that **player** request is missing to stats centre
        DESCRIPTION: (Request URL: https://stats-centre.coral.co.uk/api/player)
        EXPECTED: **player** request is not present in Network
        """
        pass
