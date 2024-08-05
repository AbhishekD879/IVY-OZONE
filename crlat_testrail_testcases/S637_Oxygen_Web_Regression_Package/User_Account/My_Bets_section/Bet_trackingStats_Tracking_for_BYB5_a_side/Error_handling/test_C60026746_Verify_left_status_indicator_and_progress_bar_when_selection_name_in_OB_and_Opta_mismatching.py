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
class Test_C60026746_Verify_left_status_indicator_and_progress_bar_when_selection_name_in_OB_and_Opta_mismatching(Common):
    """
    TR_ID: C60026746
    NAME: Verify left status indicator and progress bar when selection name in OB and Opta mismatching
    DESCRIPTION: This test case verifies left status indicator and progress bar when selection name in OB and Opta mismatching
    PRECONDITIONS: * Create a Football event in OpenBet (TI)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets with selection template = Range and template = Binary
    PRECONDITIONS: * **Make sure that Opta info for selection and selection name in OB are mismatching**
    PRECONDITIONS: * In OpenBet (TI) event should be Live (Is OFF = Yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: **NOTE**
    PRECONDITIONS: Selections with 'template = Binary' means that only 2 options are available. E.g. 'Both Team to score' -> Yes/No.
    PRECONDITIONS: Selections with template = Range' means that multiple-choice prediction is available. E.g. 'Christain Eriksen to Make 55+ Passes'
    """
    keep_browser_open = True

    def test_001_go_to_open_bets_tabpage(self):
        """
        DESCRIPTION: Go to 'Open bets' tab/page
        EXPECTED: * Build Your Bet bet is present on 'Open bets' tab/page with selections with Binary and Range templates
        EXPECTED: * WS connection with Live Serv MS is created
        EXPECTED: * 42["scoreboard","eventID"] request is sent to subscribe for Opta updates
        EXPECTED: * Initial data structure response is received
        """
        pass

    def test_002_go_build_your_bet_bet_with_template__binary_where_selection_with_opta_info_mismatches_with_ob_selection_name(self):
        """
        DESCRIPTION: Go **Build Your Bet** bet with **template = Binary** where selection with Opta info mismatches with OB selection name
        EXPECTED: * Left-hand status indicator is not displayed next to the selection name
        EXPECTED: * Default pre-match view is applied for selection
        EXPECTED: * 'i' icon is displayed next to the selection name
        EXPECTED: * Opta info is present in WS initial response, but it mismatches with OB selection name
        EXPECTED: e.g. selection name received from Opta differs from the selection name from Openbet
        """
        pass

    def test_003_go_build_your_bet_bet_with_template__range_where_selection_with_opta_info_mismatches_with_ob_selection_name(self):
        """
        DESCRIPTION: Go **Build Your Bet** bet with **template = Range** where selection with Opta info mismatches with OB selection name
        EXPECTED: * Left-hand status indicator is not displayed next to the selection name
        EXPECTED: * Progress bar and stats tracking fields are missing below the selection name
        EXPECTED: * Default pre-match view is applied for selection
        EXPECTED: * 'i' icon is displayed next to the selection name
        EXPECTED: * Opta info is present in WS initial response, but it mismatches with OB selection name
        """
        pass

    def test_004_repeat_steps_13_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1,3 for **5-a-side** bet
        EXPECTED: 
        """
        pass

    def test_005_go_to_cash_out_pagetab_and_repeat_steps_2_4_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' page/tab and repeat steps #2-4 [Coral ONLY]
        EXPECTED: 
        """
        pass

    def test_006_go_to_my_bets_tab_on_football_edp_and_repeat_steps_2_4_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on Football EDP and repeat steps #2-4 [Coral ONLY]
        EXPECTED: 
        """
        pass
