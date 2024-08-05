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
class Test_C28650_Verify_Results_on_Competitions_pages(Common):
    """
    TR_ID: C28650
    NAME: Verify Results on Competitions pages
    DESCRIPTION: This test case verifies Result section/widget on the Competitions page.
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: Results Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {domains} for different environments:
    PRECONDITIONS: * TST2: https://spark-br-tst.symphony-solutions.eu/api
    PRECONDITIONS: * STG2: https://spark-br-stg2.symphony-solutions.eu/api
    PRECONDITIONS: * PROD: https://spark-br.symphony-solutions.eu/api
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

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: 
        """
        pass

    def test_002_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        pass

    def test_003_choose_some_competition_from_expanded_class_accordion_and_clicktap_on_it(self):
        """
        DESCRIPTION: Choose some competition from expanded 'Class' accordion and click/tap on it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' tab/switcher is selected by default
        """
        pass

    def test_004_open_results_tab(self):
        """
        DESCRIPTION: Open 'Results' tab
        EXPECTED: - 'Results' tab is opened
        EXPECTED: - The latest results accordion is expanded by default
        """
        pass

    def test_005_verify_content_displaying_on_results_pagewidget(self):
        """
        DESCRIPTION: Verify content displaying on 'Results' page/widget
        EXPECTED: * Results for different dates are displayed in separate sections
        EXPECTED: * Result of each event consists of:
        EXPECTED: * Team 1
        EXPECTED: * Score of Team 1 (within black square)
        EXPECTED: * Player_1 minute_1', minute_4'
        EXPECTED: * Team 2
        EXPECTED: * Score of Team 2 (within black square)
        EXPECTED: * Player_2 minute_2', Player_3 minute_3'
        EXPECTED: where
        EXPECTED: *   **Player_1 **has scored at **minute_1** and **minute_4 **for Team 1
        EXPECTED: *   **Player_2 **has scored at **minute_2** for Team 2
        EXPECTED: *   **Player_3 **has scored at **minute_3** for Team 2
        """
        pass

    def test_006_verify_scores_correctness(self):
        """
        DESCRIPTION: Verify scores correctness
        EXPECTED: Scores correspond to **[i].result.fullTime.value **attribute from **?skip=0&limit=8** response,
        EXPECTED: where **i - **number of result for particular event
        """
        pass

    def test_007_verify_ordering_on_results_pagewidget(self):
        """
        DESCRIPTION: Verify ordering on 'Results' page/widget
        EXPECTED: Results are ordered by earliest date first (e.g  Today, Yesterday, Monday 8th August, Sunday 7th August, etc.)
        """
        pass
