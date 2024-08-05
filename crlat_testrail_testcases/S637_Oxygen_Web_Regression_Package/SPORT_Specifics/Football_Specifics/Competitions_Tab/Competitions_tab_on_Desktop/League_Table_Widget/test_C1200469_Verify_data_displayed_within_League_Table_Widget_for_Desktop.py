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
class Test_C1200469_Verify_data_displayed_within_League_Table_Widget_for_Desktop(Common):
    """
    TR_ID: C1200469
    NAME: Verify data displayed within League Table Widget for Desktop
    DESCRIPTION: This test case verifies data displayed within League Table Widget for Desktop
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
    PRECONDITIONS: Values in the League Table correspond to the following:
    PRECONDITIONS: P = "matchesTotal"
    PRECONDITIONS: W = "winTotal"
    PRECONDITIONS: D = "drawTotal"
    PRECONDITIONS: L = "lossTotal"
    PRECONDITIONS: GD = "goalDiffTotal"
    PRECONDITIONS: PTS = "pointsTotal"
    PRECONDITIONS: ![](index.php?/attachments/get/114765842)
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

    def test_004_verify_that_correct_competition_is_displayed_in_widget(self):
        """
        DESCRIPTION: Verify that correct competition is displayed in widget
        EXPECTED: Only data for competition, user is viewing, is displayed in widget
        EXPECTED: Use requests from preconditions for verification
        """
        pass

    def test_005_verify_a_list_of_seasons_for_viewed_competition(self):
        """
        DESCRIPTION: Verify a list of seasons for viewed competition
        EXPECTED: Request to verify a list of seasons with their IDs for selected competition:
        EXPECTED: **{domain}/seasons/1/XX/YY**,
        EXPECTED: where
        EXPECTED: * 1 - Spark category id for Football
        EXPECTED: * XX - Spark country id
        EXPECTED: * YY - Spark competitions id
        """
        pass

    def test_006_verify_the_season_which_is_displayed_by_default(self):
        """
        DESCRIPTION: Verify the season which is displayed by default
        EXPECTED: All seasons are ordered by **startDate** attribute, following the rule: "The most recent season is opened by default"
        EXPECTED: Use **{domain}/api/seasons/1/XX/YY**  to see **startDate** attribute
        """
        pass

    def test_007_verify_correct_results_are_shown_for_selected_season(self):
        """
        DESCRIPTION: Verify correct results are shown for selected season
        EXPECTED: Info is taken from the following request:
        EXPECTED: **{domain}/resultstables/1/XX/YY/ZZZZZ**,
        EXPECTED: where
        EXPECTED: * 1 - Spark category id for Football
        EXPECTED: * XX - Spark country id
        EXPECTED: * YY - Spark competitions id
        EXPECTED: * ZZZZZ - Spark season id
        """
        pass

    def test_008_switch_between_seasons(self):
        """
        DESCRIPTION: Switch between seasons
        EXPECTED: * Call for another season is made
        EXPECTED: * Call for respective season results is made
        EXPECTED: * Corresponding information is displayed
        """
        pass

    def test_009_switch_to_another_competition_using_change_competition_selector(self):
        """
        DESCRIPTION: Switch to another competition using 'Change Competition' selector
        EXPECTED: * Selected competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * League Table Widget is displayed in 3rd column
        """
        pass

    def test_010_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps 4-8
        EXPECTED: 
        """
        pass
