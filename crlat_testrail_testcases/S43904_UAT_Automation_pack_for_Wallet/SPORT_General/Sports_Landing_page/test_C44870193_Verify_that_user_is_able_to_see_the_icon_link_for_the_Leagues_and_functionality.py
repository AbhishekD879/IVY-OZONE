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
class Test_C44870193_Verify_that_user_is_able_to_see_the_icon_link_for_the_Leagues_and_functionality(Common):
    """
    TR_ID: C44870193
    NAME: Verify that user is able to see the icon/link for the 'Leagues' and functionality.
    DESCRIPTION: "Verify that user is able to see the icon/link for the 'Leagues' and functionality,
    DESCRIPTION: - Verify navigation of the league link goes to 'Leagues' page
    DESCRIPTION: -Verify for the Standings tab/Leauge Tables"
    PRECONDITIONS: "Site is loaded,
    PRECONDITIONS: There are inPlay/Upcoming events under Football League competitions"
    """
    keep_browser_open = True

    def test_001_tap_football_icon_from_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football 'icon from sports menu ribbon
        EXPECTED: Football sport page is opened
        """
        pass

    def test_002_tap_competitions_tab_on_the_sport_page(self):
        """
        DESCRIPTION: Tap 'Competitions' Tab on the sport page
        EXPECTED: List of available leagues is displayed
        EXPECTED: First Competition (league) type is expanded, the rest are displayed collapsed
        """
        pass

    def test_003_select_any_competition(self):
        """
        DESCRIPTION: Select any Competition
        EXPECTED: Competition page is opened with tabs available (some may be missing): matches, outrights, results,standings
        EXPECTED: List of events is displayed within selected Competition (League) in Matches tab
        """
        pass

    def test_004_open_standings_tab(self):
        """
        DESCRIPTION: Open Standings tab
        EXPECTED: League Table with results is opened
        """
        pass

    def test_005_check_data_correctness_on_the_league_table_for_particular_season(self):
        """
        DESCRIPTION: Check data correctness on the league table for particular season
        EXPECTED: The information is up to date
        """
        pass

    def test_006_verify_table_data_and_footer(self):
        """
        DESCRIPTION: Verify table data and footer
        EXPECTED: League Table contains info about first 5 teams with the following columns:
        EXPECTED: POS (position in table)
        EXPECTED: Team name (Text truncates for long names)
        EXPECTED: P (stands for 'Plays/Matches total')
        EXPECTED: W (stands for 'Won total')
        EXPECTED: D (stands for 'Draw total')
        EXPECTED: L (stands for 'Lost total')
        EXPECTED: GD (stands for 'Goal Difference total')
        EXPECTED: PTS (stands for 'Points total')
        EXPECTED: Footer contains 'Show all' link that on click expands to shown the rest of data. 'Show all' link changes to 'Show less'
        """
        pass

    def test_007_switch_to_a_different_competition_using_change_competition_selector_in_header(self):
        """
        DESCRIPTION: Switch to a different competition using 'Change competition' selector in header
        EXPECTED: Selected competition Details page is opened
        EXPECTED: League Table Widget displays data of selected competition
        """
        pass
