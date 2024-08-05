import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C874386_Volleyball_Beach_Volleyball_Scores(Common):
    """
    TR_ID: C874386
    NAME: Volleyball/Beach Volleyball Scores
    DESCRIPTION: This test case verifies Volleyball/Beach Volleyball Live Score of BIP events
    PRECONDITIONS: 1) In order to have a Scores Volleyball/Beach Volleyball event should be BIP
    PRECONDITIONS: 2) To verify Volleyball/Beach Volleyball data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "VOLLEYBALL"
    PRECONDITIONS: *   **teams** - home or away
    PRECONDITIONS: *   **name** - team name
    PRECONDITIONS: *   **score** - total score for team
    PRECONDITIONS: *   **currentPoints** - points in current set for team
    PRECONDITIONS: ![](index.php?/attachments/get/5692995)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code** ='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: ![](index.php?/attachments/get/5700213)
    PRECONDITIONS: 4) [How to generate Live Scores for Volleyball using Bet Genius][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    PRECONDITIONS: [Bet Genius credentials][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 5) [How to generate Live Scores for Volleyball/Beach Volleyball using TI][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 6) [How to configure Fallback Scoreboard in CMS][4]
    PRECONDITIONS: [4]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True

    def test_001_load_the_application_and_navigate_to_in_play_page__volleyballbeach_volleyball_tab(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Volleyball'/'Beach Volleyball' tab
        EXPECTED: 'Volleyball'/'Beach Volleyball' tab on the 'In-Play' page is opened
        """
        pass

    def test_002_verify_volleyball_event_with_scores_available(self):
        """
        DESCRIPTION: Verify 'Volleyball' event with scores available
        EXPECTED: * Total score (Sets) and PointsInCurrentSet for particular team are shown vertically at the same row as team's name near the Price/Odds button
        EXPECTED: * Score for the home player is shown in front of home player name
        EXPECTED: * Score for the away player is shown in front of away player name
        EXPECTED: * PointsInCurrentSet for the home player is shown on the first row
        EXPECTED: * PointsInCurrentSet for the away player is shown on the second row
        EXPECTED: * 'Live' label is displayed
        EXPECTED: * 'Watch Live' icon is displayed if live stream is available
        """
        pass

    def test_003_verify_volleyball_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify Volleyball event which doesn't have LIVE Score available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * Total score (Sets) and PointsInCurrentSet are NOT displayed
        """
        pass

    def test_004_repeat_steps_2_3_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 2-3 for:
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

    def test_005_desktopnavigate_to_volleyball_landing_page__matches_tab_and_verify_scoresset_number_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Volleyball landing page > 'Matches' tab and verify scores/set number for 'In-play' widget
        EXPECTED: * 'LIVE' badge is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        pass

    def test_006_desktopnavigate_to_volleyball_landing_page__matches_tab_and_verify_scoresset_number_for_live_stream_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Volleyball landing page > 'Matches' tab and verify scores/set number for 'Live Stream' widget
        EXPECTED: * 'LIVE' badge is displayed next to event class/type
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        """
        pass
