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
class Test_C874357_Navigation_Football_Leagues_Standings(Common):
    """
    TR_ID: C874357
    NAME: Navigation Football Leagues (Standings)
    DESCRIPTION: This test case verifies 'Leagues' page for Football sport
    DESCRIPTION: AUTOTEST [C49708352]
    PRECONDITIONS: [1] Link to check league table results: http://www.espnfc.com/english-league-championship/24/table
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
        EXPECTED: * List of available leagues is displayed
        EXPECTED: * First Competition (league) type is expanded, the rest are displayed collapsed
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
        EXPECTED: Standings tab is opened
        """
        pass

    def test_005_check_page(self):
        """
        DESCRIPTION: Check page
        EXPECTED: - A ribbon with available sport types is displayed (Premier League, Championship etc) for the last season
        EXPECTED: - Arrows to switch season for league is displayed
        EXPECTED: - Table with results and statistics is shown
        """
        pass

    def test_006_check_data_correctness_on_the_league_table_for_particular_seasoncompare_information_displayed_on_the_app_with_link_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: Check data correctness on the league table for particular season
        DESCRIPTION: Compare information displayed on the app with link mentioned in pre-conditions
        EXPECTED: The information is up to date
        """
        pass

    def test_007_for_desktopnavigate_to_football_landing_page___competitions_tab_and_select_any_competition_eg_premier_league(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab and select any Competition e.g. Premier League
        EXPECTED: * Competition Details page is opened
        EXPECTED: * League Table Widget is displayed in 3rd column or below main content area depending on screen resolution
        EXPECTED: * League Table Widget displays info about competition, user is viewing
        """
        pass

    def test_008_for_desktopverify_header_and_sub_header_of_league_table_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Verify header and sub-header of League Table Widget
        EXPECTED: Header contains:
        EXPECTED: - 'League table' label and up/down facing chevron
        EXPECTED: - League Table Widget can be collapsed/expanded
        EXPECTED: Sub-header contains:
        EXPECTED: - season name of competition user is viewing (e.g. Premier League 17/18)
        EXPECTED: - left/right arrows to switch between seasons (no arrows in case of 1 season)
        """
        pass

    def test_009_for_desktopverify_table_data_and_footer(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Verify table data and footer
        EXPECTED: League Table contains info about first 5 teams with the following columns:
        EXPECTED: - POS (position in table)
        EXPECTED: - Team name (Text truncates for long names)
        EXPECTED: - P (stands for 'Plays/Matches total')
        EXPECTED: - W (stands for 'Won total')
        EXPECTED: - D (stands for 'Draw total')
        EXPECTED: - L (stands for 'Lost total')
        EXPECTED: - GD (stands for 'Goal Difference total')
        EXPECTED: - PTS (stands for 'Points total')
        EXPECTED: Footer contains 'Show all' link that on click expands to shown the rest of data. 'Show all' link changes to 'Show less'
        """
        pass

    def test_010_for_desktopswitch_to_a_different_competition_using_change_competition_selector_in_header(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Switch to a different competition using 'Change competition' selector in header
        EXPECTED: * Selected competition Details page is opened
        EXPECTED: * League Table Widget displays data of selected competition
        """
        pass
