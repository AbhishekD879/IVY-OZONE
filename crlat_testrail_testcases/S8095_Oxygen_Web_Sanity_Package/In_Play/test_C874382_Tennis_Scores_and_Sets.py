import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C874382_Tennis_Scores_and_Sets(Common):
    """
    TR_ID: C874382
    NAME: Tennis Scores and Sets
    DESCRIPTION: This test case verifies the Tennis Live Score of BIP events.
    PRECONDITIONS: 1) In order to have Tennis Scores, the event should be BIP
    PRECONDITIONS: 2) To verify Tennis data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: *   **categoryCode** = "TENNIS"
    PRECONDITIONS: *   **runningSetIndex** : X,
    PRECONDITIONS: where X - number of current active set
    PRECONDITIONS: *   **setsScore -> X** : Y and Z,
    PRECONDITIONS: where X - number of current active set;
    PRECONDITIONS: Y - score for participate 1;
    PRECONDITIONS: Z - score for participate 2;
    PRECONDITIONS: *   **role_code**='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **score** - to see a Game score for particular participant
    PRECONDITIONS: ![](index.php?/attachments/get/5998192)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='GAME'and **periodIndex**='X' with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**='SET', **periodIndex**='X' - to look at the scorers for the specific Set (where 'X' - set number)
    PRECONDITIONS: *   **role_code**='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **value** - to see a Set score for particular participant
    PRECONDITIONS: ![](index.php?/attachments/get/5998209)
    PRECONDITIONS: 4) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: CLOCK
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='GAME'and **periodIndex**='X' with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: ![](index.php?/attachments/get/5998230)
    PRECONDITIONS: 5) [How to generate Live Scores for Tennis using Amelco][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: 6) [How to generate Live Scores for Tennis using TI][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 7) [How to configure Fallback Scoreboard in CMS][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True

    def test_001_load_the_application_and_navigate_to_in_play_page__tennis_tab(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Tennis' tab
        EXPECTED: 'Tennis' tab on the 'In-Play' page is opened
        """
        pass

    def test_002_verify_tennis_event_with_scores_available(self):
        """
        DESCRIPTION: Verify Tennis event with Scores available
        EXPECTED: Game Score, Set Score and Set Number are displayed
        """
        pass

    def test_003_verify_game_score_displaying(self):
        """
        DESCRIPTION: Verify Game Score displaying
        EXPECTED: *   Score for the home player is shown in front of home player name
        EXPECTED: *   Score for the away player is shown in front of away player name
        EXPECTED: *   Game score is displayed in grey (coral desktop)
        EXPECTED: *   Game score is displayed in black (coral mobile, ladbrokes mobile and desktop)
        """
        pass

    def test_004_verify_set_score_displaying(self):
        """
        DESCRIPTION: Verify Set Score displaying
        EXPECTED: *   Score for the home player is shown in front of home player name
        EXPECTED: *   Score for the away player is shown in front of away player name
        EXPECTED: *   Set score is displayed in grey (Coral desktop)
        EXPECTED: *   Set score is displayed in black (Coral mobile, ladbrokes mobile and desktop)
        EXPECTED: *   Set scores are displayed in columns for all finished sets
        """
        pass

    def test_005_verify_set_number(self):
        """
        DESCRIPTION: Verify Set Number
        EXPECTED: Number of Set is shown in format:** '<set>1st/2nd/3th Set'**
        """
        pass

    def test_006_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown
        """
        pass

    def test_007_repeat_steps_2_6_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        EXPECTED: 
        """
        pass

    def test_008_desktopnavigate_to_tennis_landing_page__matches_tab_and_verify_scoresset_number_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Tennis landing page > 'Matches' tab and verify scores/set number for 'In-play' widget
        EXPECTED: * 'LIVE'/'Set Number' is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        pass

    def test_009_desktopnavigate_to_tennis_landing_page__matches_tab_and_verify_scoresset_number_for_live_stream_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Tennis landing page > 'Matches' tab and verify scores/set number for 'Live Stream' widget
        EXPECTED: * 'LIVE'/'Set Number' red badge is displayed next to event class/type
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        """
        pass
