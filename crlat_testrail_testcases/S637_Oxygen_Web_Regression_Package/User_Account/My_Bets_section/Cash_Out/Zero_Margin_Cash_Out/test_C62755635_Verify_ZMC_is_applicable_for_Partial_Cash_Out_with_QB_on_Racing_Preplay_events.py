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
class Test_C62755635_Verify_ZMC_is_applicable_for_Partial_Cash_Out_with_QB_on_Racing_Preplay_events(Common):
    """
    TR_ID: C62755635
    NAME: Verify ZMC is applicable for Partial Cash Out with QB on Racing Preplay events
    DESCRIPTION: This test case verifies Zero margin cash Out is applicable for partial cash out with QB on Racing(Horse Racing and Grey Hounds) Preplay events when there are no price changes in Cash Out tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "NO" or "N/A" at event level in OB
    PRECONDITIONS: *  Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_add_a_selection_from_horse_racing_preplay_event_to_quick_bet_for_which_cash_out_is_available_sp_and_lp_prices(self):
        """
        DESCRIPTION: Add a selection from Horse Racing Preplay event to Quick Bet for which cash out is available (SP and LP prices)
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_002_add_stake_amount_and_click_on_place_bet(self):
        """
        DESCRIPTION: Add stake amount and click on "Place bet"
        EXPECTED: Quick Bet should be placed successfully
        """
        pass

    def test_003_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_004_go_to_single_cash_out_bet(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet
        EXPECTED: 
        """
        pass

    def test_005_click_on_partial_cash_out_button_on_cash_out_bar(self):
        """
        DESCRIPTION: Click on 'Partial Cash Out' button on Cash Out bar
        EXPECTED: 'Partial Cash Out' slider should be displayed
        """
        pass

    def test_006_make_sure_that_no_price_changes_are_triggered_on_above_placed_bet(self):
        """
        DESCRIPTION: Make sure that no price changes are triggered on above placed bet
        EXPECTED: Price changes should not happen on the above placed bet
        """
        pass

    def test_007_set_pointer_on_the_bar_to_any_value_not_to_maximum(self):
        """
        DESCRIPTION: Set pointer on the bar to any value (not to maximum)
        EXPECTED: Value on Cash Out button should be changed
        """
        pass

    def test_008_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with value selected in the pointer should be displayed
        """
        pass

    def test_009_tap_confirm_cash_out_cta(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' CTA
        EXPECTED: Spinner + Cashing Out label should be displayed
        """
        pass

    def test_010_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance should be increased with partial cash out amount
        """
        pass

    def test_011_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: Cash out value should be displayed as Initial stake amount - partial cash out amount
        EXPECTED: Note:
        EXPECTED: User should able to partially cash out the total initial stake amount
        """
        pass

    def test_012_verify_cash_out_call_in_network_tab(self):
        """
        DESCRIPTION: Verify cash out call in Network tab
        EXPECTED: Cash out call should consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        """
        pass

    def test_013_repeat_steps_1_12_for_grey_hounds_lp(self):
        """
        DESCRIPTION: Repeat steps 1-12 for Grey Hounds (LP)
        EXPECTED: 
        """
        pass
