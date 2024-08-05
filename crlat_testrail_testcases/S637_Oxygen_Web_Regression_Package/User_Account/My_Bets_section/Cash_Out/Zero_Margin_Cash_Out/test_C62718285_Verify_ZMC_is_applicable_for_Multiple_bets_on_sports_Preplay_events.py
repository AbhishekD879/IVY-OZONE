import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.cash_out
@vtest
class Test_C62718285_Verify_ZMC_is_applicable_for_Multiple_bets_on_sports_Preplay_events(Common):
    """
    TR_ID: C62718285
    NAME: Verify ZMC is applicable for Multiple bets on sports Preplay events
    DESCRIPTION: This test case verifies Zero margin cash Out is applicable for full cash out with Multiple bets on Tier 1 and 2 sports of Preplay events when there are no price changes in Cash Out tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "No" or "N/A" at event level in OB
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
        EXPECTED: Cash Out value should be displayed with Total stake amount
        EXPECTED: Note:
        EXPECTED: User places a bet with Stake as 1GBP then Cash Out value should be displayed as 1GBP
        """
        pass

    def test_008_verify_the_network_call_in_ws(self):
        """
        DESCRIPTION: Verify the Network call in WS
        EXPECTED: Initial call in WS should consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        EXPECTED: * is Off: "-" or "N"
        """
        pass

    def test_009_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with bet placed stake value should be displayed
        """
        pass

    def test_010_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner + Cashing Out label should be displayed
        """
        pass

    def test_011_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance should be increased on full cash out value
        """
        pass
