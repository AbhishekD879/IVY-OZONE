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
class Test_C59997797_Verify_Winning_Lossing_updates_for_Left_hand_indicators(Common):
    """
    TR_ID: C59997797
    NAME: Verify Winning/Lossing updates for Left-hand indicators
    DESCRIPTION: This test case verifies Bet Tracker info when event has finished
    PRECONDITIONS: * Create a Football event in OpenBet (TI)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets with selection template = Range and template = Binary
    PRECONDITIONS: * In OpenBet (TI) event should be in pre-play state (Is OFF = No)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: **NOTE**
    PRECONDITIONS: Selections with 'template = Binary' means that only 2 options are available. E.g. 'Both Team to score' -> Yes/No.
    PRECONDITIONS: Selections with template = Range' means that multiple-choice prediction is available. E.g. 'Christain Eriksen to Make 55+ Passes'
    PRECONDITIONS: In order to have valid Opta statistic updates data across 3 provides (OpenBet, Banach, Opta) should be the same. Event, selections names should be the same on OpenBet TI, Banach, Opta endpoints. This is the ideal case and due to lack of data on TST2 env may be checked on PROD env.
    PRECONDITIONS: e.g. Event with name |Liverpool| |vs| |Arsenal| in OpenBet should have selections with: |Liverpool|,|Draw|,|Arsenal|. Banach and Opta statistic should be mapped to the event with the same info: Liverpool vs Arsenal.
    """
    keep_browser_open = True

    def test_001_go_to_open_bets_tabpage_and_find_build_your_bet_bet(self):
        """
        DESCRIPTION: Go to 'Open bets' tab/page and find **Build Your Bet** bet
        EXPECTED: * Build Your Bet bet is present on 'Open bets' tab/page with selections with Binary and Range templates
        EXPECTED: * WS connection with Live Serv MS is created
        EXPECTED: * 42["scoreboard","eventID"] request is sent to subscribe for Opta updates
        EXPECTED: * Initial data structure response is received
        """
        pass

    def test_002_trigger_winning_for_one_of_selection_with_template__range(self):
        """
        DESCRIPTION: Trigger winning for one of selection with template = Range
        EXPECTED: * Opta update is received in WS
        EXPECTED: * Green arrow showing up appears next to Range selection automatically without page refresh
        EXPECTED: ![](index.php?/attachments/get/120826051)
        """
        pass

    def test_003_trigger_winning_for_one_of_selection_with_template__binary(self):
        """
        DESCRIPTION: Trigger winning for one of selection with template = Binary
        EXPECTED: Results are the same as on step #2
        """
        pass

    def test_004_trigger_losing_for_one_of_selection_with_template__range(self):
        """
        DESCRIPTION: Trigger losing for one of selection with template = Range
        EXPECTED: * Opta update is received in WS
        EXPECTED: * Red arrow showing down appears next to Range selection automatically without page refresh
        EXPECTED: ![](index.php?/attachments/get/120826052)
        """
        pass

    def test_005_trigger_losing_for_one_of_selection_with_template__binary(self):
        """
        DESCRIPTION: Trigger losing for one of selection with template = Binary
        EXPECTED: Results are the same as on step #4
        """
        pass

    def test_006_go_to_cash_out_pagetab_and_repeat_steps_2_5_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' page/tab and repeat steps #2-5 (Coral only)
        EXPECTED: 
        """
        pass

    def test_007_go_to_my_bets_tab_on_football_edp_and_repeat_steps_2_5_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on Football EDP and repeat steps #2-5 (Coral only)
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_7_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1-7 for **5-a-side** bet
        EXPECTED: 
        """
        pass
