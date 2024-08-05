import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C59957114_Verify_receiving_live_updates_when_changing_the_event_from_pre_play_to_in_play_state(Common):
    """
    TR_ID: C59957114
    NAME: Verify receiving live updates when changing the event from pre-play to in play state
    DESCRIPTION: Test case verifies receiving live updates when changing the event from pre-play to in play state without refreshing page
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Create a Football event in OpenBet (TI)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets with selection template = Range and template = Binary created Football event (FE)
    PRECONDITIONS: * In OpenBet (TI) event should be in pre-play state (Is OFF = No)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: **NOTE**
    PRECONDITIONS: Selections with 'template = Binary' means that only 2 options are available. E.g. 'Both Team to score' -> Yes/No.
    PRECONDITIONS: Selections with template = Range' means that multiple-choice prediction is available. E.g. 'Christain Eriksen to Make 55+ Passes'
    """
    keep_browser_open = True

    def test_001_open_my_betsopen_bets_tab_open_bets_and_go_to_placed_build_your_bet_bet(self):
        """
        DESCRIPTION: Open My Bets/Open Bets tab (/open-bets) and go to placed **Build Your Bet** bet
        EXPECTED: * Opta disclaimer short text (My Bets Footer)is not displayed for FE (from precondition) next to Build Your Bet/5-a-side bets
        EXPECTED: * Left-hand status indicators for the bet's selections are NOT displayed
        EXPECTED: * Progress bars and stats descriptions for the bet's selections are NOT displayed
        """
        pass

    def test_002_open_devtools___network_and_filter_by_web_sockets_ws_verify_subscription_for_bet_tracker_updates_liveserve_ws(self):
        """
        DESCRIPTION: Open DevTools - Network and filter by Web Sockets (WS), verify subscription for Bet Tracker updates (liveserve WS)
        EXPECTED: * WS connection with Live Serv MS is created
        EXPECTED: * 42["scoreboard","eventID"] message is not present (eventID from TI)
        """
        pass

    def test_003_go_to_ti_and_change_the_event_from_pre_play_to_in_play_state_is_off__yessave_changes(self):
        """
        DESCRIPTION: Go to TI and change the event from pre-play to in play state (Is OFF = YES)
        DESCRIPTION: Save changes
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_004_go_back_to_the_app___my_betsopen_bets_tab_open_bets_without_refreshing_the_pageopen_eio3transportwebsocket_in_devtools_liveserve_ws(self):
        """
        DESCRIPTION: Go back to the app -> My Bets/Open Bets tab (/open-bets) without refreshing the page
        DESCRIPTION: Open EIO=3&transport=websocket in DevTools (liveserve WS)
        EXPECTED: * 42["scoreboard","eventID"] message appears in
        EXPECTED: ?EIO=3&transport=websocket (eventID from TI)
        EXPECTED: * Event is subscribed for Opta Live updates
        """
        pass

    def test_005_check_build_your_bet_bet_displaying(self):
        """
        DESCRIPTION: Check Build Your Bet bet displaying
        EXPECTED: * Left-hand status indicators (red 'up' and green 'down') are displayed next to selections automatically without page refresh for both **Range** and **Binary** template
        EXPECTED: * Progress bars is displayed in the starting position(0% progress) automatically without page refresh for **Range** template only
        EXPECTED: * Stats descriptions are displayed below progress bars automatically without page refresh in the default state(e.g. '0 of 2 Shots') for **Range** template only
        """
        pass

    def test_006_repeat_steps_1_5_for_my_betsopen_bets_widget_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-5 for My Bets/Open Bets widget for Desktop
        EXPECTED: 
        """
        pass

    def test_007_only_coral_repeat_steps_1_5_for_cash_out_tab_for_fe_from_precondition(self):
        """
        DESCRIPTION: [Only Coral] Repeat steps 1-5 for Cash out tab for FE (from precondition)
        EXPECTED: 
        """
        pass

    def test_008_only_coral_repeat_steps_1_5_for_my_bets_tab_in_edp_for_fe_from_precondition(self):
        """
        DESCRIPTION: [Only Coral] Repeat steps 1-5 for My Bets tab in EDP for FE (from precondition)
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_8_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1-8 for **5-a-side** bet
        EXPECTED: 
        """
        pass
