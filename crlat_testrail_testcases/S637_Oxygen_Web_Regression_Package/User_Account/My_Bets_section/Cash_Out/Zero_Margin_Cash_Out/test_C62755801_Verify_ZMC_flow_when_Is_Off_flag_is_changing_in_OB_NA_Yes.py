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
class Test_C62755801_Verify_ZMC_flow_when_Is_Off_flag_is_changing_in_OB_NA_Yes(Common):
    """
    TR_ID: C62755801
    NAME: Verify ZMC flow when 'Is Off' flag is changing in OB (-,NA, Yes)
    DESCRIPTION: This test case verifies Zero margin cash Out flow when 'Is Off' flag is changing between -,NA and Yes in OB
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "NO", "N/A" and "Yes" at event level in OB
    PRECONDITIONS: * Make sure no generic bet offers are running currently in OB
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    PRECONDITIONS: Example: TENNIS: |U.S.Open Men's Singles Outright|: Is off field Changes between all 3 options(-, NA, Yes) multiple times
    """
    keep_browser_open = True

    def test_001_add_a_selection_from_preplay_event_to_quick_betbetslip_for_which_cash_out_is_available(self):
        """
        DESCRIPTION: Add a selection from Preplay event to Quick Bet/Betslip for which cash out is available
        EXPECTED: Selections should be added successfully to Betslip/Quick Bet
        """
        pass

    def test_002_change_is_off_field_to_na_in_ob(self):
        """
        DESCRIPTION: Change 'Is Off' field to 'N/A' in OB
        EXPECTED: 'Is Off' field should be displayed as 'N/A'
        """
        pass

    def test_003_add_stake_amount_and_click_on_place_bet_in_fe(self):
        """
        DESCRIPTION: Add stake amount and click on "Place bet" in FE
        EXPECTED: Bet should be placed successfully
        """
        pass

    def test_004_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_005_go_to_single_cash_out_bet(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet
        EXPECTED: 
        """
        pass

    def test_006_make_sure_that_no_price_changes_are_triggered_on_above_placed_bet(self):
        """
        DESCRIPTION: Make sure that no price changes are triggered on above placed bet
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
        EXPECTED: * is Off: "-"
        """
        pass

    def test_009_click_on_cash_out(self):
        """
        DESCRIPTION: Click on Cash Out
        EXPECTED: Cash Out should be successful
        """
        pass

    def test_010_repeat_steps_1_7_by_changing_is_off_field_to_no_in_ob(self):
        """
        DESCRIPTION: Repeat steps 1-7 by changing 'Is Off' field to 'No' in OB
        EXPECTED: 
        """
        pass

    def test_011_verify_the_network_call_in_ws(self):
        """
        DESCRIPTION: Verify the Network call in WS
        EXPECTED: Initial call in WS should consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        EXPECTED: * is Off: "N"
        """
        pass

    def test_012_change_is_off_field_to_yes_in_ob(self):
        """
        DESCRIPTION: Change 'Is Off' field to 'Yes' in OB
        EXPECTED: 'Is Off' field should be displayed as 'Yes'
        """
        pass

    def test_013_verify_the_cash_out_value_and_network_call(self):
        """
        DESCRIPTION: Verify the Cash Out value and network call
        EXPECTED: * Cash out value should be lower than the stake amount
        EXPECTED: * cash out Profile: "NO_LOSS" should not be displayed in WS
        """
        pass

    def test_014_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: Cash Out value should not be displayed with Total stake amount
        EXPECTED: Note:
        EXPECTED: User places a bet with Stake as 1GBP then Cash Out value should be less than 1GBP
        """
        pass
