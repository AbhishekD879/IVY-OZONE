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
class Test_C722750_Verify_Badminton_Live_Score_of_BIP_events(Common):
    """
    TR_ID: C722750
    NAME: Verify Badminton Live Score of BIP events
    DESCRIPTION: This test case verifies Badminton Live Score of BIP events.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to 'Badminton' landing page -> 'In-Play' tab **DESKTOP** and Go to 'Badminton' landing page -> 'In-Play' module at the top of the page (if it's set in CMS and Live events are available) **MOBILE**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - In order to have a Scores Badminton event should be BIP
    PRECONDITIONS: - To verify new received data for 'In-Play' tab or page use Dev Tools-> Network -> Web Sockets -> wss://inplay-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket -> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXXXX"
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "BADMINTON"
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='PLAYER_1' / **role_code**='PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: - To verify new received data for 'In-Play' module use Dev Tools-> Network -> Web Sockets -> wss://featured-sports-prd0.coralsports.prod.cloud.ladbrokescoral.com/socket.io/?EIO=3&transport=websocket -> response with type: "FEATURED_STRUCTURE_CHANGED"
    PRECONDITIONS: Look at the attributes for InPlayModule:
    PRECONDITIONS: *   **categoryCode** = "BADMINTON"
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='PLAYER_1' / **role_code**='PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: - [How to generate Live Scores for Badminton][1]
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    """
    keep_browser_open = True

    def test_001_verify_badminton_event_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Badminton event with Game Scores available
        EXPECTED: Event is shown
        """
        pass

    def test_002_verify_game_score_displaying(self):
        """
        DESCRIPTION: Verify Game Score displaying
        EXPECTED: Game Score colored in grey for a particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_003_verify_game_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Game Score correctness for each player
        EXPECTED: * Game Score for Home team corresponds to **events.comments.team.player_1.score** attribute from WS response
        EXPECTED: * Game Score for Away team corresponds to **events.comments.team.player_2.score** attribute from WS response
        """
        pass

    def test_004_verify_points_score_displaying(self):
        """
        DESCRIPTION: Verify Points Score displaying
        EXPECTED: Points score colored in black for particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_005_verify_points_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Points Score correctness for each player
        EXPECTED: Points Score for each team corresponds to **events.comments.setScores.[i]**
        EXPECTED: where i - the highest value
        """
        pass

    def test_006_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: * Scores are not shown
        EXPECTED: * 'LIVE' label is shown
        """
        pass

    def test_007_verify_game_and_points_scores__for_outright_event(self):
        """
        DESCRIPTION: Verify Game and Points Scores  for Outright event
        EXPECTED: * Scores are not shown for Outright events
        EXPECTED: * 'LIVE' label is shown
        """
        pass

    def test_008_go_to_in_play_page___badminton_sorting_type_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Go to 'In Play' page -> 'Badminton' sorting type and repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_009_go_to_in_play_tab_on_module_selector_ribbon_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Go to 'In Play' tab on Module Selector Ribbon and repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_010_go_to_in_play_widget_and_repeat_steps_1_7_desktop(self):
        """
        DESCRIPTION: Go to 'In Play' widget and repeat steps 1-7 **DESKTOP**
        EXPECTED: 
        """
        pass

    def test_011_go_to_featured_tab_and_repeat_steps_1_7_mobile(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps 1-7 **MOBILE**
        EXPECTED: 
        """
        pass
