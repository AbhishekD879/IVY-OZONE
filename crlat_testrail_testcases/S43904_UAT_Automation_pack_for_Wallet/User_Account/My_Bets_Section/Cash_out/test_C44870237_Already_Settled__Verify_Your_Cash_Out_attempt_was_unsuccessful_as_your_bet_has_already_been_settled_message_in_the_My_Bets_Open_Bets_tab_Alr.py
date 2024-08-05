import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870237_Already_Settled__Verify_Your_Cash_Out_attempt_was_unsuccessful_as_your_bet_has_already_been_settled_message_in_the_My_Bets_Open_Bets_tab_Already_Cashedout__Verify_Your_Cash_Out_attempt_was_unsuccessful_as_your_bet_has_already_been_Cashe(Common):
    """
    TR_ID: C44870237
    NAME: "Already Settled - Verify  ""Your Cash Out attempt was unsuccessful as your bet has already been settled."" message in the My Bets > Open Bets tab. Already Cashedout - Verify ""Your Cash Out attempt was unsuccessful as your bet has already been Cashe
    DESCRIPTION: "Already Settled - Verify  ""Your Cash Out attempt was unsuccessful as your bet has already been settled."" message in the My Bets > Open Bets tab.
    DESCRIPTION: Already Cashedout - Verify ""Your Cash Out attempt was unsuccessful as your bet has already been Cashed Out."" message in the My Bets > Open Bets tab .
    DESCRIPTION: Freebet cash-out not allowed  - Verify ""'Bets placed with a free bet or bets triggering a free bet offer cannot be cashed out."" message in the My Bets > Open Bets tab.
    DESCRIPTION: Cash-out not available for certain bet types - Verify 'Cash out is unavailable on this bet.'  message in the My Bets > Open Bets tab.
    DESCRIPTION: SP Selection - Verify 'Bets placed at starting price (SP) cannot be cashed out.'  message in the My Bets > Open Bets tab.
    DESCRIPTION: Cash out from location not allowed  - Verify  'Sorry, we cannot authorise cash out from your location. Please contact us.' message in My Bets > Open Bets tab .
    DESCRIPTION: Account is blocked from cash-out - Verify ''Sorry, we cannot authorise Cash Out from your account. Please contact us if you feel this may be in error' message in My Bets > Open Bets tab .
    DESCRIPTION: Cash-out value is £0.00 - Verify 'Cash Out is unavailable because the offer is less than 0.00' message in My Bets > Open Bets tab
    DESCRIPTION: Cash out no odds available - Verify 'One or more events in your bet are not available for in-play Cash Out.' message in My Bets > Open Bets tab
    DESCRIPTION: In play cash-out not available for some of your selections - Verify 'One or more events in your bet are not available for cash out' message in
    DESCRIPTION: Example: Football and Badminton double, of which only football is available for cash-out
    DESCRIPTION: Load error - Verify 'Cash Out unsuccessful, please try again.' message When user select the cash out button and  an error occurs when loading
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Singles and Multiple bets where Cash Out offer is available
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: User has some bets available for Cashout
        """
        pass

    def test_002_trigger_suberrorcode_cashout_bet_settled_for_cashoutbet_response_during_cash_out_attemptsuspend_event_or_market_or_selection_for_event_with_placed_bet_in_backofficeimmediately_click_cash_out_and_confrim_cash_out_buttonsusing_fiddler_tool_mock_response_in_cashoutbet_responseand_verify_error_message(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_BET_SETTLED' for cashoutBet response during cash out attempt:
        DESCRIPTION: Suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: Immediately click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: Using Fiddler tool mock response in cashoutBet response
        DESCRIPTION: and Verify error message
        EXPECTED: Message box with an "X" in a circle and message of 'CASH OUT UNSUCCESSFUL' is shown below bet line details. Icon and text are centred.
        EXPECTED: Underneath previous box second message is displayed with centred text 'Your Cash Out attempt was unsuccessful, as your bet has already been settled.'
        """
        pass

    def test_003_trigger_suberrorcode_cashout_bet_cashed_out_for_cashoutbet_response_during_cash_out_attemptsuspend_event_or_market_or_selection_for_event_with_placed_bet_in_backofficeimmediately_click_cash_out_and_confrim_cash_out_buttonsusing_fiddler_tool_mock_response_in_cashoutbet_responseand_verify_error_messages(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_BET_CASHED_OUT' for cashoutBet response during cash out attempt:
        DESCRIPTION: Suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: Immediately click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: Using Fiddler tool mock response in cashoutBet response
        DESCRIPTION: and Verify error messages
        EXPECTED: Message box with an "X" in a circle and message of 'CASH OUT UNSUCCESSFUL' is shown below bet line details. Icon and text are centred.
        EXPECTED: Underneath previous box second message is displayed with centred text 'Your Cash Out attempt was unsuccessful, as your bet has already been Cashed Out.'
        """
        pass

    def test_004_place_a_bet_using_freebet_for_a_event_which_has_cashout_available__and_verify_the_user_is_able_to_cashout_and_verify_the_reduced_cashout_message(self):
        """
        DESCRIPTION: Place a bet using Freebet for a event which has Cashout available  and verify the user is able to cashout and verify the reduced cashout message.
        EXPECTED: Cashout is available and message is displayed as "Free Bets has a reduced cashout Value"
        """
        pass
