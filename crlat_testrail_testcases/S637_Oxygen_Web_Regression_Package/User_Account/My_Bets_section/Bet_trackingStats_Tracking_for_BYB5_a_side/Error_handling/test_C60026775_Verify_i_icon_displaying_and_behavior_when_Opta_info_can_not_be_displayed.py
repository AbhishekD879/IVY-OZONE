import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C60026775_Verify_i_icon_displaying_and_behavior_when_Opta_info_can_not_be_displayed(Common):
    """
    TR_ID: C60026775
    NAME: Verify 'i' icon displaying and behavior when Opta info can not be displayed
    DESCRIPTION: This test case verifies 'i' icon displaying and behavior when Opta info can not be displayed for BYB/5-a-side selection
    PRECONDITIONS: * Create a Football event in OpenBet (TI)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets
    PRECONDITIONS: * **Make sure that Opta info can not be displayed for placed selections** e.g. data mismatch, no data on Opta
    PRECONDITIONS: * In OpenBet (TI) event should be Live (Is OFF = Yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
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

    def test_002_go_build_your_bet_bet_where_opta_info_can_not_be_displayed_for_selection(self):
        """
        DESCRIPTION: Go **Build Your Bet** bet where Opta info can not be displayed for selection
        EXPECTED: * Pre-match view is displayed for selection
        EXPECTED: * 'i' icon is displayed next to the selection
        """
        pass

    def test_003_tapclick_on_the_i_icon(self):
        """
        DESCRIPTION: Tap/click on the 'i' icon
        EXPECTED: * Tooltip is displayed with the next text:
        EXPECTED: 'Stats Unavailable For This Selection'
        EXPECTED: ![](index.php?/attachments/get/121267186)
        EXPECTED: ![](index.php?/attachments/get/121267187)
        """
        pass

    def test_004_tapclick_away_tooltip(self):
        """
        DESCRIPTION: Tap/click away tooltip
        EXPECTED: * Tooltip is no more shown
        """
        pass

    def test_005_go_to_settled_bets_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'Settled Bets' page and repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_006_go_to_cash_out_pagetab_and_repeat_steps_2_4_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' page/tab and repeat steps #2-4 [Coral ONLY]
        EXPECTED: 
        """
        pass

    def test_007_go_to_my_bets_tab_on_football_edp_and_repeat_steps_2_4_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on Football EDP and repeat steps #2-4 [Coral ONLY]
        EXPECTED: 
        """
        pass

    def test_008_go_5_a_side_bet_where_opta_info_can_not_be_displayed_for_selection_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Go **5-a-side** bet where Opta info can not be displayed for selection and repeat steps #2-7
        EXPECTED: 
        """
        pass
