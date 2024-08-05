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
class Test_C722752_Verify_Badminton_Game_Score_changing_on_In_Play_page(Common):
    """
    TR_ID: C722752
    NAME: Verify Badminton Game Score changing on In Play page
    DESCRIPTION: This test case verifies Game Score changing on In-Play page
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

    def test_001_verify_badminton_event_with_score_available(self):
        """
        DESCRIPTION: Verify Badminton event with score available
        EXPECTED: Game Score colored in grey for a particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_002_change_game_score_for_home_team(self):
        """
        DESCRIPTION: Change Game Score for Home team
        EXPECTED: * Game Score immediately starts displaying new value for Home player
        EXPECTED: * Game Score corresponds to **value** attribute from WS where **role_code**='PLAYER_1' and **period_code**='ALL' on the highest **period_index**
        """
        pass

    def test_003_change_game_score_for_away_team(self):
        """
        DESCRIPTION: Change Game Score for Away team
        EXPECTED: * Game Score immediately starts displaying new value for Home player
        EXPECTED: * Game Score corresponds to **value** attribute from WS where **role_code**='PLAYER_2' and **period_code**='ALL' on the highest **period_index**
        """
        pass

    def test_004_verify_game_score_change_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Game Score change for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Score will be shown there
        """
        pass

    def test_005_verify_game_score_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Game Score change before application is opened
        EXPECTED: If application was not started/opened and Score was changed, after opening application and verified event - updated Score will be shown there
        """
        pass

    def test_006_verify_game_score_change_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify Game Score change when Details Page of verified event is opened
        EXPECTED: After tapping Back button updated Score will be shown on Landing page
        """
        pass

    def test_007_go_to_in_play_page_badminton_sorting_type_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'Badminton' sorting type and repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_008_go_to_in_play_tab_on_the_homepage_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Go to 'In Play' tab on the Homepage and repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_009_go_to_in_play_widget_and_repeat_steps_1_7_desktop(self):
        """
        DESCRIPTION: Go to 'In Play' widget and repeat steps 1-7 **DESKTOP**
        EXPECTED: 
        """
        pass

    def test_010_go_to_featured_tab_and_repeat_steps_1_7_mobile(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps 1-7 **MOBILE**
        EXPECTED: 
        """
        pass
