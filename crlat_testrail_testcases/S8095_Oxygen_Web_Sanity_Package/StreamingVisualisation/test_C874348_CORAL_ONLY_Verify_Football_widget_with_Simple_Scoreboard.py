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
class Test_C874348_CORAL_ONLY_Verify_Football_widget_with_Simple_Scoreboard(Common):
    """
    TR_ID: C874348
    NAME: [CORAL ONLY] Verify Football widget with Simple Scoreboard
    DESCRIPTION: This test case verifies Football widget with Simple Scoreboard
    PRECONDITIONS: There are LIVE football events without mapped Perform events with OpenBet commentary feed
    PRECONDITIONS: NOTE:
    PRECONDITIONS: All information is taken from WebSockets:
    PRECONDITIONS: *      info related to OpenBet event information (eventName, className, typeName etc) comes in "generic" packet
    PRECONDITIONS: *      info related to OpenBet time, period name and scores (mtime, period, score) comes in "incident" or 'history' packet
    PRECONDITIONS: *      OpenBet does not send information about statistic
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_unmapped_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of unmapped event
        EXPECTED: Football widget with Simple Scoreboard is displayed
        """
        pass

    def test_002_verify_content_of_simple_scoreboard(self):
        """
        DESCRIPTION: Verify content of Simple Scoreboard
        EXPECTED: Simple Scoreboard contains the following elements:
        EXPECTED: *   Mini Scoreboard bar
        EXPECTED: *   Line with Basic Event Information
        EXPECTED: *   Message "Game in Progress"
        EXPECTED: *   Pitch with the background
        EXPECTED: *   Statistic information
        EXPECTED: ![](index.php?/attachments/get/59323462)
        """
        pass

    def test_003_verify_content_of_mini_scores_bar(self):
        """
        DESCRIPTION: Verify content of Mini Scores bar
        EXPECTED: Mini Scores bar contains data in the following order:
        EXPECTED: *   Home Team Name
        EXPECTED: *   Home Team Match Score
        EXPECTED: *   Match Clock
        EXPECTED: *   Period Name
        EXPECTED: *   Away Team Match Score
        EXPECTED: *   Away Team Name
        """
        pass

    def test_004_verify_content_of_basic_event_information(self):
        """
        DESCRIPTION: Verify content of Basic Event Information
        EXPECTED: Basic Event Information contains data in the following order:
        EXPECTED: *   Country Flag or Trophy icon
        EXPECTED: *   League name
        """
        pass

    def test_005_verify_static_message(self):
        """
        DESCRIPTION: Verify static message
        EXPECTED: Message "**Game in Progress**" is shown below Basic Event Information
        """
        pass

    def test_006_verify_pitch_part_of_the_widget(self):
        """
        DESCRIPTION: Verify Pitch part of the widget
        EXPECTED: Any info boxes and animations are NOT shown on or above the pitch during live matches
        """
        pass

    def test_007_verify_statistics_values_displaying(self):
        """
        DESCRIPTION: Verify statistics values displaying
        EXPECTED: *   Dashes are displayed for all statistic types at the bottom of football widget
        EXPECTED: *   Statistic values are not updated during live event
        """
        pass
