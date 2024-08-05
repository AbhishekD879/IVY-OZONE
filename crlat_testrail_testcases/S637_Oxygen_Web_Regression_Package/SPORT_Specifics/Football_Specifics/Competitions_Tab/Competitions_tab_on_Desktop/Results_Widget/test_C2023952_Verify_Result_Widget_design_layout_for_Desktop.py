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
class Test_C2023952_Verify_Result_Widget_design_layout_for_Desktop(Common):
    """
    TR_ID: C2023952
    NAME: Verify Result Widget design/layout for Desktop
    DESCRIPTION: This test case verifies Results Widget design/layout for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
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

    def test_004_choose_some_competition_that_has_results_widget_from_expanded_class_accordion_and_click_it(self):
        """
        DESCRIPTION: Choose some competition that has 'Results' Widget from expanded 'Class' accordion and click it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * 'Results' Widget is displayed in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_005_verify_header_accordion_of_result_widget(self):
        """
        DESCRIPTION: Verify header accordion of Result Widget
        EXPECTED: * Header contains capitalized text: 'Results' and up/down facing chevron
        EXPECTED: * Header accordion is collapsible/expandable to realize possibility of hiding/showing widget content
        EXPECTED: * On hover Header accordion color changes
        """
        pass

    def test_006_verify_content_displaying_on_results_widget(self):
        """
        DESCRIPTION: Verify content displaying on 'Results' widget
        EXPECTED: 'Results' page/widget consists of:
        EXPECTED: * Results for different date is displayed in separate sections:
        EXPECTED: * Team 1/Team 2
        EXPECTED: * Score of Team 1/Score of Team 2
        EXPECTED: * Player_1 minute_1', minute_4'/Player_2 minute_1', minute_4'
        EXPECTED: * Date is displayed in the next format on each separate section: Today, Yesterday, 8th August 2018, etc.)
        """
        pass

    def test_007_verify_footer_of_result_widget(self):
        """
        DESCRIPTION: Verify footer of Result Widget
        EXPECTED: Footer contains capitalized 'Show More' link
        """
        pass
