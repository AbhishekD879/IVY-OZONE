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
class Test_C62736557_Verify_ZMC_is_applicable_for_Partial_Cash_Out_with_Multiple_bets_on_sports_Preplay_events(Common):
    """
    TR_ID: C62736557
    NAME: Verify ZMC is applicable for Partial Cash Out with Multiple bets on sports Preplay events
    DESCRIPTION: This test case verifies Zero margin cash Out is applicable for partial cash out with Multiple bets on Tier 1 and 2 sports of Preplay events when there are no price changes in Cash Out tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "NO" or "N/A" at event level in OB
    PRECONDITIONS: * Make sure no generic bet offers are running currently in OB
    PRECONDITIONS: Tier1 sports: Football, Basketball and Tennis
    PRECONDITIONS: Tier2 sports: American Football, Rugby Union, Rugby League,Cricket,Volleyball,Boxing,Golf,Darts,Snooker,Baseball,Ice Hockey etc..
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

    def test_006_click_on_partial_cash_out_button_on_cash_out_bar(self):
        """
        DESCRIPTION: Click on 'Partial Cash Out' button on Cash Out bar
        EXPECTED: 'Partial Cash Out' slider should be displayed
        """
        pass

    def test_007_make_sure_that_no_price_changes_are_triggered_on_above_placed_bet(self):
        """
        DESCRIPTION: Make sure that no price changes are triggered on above placed bet
        EXPECTED: Price changes should not happen on the above placed bet
        """
        pass

    def test_008_set_pointer_on_the_bar_to_any_value_not_to_maximum(self):
        """
        DESCRIPTION: Set pointer on the bar to any value (not to maximum)
        EXPECTED: Value on Cash Out button should be changed
        """
        pass

    def test_009_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with value selected in the pointer should be displayed
        """
        pass

    def test_010_tap_confirm_cash_out_cta(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' CTA
        EXPECTED: Spinner + Cashing Out label should be displayed
        """
        pass

    def test_011_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance should be increased with partial cash out amount
        """
        pass

    def test_012_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: Cash out value should be displayed as Initial stake amount - partial cash out amount
        EXPECTED: Note:
        EXPECTED: User should able to partially cash out the total initial stake amount
        """
        pass

    def test_013_verify_cash_out_call_in_network_tab(self):
        """
        DESCRIPTION: Verify cash out call in Network tab
        EXPECTED: cash out call should consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        """
        pass
