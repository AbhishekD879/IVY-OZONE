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
class Test_C1406190_Verify_tabs_displaying_if_divisions_or_groups_are_available_for_League_on_League_Table_widget(Common):
    """
    TR_ID: C1406190
    NAME: Verify tabs displaying if divisions or groups are available for League on 'League Table' widget
    DESCRIPTION: This test case verifies tabs displaying if divisions or groups are available for League on 'League Table' widget
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

    def test_002_navigate_to_football_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        pass

    def test_003_expand_classes_accordion_and_select_group_stage_league_ie_the_international_class_euro_cup_league_or_league_with_separate_division_ie_usa_class_major_league_soccer_type(self):
        """
        DESCRIPTION: Expand Classes accordion and select Group Stage League (ie. the 'International' class, 'Euro Cup' league) or League with Separate Division (ie. 'USA' class, 'Major League Soccer' type)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * League Table Widget is displayed in 3rd column
        """
        pass

    def test_004_verify_displaying_of_groupdivision_tabs(self):
        """
        DESCRIPTION: Verify displaying of 'Group'/'Division' tabs
        EXPECTED: * 'Group'/'Division' tabs are displayed below Sub Header with the league name
        EXPECTED: * The first one is selected by default and highlighted
        EXPECTED: * The name of tabs corresponds to value in 'tableName' attribute received in response to the particular season
        EXPECTED: * Data received from the response to the particular season is displayed below the selected 'Group'/'Division' tab
        """
        pass

    def test_005_hover_the_mouse_over_the_groupdivision_tabs(self):
        """
        DESCRIPTION: Hover the mouse over the 'Group'/'Division' tabs
        EXPECTED: * Navigation arrows do NOT appear in case all tabs are visible fully
        EXPECTED: * Navigation arrows appear in case NOT all tabs are visible fully
        """
        pass

    def test_006_click_on_navigation_arrows_to_rich_the_groupdivision_tab_that_is_not_visible_fully_or_not_visible_at_all(self):
        """
        DESCRIPTION: Click on Navigation arrows to rich the 'Group'/'Division' tab that is not visible fully or not visible at all
        EXPECTED: Content scrolls horizontally in the left or right directions
        """
        pass

    def test_007_click_on_some_groupdivision_tab(self):
        """
        DESCRIPTION: Click on some 'Group'/'Division' tab
        EXPECTED: * 'Group'/'Division' tab is clickable
        EXPECTED: * Selected 'Group'/'Division' tab is highlighted
        EXPECTED: * Data received from the response to the particular season is displayed below the selected 'Group'/'Division' tab
        """
        pass

    def test_008_click_on_groupdivision_tab_that_not_contains_any_data(self):
        """
        DESCRIPTION: Click on 'Group'/'Division' tab that not contains any data
        EXPECTED: * 'Group'/'Division' tab is clickable
        EXPECTED: * Selected 'Group'/'Division' tab is highlighted
        EXPECTED: * 'Data not found' received in the response to the particular 'Group'/'Division'
        EXPECTED: * 'No events found' message is displayed below the selected 'Group'/'Division' tab
        """
        pass
