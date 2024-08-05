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
class Test_C62746244_Verify_ZMC_is_applicable_for_QB_on_Racing_Preplay_events__SPLP(Common):
    """
    TR_ID: C62746244
    NAME: Verify ZMC is applicable for QB on Racing Preplay events - SP,LP
    DESCRIPTION: This test case verifies Zero margin cash Out is applicable for full cash out with QB on Racing(Horse Racing and Grey Hounds) with prices SP and LP of Preplay events when there are no price changes in Cash Out tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "NO" or "N/A" at event level in OB
    PRECONDITIONS: * Make sure no generic bet offers are running currently in OB
    PRECONDITIONS: * Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_add_a_selection_from_hr_preplay_event_sp_to_quick_bet_for_which_cash_out_is_available(self):
        """
        DESCRIPTION: Add a selection from HR Preplay event (SP) to Quick Bet for which cash out is available
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

    def test_005_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: Cash Out value should be displayed with Total stake amount
        EXPECTED: Note:
        EXPECTED: User places a bet with Stake as 1GBP then Cash Out value should be displayed as 1GBP
        """
        pass

    def test_006_verify_the_network_call_in_ws(self):
        """
        DESCRIPTION: Verify the Network call in WS
        EXPECTED: Initial call in WS should consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        EXPECTED: * is Off: "-" or "N"
        """
        pass

    def test_007_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with bet placed stake value should be displayed
        """
        pass

    def test_008_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner + Cashing Out label should be displayed
        """
        pass

    def test_009_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance should be increased on full cash out value
        """
        pass

    def test_010_repeat_steps_1_9_for_hr_preplay_event_with_price_as_lp(self):
        """
        DESCRIPTION: Repeat steps 1-9 for HR Preplay event with price as LP
        EXPECTED: 
        """
        pass

    def test_011_repeat_1_11_for_greyhoundslp(self):
        """
        DESCRIPTION: Repeat 1-11 for Greyhounds(LP)
        EXPECTED: 
        """
        pass
