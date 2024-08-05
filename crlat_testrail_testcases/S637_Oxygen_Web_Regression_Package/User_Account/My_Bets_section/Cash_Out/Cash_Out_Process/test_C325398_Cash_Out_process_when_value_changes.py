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
class Test_C325398_Cash_Out_process_when_value_changes(Common):
    """
    TR_ID: C325398
    NAME: Cash Out process when value changes
    DESCRIPTION: This test case verifies Cash Out functionality when cash out value changes during cash out process on Cash Out tab
    DESCRIPTION: NOTE: When editing, separate steps in different test cases. Test case is too complex
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: * To check tolerance value on test environments please follow the next url (for information about other environments or any changes please contact UAT team):
    PRECONDITIONS: * http://backoffice-tst2.coral.co.uk/office -> Admin -> Miscellaneous -> Openbet Config -> Configurable cashout values -> COMB_TOLERANCE_VALUE. (Make sure that the tolerance is enabled with the ENABLE_COMB_TOLERANCE config)
    PRECONDITIONS: * Note: when tolerance is disabled it means that all increased values are treated as being within the tolerance
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_single_bet_and_check_cash_out_value_on_cash_out_button(self):
        """
        DESCRIPTION: Navigate to the **Single** bet and check cash out value on 'CASH OUT' button
        EXPECTED: 
        """
        pass

    def test_003_trigger_situation_when_cash_out_value_increases_within_tolerance_value_for_less_than_cashout_value_plus_cashout_valuetolerance_value_during_cash_out_process_priceodds_should_be_decreased_change_price_in_backoffice_click_cash_out___confirm_cash_out(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increases within tolerance value** (for less than cashout_value + cashout_value*tolerance_value) during cash out process (price/Odds should be decreased):
        DESCRIPTION: * Change price in backoffice
        DESCRIPTION: * Click 'CASH OUT' -> 'CONFIRM CASH OUT'
        EXPECTED: * Cash Out attempt is successful
        EXPECTED: * User balance is increased on value from step #2, not the changed one
        """
        pass

    def test_004_navigate_to_another_single_bet_and_check_cash_out_value_on_cash_out_button(self):
        """
        DESCRIPTION: Navigate to another **Single** bet and check cash out value on 'CASH OUT' button
        EXPECTED: 
        """
        pass

    def test_005_trigger_situation_when_cash_out_value_increases_above_tolerance_value_for_more_than_cashout_value_plus_cashout_valuetolerance_value_during_cash_out_process_for_cashoutbet_response_priceodds_should_be_increased_change_price_in_backoffice_click_cash_out___confirm_cash_out(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increases above tolerance value** (for more than cashout_value + cashout_value*tolerance_value) during cash out process for **cashoutBet** response (price/Odds should be increased):
        DESCRIPTION: * Change price in backoffice
        DESCRIPTION: * Click 'CASH OUT' -> 'CONFIRM CASH OUT'
        EXPECTED: * Cash Out attempt is NOT successful
        EXPECTED: * User balance is not updated
        EXPECTED: * Error messages are displayed
        EXPECTED: * subErrorCode "CASHOUT_VALUE_CHANGE" is received in cashoutBet response
        """
        pass

    def test_006_verify_error_messages(self):
        """
        DESCRIPTION: Verify error messages
        EXPECTED: The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * message of 'Cash Out is unavailable' is shown below bet line details. Text is centered.
        EXPECTED: * Underneath previous box second message is displayed with centered text Your Cash Out attempt was unsuccessful due to a price change. Please try again.
        EXPECTED: * Verify error messages disappearing
        """
        pass

    def test_007_verify_error_messages_disappearing(self):
        """
        DESCRIPTION: Verify error messages disappearing
        EXPECTED: * Error messages disappear when getBetDetail response is received with new cash out value and without error
        EXPECTED: * 'CASH OUT' button with new value and slider set to 100% are displayed
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Error messages disappear when new WebSocket connection to Cashout MS is created with new cash out value and error is not received in cashoutBet responce
        EXPECTED: * 'CASH OUT' button with new value and slider set to 100% are displayed
        """
        pass

    def test_008_trigger_situation_when_cash_out_value_increases_above_tolerance_value_for_more_than_cashout_value_plus_cashout_valuetolerance_value_during_cash_out_process_for_readbet_response_priceodds_should_be_increased_click_cash_out___confirm_cash_out_change_price_in_backoffice(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increases above tolerance value** (for more than cashout_value + cashout_value*tolerance_value) during cash out process for **readBet** response (price/Odds should be increased):
        DESCRIPTION: * Click 'CASH OUT' -> 'CONFIRM CASH OUT'
        DESCRIPTION: * Change price in backoffice
        EXPECTED: * Cash Out attempt is NOT successful
        EXPECTED: * User balance is not updated
        EXPECTED: * Error messages are displayed
        EXPECTED: * subErrorCode "CASHOUT_VALUE_CHANGE" is received in readBet response
        """
        pass

    def test_009_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: Results are the same
        """
        pass

    def test_010_repeat_steps_4_9_for_situation_when_cash_out_value_decreases_during_cash_out_process__priceodds_should_be_increased(self):
        """
        DESCRIPTION: Repeat steps #4-9 for situation when cash out value **decreases** during cash out process  (price/Odds should be increased)
        EXPECTED: Results are the same
        """
        pass

    def test_011_repeat_steps_2_10_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #2-10 for **Multiple** bets
        EXPECTED: Results are the same
        """
        pass

    def test_012_repeat_steps_2_11_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeat steps #2-11 for **Partial** Cash out attempt
        EXPECTED: Results are the same
        """
        pass
