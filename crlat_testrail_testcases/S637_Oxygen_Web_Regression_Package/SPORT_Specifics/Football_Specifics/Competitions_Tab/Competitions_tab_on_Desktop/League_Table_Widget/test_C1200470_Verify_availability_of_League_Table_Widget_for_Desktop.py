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
class Test_C1200470_Verify_availability_of_League_Table_Widget_for_Desktop(Common):
    """
    TR_ID: C1200470
    NAME: Verify availability of 'League Table' Widget for Desktop
    DESCRIPTION: This test case verifies conditions when 'League Table' Widget is shown/hidden for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: League Table Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {domains} for different environments:
    PRECONDITIONS: * TST: https://stats-centre-tst0.coral.co.uk/api
    PRECONDITIONS: * PROD: https://stats-centre.coral.co.uk/api/
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
    PRECONDITIONS: Results for selected season:
    PRECONDITIONS: **{domain}/resultstables/1/XX/YY/ZZZZZ**,
    PRECONDITIONS: where
    PRECONDITIONS: * 1 - Spark category id for Football
    PRECONDITIONS: * XX - Spark country id
    PRECONDITIONS: * YY - Spark competitions id
    PRECONDITIONS: * ZZZZZ - Spark season id**Pre-conditions:**
    PRECONDITIONS: League Table Widget is available ONLY for Football sport
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page__gt_competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt; 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        pass

    def test_003_navigate_to_any_competition_details_page_that_has_league_table_widget(self):
        """
        DESCRIPTION: Navigate to any Competition Details page that has 'League Table' Widget
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * 'League Table' Widget is displayed in 3rd column
        """
        pass

    def test_004_switch_to_outrights_tab(self):
        """
        DESCRIPTION: Switch to 'Outrights' tab
        EXPECTED: * List of Outrights events is loaded on the page
        EXPECTED: * 'League Table' Widget is displayed in 3rd column
        """
        pass

    def test_005_verify_position_of_league_table_widget(self):
        """
        DESCRIPTION: Verify position of 'League Table' Widget
        EXPECTED: * 'League Table' Widget is shown in 3rd column at 1280px and higher screen resolution
        EXPECTED: * 'League Table' Widget is shown in 2nd column below the list of competition events at 1279px and lower screen resolutions
        """
        pass

    def test_006_verify_condition_when_league_table_widget_is_shown(self):
        """
        DESCRIPTION: Verify condition when 'League Table' Widget is shown
        EXPECTED: 'League Table' Widget is shown in case data for selected competition/season is received from Spark.
        EXPECTED: Use this request to verify:
        EXPECTED: **{domain}/resultstables/1/XX/YY/ZZZZZ**,
        EXPECTED: where
        EXPECTED: * 1 - Spark category id for Football
        EXPECTED: * XX - Spark country id
        EXPECTED: * YY - Spark competitions id
        EXPECTED: * ZZZZZ - Spark season id
        EXPECTED: In case 'Data not found' is returned ('Preview' tab), widget is NOT shown
        """
        pass

    def test_007_navigate_to_competition_details_page_for_which_data_is_not_received(self):
        """
        DESCRIPTION: Navigate to Competition Details page for which data is not received
        EXPECTED: * 'League Table' Widget is not shown
        EXPECTED: * 'Results' Widget is shown in case it's available
        EXPECTED: * 2nd column extends to occupy 3rd column in case none of the widgets available
        """
        pass
