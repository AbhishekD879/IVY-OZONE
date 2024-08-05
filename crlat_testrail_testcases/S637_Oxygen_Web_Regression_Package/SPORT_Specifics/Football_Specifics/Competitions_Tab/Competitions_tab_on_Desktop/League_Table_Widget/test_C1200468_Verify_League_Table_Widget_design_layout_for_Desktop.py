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
class Test_C1200468_Verify_League_Table_Widget_design_layout_for_Desktop(Common):
    """
    TR_ID: C1200468
    NAME: Verify League Table Widget design/layout for Desktop
    DESCRIPTION: This test case verifies League Table Widget design/layout for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    DESCRIPTION: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5a37a27592b402caa8eb4f4b
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
    PRECONDITIONS: * ZZZZZ - Spark season id
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

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * League Table Widget is displayed in 3rd column
        """
        pass

    def test_004_verify_header_accordion_of_league_table_widget(self):
        """
        DESCRIPTION: Verify header accordion of League Table Widget
        EXPECTED: * Header contains capitalized text: 'League Table' and up/down facing chevron
        EXPECTED: * Header accordion is collapsible/expandable to realize possibility of hiding/showing widget content
        EXPECTED: * On hover Header accordion color changes
        """
        pass

    def test_005_verify_sub_header_of_league_table_widget(self):
        """
        DESCRIPTION: Verify sub header of League Table Widget
        EXPECTED: Sub header contains:
        EXPECTED: * season name of competition user is viewing (e.g. Championship 17/18)
        EXPECTED: * left/right arrows in case of multiple seasons within the same competition
        EXPECTED: * no arrows are displayed in case of 1 season
        """
        pass

    def test_006_verify_table_data(self):
        """
        DESCRIPTION: Verify table data
        EXPECTED: League Table contains info about first 5 teams with the following columns:
        EXPECTED: * POS (position in table)
        EXPECTED: * Team name (Text truncates for long names)
        EXPECTED: * P (stands for 'Plays/Matches total')
        EXPECTED: * W (stands for 'Won total')
        EXPECTED: * D (stands for 'Draw total')
        EXPECTED: * L (stands for 'Lost total')
        EXPECTED: * GD (stands for 'Goal Difference total')
        EXPECTED: * PTS (stands for 'Points total')
        EXPECTED: Content is not clickable
        EXPECTED: Teams appear in the same order as in the following request:
        EXPECTED: {domain}/resultstables/1/XX/YY/ZZZZZ,
        EXPECTED: where
        EXPECTED: XX - Spark country id
        EXPECTED: YY - Spark competition id,
        EXPECTED: ZZZZZ - Spark season id
        """
        pass

    def test_007_verify_footer_of_league_table_widget(self):
        """
        DESCRIPTION: Verify footer of League Table Widget
        EXPECTED: * Footer contains capitalized 'Show all' link
        """
        pass

    def test_008_click_on_show_all_link(self):
        """
        DESCRIPTION: Click on 'Show all' link
        EXPECTED: * Widget expands downwards to show full League Table
        EXPECTED: *  'Show all' changes to 'Show less'
        """
        pass

    def test_009_click_on_show_less_link(self):
        """
        DESCRIPTION: Click on 'Show less' link
        EXPECTED: * Widget collapses to show first 5 teams
        EXPECTED: *  'Show less' changes to 'Show all'
        """
        pass
