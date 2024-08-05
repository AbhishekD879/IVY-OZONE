import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C874346_Coral_Only_Football_Visualization__Perform(Common):
    """
    TR_ID: C874346
    NAME: Coral Only: Football Visualization - Perform
    DESCRIPTION: This test case verifies Football Visualization widget
    PRECONDITIONS: There are LIVE football events mapped with **Perform** events
    PRECONDITIONS: All information is taken from WebSockets:
    PRECONDITIONS: * info related to OpenBet event (className, typeName etc) comes in **generic** packet
    PRECONDITIONS: * info about Team Names and Stadium name comes in **details** packet
    PRECONDITIONS: * historic info about event comes in **history** packet
    PRECONDITIONS: * info about statistic comes in **statistics** packet
    PRECONDITIONS: * info about incidents comes in **incident** packets
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_mapped_with_perform_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of event mapped with Perform event
        EXPECTED: * Football widget is displayed
        EXPECTED: * Football widget consists of 1 slide: slide with Football Visualization only
        """
        pass

    def test_002_verify_content_of_slide_with_football_visualization(self):
        """
        DESCRIPTION: Verify content of slide with Football Visualization
        EXPECTED: Slide with Football Visualization consists of the following elements:
        EXPECTED: * Mini Scoreboard bar
        EXPECTED: * Goal Scorer name and Time for goal
        EXPECTED: * Line with Basic Event Information
        EXPECTED: * Pitch with the background
        EXPECTED: * Banner
        EXPECTED: * Team Shirts (if available)
        EXPECTED: * Statistic information
        """
        pass

    def test_003_verify_content_of_mini_scoreboard_bar(self):
        """
        DESCRIPTION: Verify content of Mini Scoreboard bar
        EXPECTED: Mini Scores bar contains data in the following order:
        EXPECTED: *   Home Team Name
        EXPECTED: *   Home Team Match Score
        EXPECTED: *   Match Clock
        EXPECTED: *   Period Name
        EXPECTED: *   Away Team Match Score
        EXPECTED: *   Away Team Name
        EXPECTED: Red Cards can be shown under Team Names (if available)
        """
        pass

    def test_004_verify_goal_scorer_name_and_time_for_goalif_available(self):
        """
        DESCRIPTION: Verify Goal Scorer name and Time for goal
        DESCRIPTION: (if available)
        EXPECTED: * Goal scorer name and time of goal is displayed beneath corresponding team name
        EXPECTED: * Goal scorer name and time is displayed in plain text (e.g. Suarez 71’)
        """
        pass

    def test_005_verify_basic_match_information_line_content_and_locationif_available(self):
        """
        DESCRIPTION: Verify Basic Match Information line content and location
        DESCRIPTION: (if available)
        EXPECTED: * Basic Match information line with country flag/trophy icon, league name and stadium name are displayed under Mini Scoreboard bar
        EXPECTED: * The content of the Basic Match information line is dynamically centered when some information is not available
        EXPECTED: * If League/Stadium names are too long then ellipsis (...) is used for cutting
        """
        pass

    def test_006_verify_teams_shirts_displayingif_available(self):
        """
        DESCRIPTION: Verify Teams Shirts displaying
        DESCRIPTION: (if available)
        EXPECTED: * Teams Shirts are displayed on the left (home team) and right side (away team) team) of the widget
        EXPECTED: * Teams Shirts are displayed below the Team Names
        EXPECTED: * Cross icons are displayed next to the shirts (if line ups are available)
        """
        pass

    def test_007_click_on_cross_iconif_available(self):
        """
        DESCRIPTION: Click on cross icon
        DESCRIPTION: (if available)
        EXPECTED: * Popup/overlay list of players (line up) is shown
        EXPECTED: * The Line up Popup/overlay will cover the whole widget area
        EXPECTED: * The list is divided into 3 parts: Main Players, Substitutions and Manager Name
        EXPECTED: * An arrow icon is available to close the popup/overlay
        """
        pass

    def test_008_click_on_arrow_icon(self):
        """
        DESCRIPTION: Click on arrow icon
        EXPECTED: Football widget is displayed
        """
        pass

    def test_009_verify_banners_displaying_on_the_background(self):
        """
        DESCRIPTION: Verify banners displaying on the background
        EXPECTED: * Set of turned on banners, which are uploaded to CMS, are showing: one at a time
        EXPECTED: * Every 5 minutes banner is changed to another with a fade in and fade out fluid motion
        EXPECTED: * Order of banners is the same as set in CMS
        """
        pass

    def test_010_verify_incidents_displayingif_available(self):
        """
        DESCRIPTION: Verify incidents displaying
        DESCRIPTION: (if available)
        EXPECTED: * Relevant info-box is shown below basic event information
        EXPECTED: * Relevant animation is shown on the pitch area
        """
        pass

    def test_011_verify_info_box_contentif_available(self):
        """
        DESCRIPTION: Verify info-box content
        DESCRIPTION: (if available)
        EXPECTED: * Relevant incident icon is displayed
        EXPECTED: * Relevant incident label is shown as a descriptive text
        EXPECTED: * Team Name/Player Name is shown under incident label (if available)
        """
        pass

    def test_012_verify_statistics_values_displaying(self):
        """
        DESCRIPTION: Verify statistics values displaying
        EXPECTED: * Statistics values are displayed at the bottom of football widget
        EXPECTED: * Each of the stats type are displayed with its own icon
        EXPECTED: * Each of the stats type have a values (numbers) on the team corresponding side
        EXPECTED: * Each of the stats has a name above the icon
        EXPECTED: * Statistic values are updated during live event
        """
        pass
