import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1474623_Verify_Badminton_Points_Score_changing_in_My_Bets_section(Common):
    """
    TR_ID: C1474623
    NAME: Verify Badminton Points Score changing in My Bets section
    DESCRIPTION: This test case verifies Badminton Points Score changing on 'Cash Out', 'Open Bets' and 'Bet History' pages
    PRECONDITIONS: 1. User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: 2. User should have placed bets on a Badminton live event with scores available
    PRECONDITIONS: 3. In order to have Scores, Badminton event should be in-play
    PRECONDITIONS: 4. To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::::LIVE_EVENT"
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "BADMINTON"
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='PLAYER_1' / **role_code**='PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: 5. [How to generate Live Scores for Badminton][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: * Cash out page is opened
        EXPECTED: * User's cash out bets are shown
        """
        pass

    def test_002_verify_badminton_bet_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Badminton bet with Game scores available
        EXPECTED: * The bet is shown in the cash out section
        EXPECTED: * Scores are shown on the bet card
        """
        pass

    def test_003_change_points_score_for_home_team(self):
        """
        DESCRIPTION: Change Points Score for Home team
        EXPECTED: * Points Score immediately starts displaying new value for Home player
        EXPECTED: * Point Score corresponds to **value** attribute from WS where **role_code**='PLAYER_1' and **period_code**='SET' on the highest **period_index**
        """
        pass

    def test_004_change_points_score_for_away_team(self):
        """
        DESCRIPTION: Change Points Score for Away team
        EXPECTED: * Points Score immediately starts displaying new value for Away player
        EXPECTED: * Point Score corresponds to **value** attribute from WS where **role_code**='PLAYER_2' and **period_code**='SET' on the highest **period_index**
        """
        pass

    def test_005_verify_points_score_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Points Score change before application is opened
        EXPECTED: If application was not started/opened and Score was changed, after opening application and cash out page with verified bet - updated Points Score will be shown there
        """
        pass

    def test_006_for_multiples_repeat_steps_2_5(self):
        """
        DESCRIPTION: For multiples repeat steps 2-5
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_6_for_cash_out_tab_my_bets_tab_bet_history_tab(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'My Bets' tab
        DESCRIPTION: * 'Bet History' tab
        EXPECTED: 
        """
        pass
