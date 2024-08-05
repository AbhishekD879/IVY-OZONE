import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C62736562_Verify_ZMC_is_N_A_for_Single_and_Multiple_bets_on_sports_Inplay_events(Common):
    """
    TR_ID: C62736562
    NAME: Verify ZMC is N/A  for Single and  Multiple bets on sports Inplay events
    DESCRIPTION: This test case verifies Zero margin cash Out is Not applicable for full cash out with Single and Multiple bets on Tier1 and Tier2 sports of Inplay events when there are no price changes in Cash Out tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "yes" at event level in OB
    PRECONDITIONS: * Make sure no generic bet offers are running currently in OB
    PRECONDITIONS: Tier1 sports: Football, Basketball and Tennis
    PRECONDITIONS: Tier2 sports: American Football, Rugby Union, Rugby League,Cricket,Volleyball,Boxing,Golf,Darts,Snooker,Baseball,Ice Hockey etc..
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_add_several_selections_from_different_events_to_the_betslip_for_which_cash_out_is_available(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip for which cash out is available
        EXPECTED: 
        """
        pass

    def test_002_open_betslip_gtmultiples_section(self):
        """
        DESCRIPTION: Open Betslip-&gt;'Multiples' section
        EXPECTED: Multiples section should be displayed
        """
        pass

    def test_003_enter_stake_for_one_of_available_multiples_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter Stake for one of available Multiples and click on "Place bet"
        EXPECTED: Multiple Bet should be placed successfully (the one which had entered Stake, the rest Multiples are ignored)
        """
        pass

    def test_004_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_005_go_to_multiple_cash_out_bet(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet
        EXPECTED: 
        """
        pass

    def test_006_make_sure_that_no_price_changes_are_trigged_on_above_placed_bet(self):
        """
        DESCRIPTION: Make sure that no price changes are trigged on above placed bet
        EXPECTED: Price changes should not happen on the above placed bet
        """
        pass

    def test_007_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: * Cash Out value should be lower than the initial stake
        EXPECTED: * Based on the ladders margin of the stake should be deducted from the stake value
        """
        pass

    def test_008_verify_the_network_call_in_ws(self):
        """
        DESCRIPTION: Verify the Network call in WS
        EXPECTED: Initial call in WS should not consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        EXPECTED: * is Off: "-" or "N"
        """
        pass

    def test_009_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with lower than the initial stake value should be displayed
        """
        pass

    def test_010_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner + Count down timer should be displayed
        """
        pass

    def test_011_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance should be increased with cash out value
        """
        pass

    def test_012_place_single_bet_and_navigate_to_cash_out_tabpagerepeat_steps_6_11(self):
        """
        DESCRIPTION: Place Single bet and navigate to Cash Out Tab/Page
        DESCRIPTION: Repeat steps 6-11
        EXPECTED: 
        """
        pass
