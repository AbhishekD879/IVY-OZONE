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
class Test_C28653_Verify_Show_More_Dates_option_on_Results_page_widget_on_the_Competition_page(Common):
    """
    TR_ID: C28653
    NAME: Verify 'Show More Dates' option on 'Results' page/widget on the Competition page 
    DESCRIPTION: This test case verifies 'See More Dates' option on 'Results' page and 'Show more' on Results' widget of the Competition page.
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

    def test_004_choose_some_competition_from_expanded_class_accordion_and_clicktap_it(self):
        """
        DESCRIPTION: Choose some competition from expanded 'Class' accordion and click/tap it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' tab/switcher is selected by default
        EXPECTED: * 'Results' widget is displayed (if applicable) for **Desktop**
        """
        pass

    def test_005_for_mobiletabletselect_results_tab_and_check_number_of_events_displayed(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Select 'Results' tab and check number of events displayed
        EXPECTED: Maximum 7 events are displayed
        """
        pass

    def test_006_for_desktopcheck_number_of_events_displayed_on_results_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check number of events displayed on 'Results' widget
        EXPECTED: Maximum 3 events are displayed
        """
        pass

    def test_007_verify_see_more_dates_button_presence(self):
        """
        DESCRIPTION: Verify 'See More Dates' button presence
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'See More Dates' button is displayed under last seventh event
        EXPECTED: * 'See More Dates' button is missing if there are less than 7 events
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Show More' button is displayed under last third event
        EXPECTED: * 'Show More' button is missing if there are less than 3 events
        """
        pass

    def test_008_clicktap_on_see_more_dates_button_and_verify_more_events_appear(self):
        """
        DESCRIPTION: Click/Tap on 'See More Dates' button and verify more events appear
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Previous 7 days events are loaded
        EXPECTED: * 'See More Dates' button is present below the last event if there are more events
        EXPECTED: **For Desktop:**
        EXPECTED: * Previous and 8 more events are displayed
        EXPECTED: * 'Show More' button is present below the last event if there are more events
        """
        pass

    def test_009_repeat_step_8(self):
        """
        DESCRIPTION: Repeat step 8
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Previous 7 days events are loaded
        EXPECTED: * 'See More Dates' button is present below the last event if there are more events
        EXPECTED: **For Desktop:**
        EXPECTED: * Previous and 8 more events are displayed
        EXPECTED: * 'Show More' button is present below the last event if there are more events
        """
        pass

    def test_010_repeat_step_8_until_all_events_are_displayed_and_check_see_more_dates_button_missing(self):
        """
        DESCRIPTION: Repeat step 8 until all events are displayed and check  'See More Dates' button missing
        EXPECTED: 'See More Dates' button is not present under last event when all events are displayed
        """
        pass
