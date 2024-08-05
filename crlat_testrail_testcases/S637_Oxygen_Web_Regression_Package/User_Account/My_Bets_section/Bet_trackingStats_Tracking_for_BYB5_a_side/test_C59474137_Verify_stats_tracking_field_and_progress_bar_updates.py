import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C59474137_Verify_stats_tracking_field_and_progress_bar_updates(Common):
    """
    TR_ID: C59474137
    NAME: Verify stats tracking field and progress bar updates
    DESCRIPTION: This test case verifies stats tracking field and progress bar updates and animation
    PRECONDITIONS: * Make sure that Bet Tracking feature is enabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = true
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bet on selection with **template = Range** e.g. |BUILD YOUR BET| |PLAYER TOTAL ASSISTS|/|PLAYER TOTAL GOALS|
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Start recorded event (In TI set 'Іs Off' = yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Go to Open Bets page/tab -> event subscription for Opta updates should be made in Live Serv MS: 42["scoreboard","eventID"] and initial response must be received
    PRECONDITIONS: * To check Opta live updates open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: **NOTE** In order to have valid Opta statistic updates data across 3 provides (OpenBet, Banach, Opta) should be the same. Event, selections names should be the same on OpenBet TI, Banach, Opta endpoints. This is the ideal case and due to lack of data on TST2 env may be checked on PROD env.
    PRECONDITIONS: e.g. Event with name |Liverpool| |vs| |Arsenal| in OpenBet should have selections with: |Liverpool|,|Draw|,|Arsenal|. Banach and Opta statistic should be mapped to the event with the same info: Liverpool vs Arsenal.
    """
    keep_browser_open = True

    def test_001_trigger_opta_live_update_that_is_applicable_for_placed_build_your_bet_bet_and_check_status_bar_animationeg_team_a_scored_1st_goal_and_user_have_placed_bet_on_team_a_to_score_3plus_goals(self):
        """
        DESCRIPTION: Trigger Opta live update that is applicable for placed **Build Your Bet** bet and check status bar animation
        DESCRIPTION: e.g. Team-A scored 1st goal and user have placed bet on 'Team-A To Score 3+ Goals'
        EXPECTED: * Opta live update is received in WS (see preconditions)
        EXPECTED: * Stats tracking field is updated automatically
        EXPECTED: * Progress bar indicator increased with animation (see attached file for reference).
        EXPECTED: ![](index.php?/attachments/get/115421566)
        EXPECTED: e.g. '1 of 2 goals' text is displayed and progress bar filled from 0% to 50% with animation
        """
        pass

    def test_002_go_to_cash_out_tab_and_repeat_step_1_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' tab and repeat step #1 (Coral only)
        EXPECTED: 
        """
        pass

    def test_003_go_to_edp_of_placed_bet___openmy_bets_tab_and_repeat_step_1_coral_only(self):
        """
        DESCRIPTION: Go to EDP of placed bet -> open'My Bets' tab and repeat step #1 (Coral only)
        EXPECTED: 
        """
        pass

    def test_004_in_desktop_mode_open_my_bets_tab_on_edp_and_my_betscash_outsettled_bets_tab_on_betslip_widget_coral_only(self):
        """
        DESCRIPTION: In Desktop mode open 'My Bets' tab on EDP and 'My Bets'/'Cash Out'/'Settled Bets' tab on Betslip widget (Coral only)
        EXPECTED: 
        """
        pass

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step #1
        EXPECTED: * Opta live update is received in WS
        EXPECTED: * Stats tracking field is updated automatically on both 'My Bets' tab on EDP and 'My Bets'/'Cash Out'/'Settled Bets' tab
        EXPECTED: * Progress bar indicator increased with animation on both 'My Bets' tab on EDP and 'My Bets'/'Cash Out'/'Settled Bets' tab
        """
        pass

    def test_006_in_desktop_mode_open_my_betscash_outsettled_bets_on_main_screen_and_my_betscash_outsettled_bets_tab_on_betslip_widget(self):
        """
        DESCRIPTION: In Desktop mode open 'My Bets'/'Cash Out'/'Settled Bets' on main screen and 'My Bets'/'Cash Out'/'Settled Bets' tab on Betslip widget
        EXPECTED: 
        """
        pass

    def test_007_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step #1
        EXPECTED: * Opta live update is received in WS
        EXPECTED: * Stats tracking field is updated automatically on both 'My Bets'/'Cash Out'/'Settled Bets' on main screen and 'My Bets'/'Cash Out'/'Settled Bets' tab
        EXPECTED: * Progress bar indicator increased with animation on both 'My Bets'/'Cash Out'/'Settled Bets' on main screen and 'My Bets'/'Cash Out'/'Settled Bets' tab
        """
        pass

    def test_008_repeat_steps_1_7_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1-7 for **5-a-side** bet
        EXPECTED: 
        """
        pass
