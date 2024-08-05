import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C62736563_Verify_ZMC_is_N_A_for_Single_and_Multiple_bets_placed_using_Free_Bets(Common):
    """
    TR_ID: C62736563
    NAME: Verify ZMC is N/A for Single and Multiple bets placed using Free Bets
    DESCRIPTION: This test case verifies Zero margin cash Out is Not applicable for full Cash Out and partial cash out for bets placed using Free Bets
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "NO" and "N/A" at event level in OB
    PRECONDITIONS: * Make sure no generic bet offers are running currently in OB
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_add_selection__from_this_event_cash_out_is_available_to_the_betslip_and_select_free_bet_from_free_bets_available_drop_down(self):
        """
        DESCRIPTION: Add selection  from this event (cash out is available) to the Betslip and select Free Bet from 'Free Bets Available' drop-down
        EXPECTED: Free bet offer is selected
        """
        pass

    def test_002_place_bet_using_selected_free_bet(self):
        """
        DESCRIPTION: Place Bet using selected Free Bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_navigate_to_cash_out_section_and_verify_placed_bet_displaying(self):
        """
        DESCRIPTION: Navigate to Cash out section and verify placed bet displaying
        EXPECTED: * Placed Bet should be displayed in Cash out section
        EXPECTED: * Cash out CTA is available for the Placed Bet and Partial Cash out CTA should not be available
        """
        pass

    def test_004_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: Cash Out value should be lower than the initial stake
        EXPECTED: Full margin should not be given to the users
        """
        pass

    def test_005_verify_the_network_call_in_ws(self):
        """
        DESCRIPTION: Verify the Network call in WS
        EXPECTED: Initial call in WS should not consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * is Off: "-" or "N"
        """
        pass

    def test_006_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with lower than the initial stake value should be displayed
        """
        pass

    def test_007_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: cash out should be successful
        """
        pass

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance should be increased with cash out value
        """
        pass
