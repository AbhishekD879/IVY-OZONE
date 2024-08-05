import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28651_Verify_availability_of_Results_Widget_for_Desktop(Common):
    """
    TR_ID: C28651
    NAME: Verify availability of 'Results' Widget for Desktop
    DESCRIPTION: This test case verifies availability of 'Results' Widget for Desktop.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
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

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        """
        pass

    def test_003_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        pass

    def test_004_choose_some_competition_that_has_results_widget_from_expanded_class_accordion_and_clicktap_it(self):
        """
        DESCRIPTION: Choose some competition that has 'Results' Widget from expanded 'Class' accordion and click/tap it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * 'Results' Widget is displayed in 3rd column
        """
        pass

    def test_005_switch_to_outrights_tab(self):
        """
        DESCRIPTION: Switch to 'Outrights' tab
        EXPECTED: * List of Outrights events is loaded on the page
        EXPECTED: * 'Results' Widget is displayed in 3rd column
        """
        pass

    def test_006_verify_position_of_results_widget(self):
        """
        DESCRIPTION: Verify position of 'Results' Widget
        EXPECTED: * 'Results' Widget is shown in 3rd column at 1280px and higher screen resolution
        EXPECTED: * 'Results' Widget is shown in 2nd column below the list of competition events at 1279px and lower screen resolutions
        """
        pass

    def test_007_verify_condition_when_results_widget_is_shown(self):
        """
        DESCRIPTION: Verify condition when 'Results' Widget is shown
        EXPECTED: 'Results' Widget is shown in case data for selected competition/season is received from Spark.
        EXPECTED: Use this request to verify:
        EXPECTED: **{domain}/season/XXXXX/matches/?skip=0&limit=4**
        EXPECTED: where
        EXPECTED: * XXXXX - Spark season id
        EXPECTED: In case 'Data not found' is returned ('Preview' tab), widget is NOT shown
        """
        pass

    def test_008_navigate_to_competition_details_page_for_which_data_is_not_received(self):
        """
        DESCRIPTION: Navigate to Competition Details page for which data is not received
        EXPECTED: * 'Results' Widget is not shown
        EXPECTED: * 'League Table' Widget is shown in case it's available
        EXPECTED: * 2nd column extends to occupy 3rd column in case none of the widgets available
        """
        pass
