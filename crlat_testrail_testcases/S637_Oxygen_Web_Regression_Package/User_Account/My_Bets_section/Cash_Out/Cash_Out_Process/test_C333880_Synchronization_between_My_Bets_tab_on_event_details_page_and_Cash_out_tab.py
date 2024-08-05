import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C333880_Synchronization_between_My_Bets_tab_on_event_details_page_and_Cash_out_tab(Common):
    """
    TR_ID: C333880
    NAME: Synchronization between 'My Bets' tab on event details page and 'Cash out' tab
    DESCRIPTION: This test case verifies synchronization between 'My Bets' tab on event details page and 'Cash out' tab:
    DESCRIPTION: - during cash out attempt (successful and failure);
    DESCRIPTION: - after receiving live updates
    DESCRIPTION: DESIGNS (available from OX 99):
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f1ce639594ebeef05d0cc
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f09b1d2815d60d0789631
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: **CORAL**
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: **cashoutStatuses filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED/CASHOUT_LEGSORT_NOT_ALLOWED
    PRECONDITIONS: * CASHOUT_SELN_NO_CASHOUT
    PRECONDITIONS: * DB_ERROR
    PRECONDITIONS: Should be run on Tablet and Desktop
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Settled Bets;
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    """
    keep_browser_open = True

    def test_001_open_my_betscash_out_tab_on_event_details_page_and_cash_out_tab_on_bet_slip_widget(self):
        """
        DESCRIPTION: Open 'My Bets>Cash Out' tab on event details page and 'Cash out' tab on 'Bet Slip' widget
        EXPECTED: 'My Bets' and 'Cash out' tabs are opened simultaneously
        """
        pass

    def test_002_click_on_partial_cashout_button_on_cashout_bar(self):
        """
        DESCRIPTION: Click on 'Partial CashOut' button on CashOut bar
        EXPECTED: 'Partial CashOut' slider is shown
        """
        pass

    def test_003_move_slider_on_my_bets_tab_to_any_position(self):
        """
        DESCRIPTION: Move slider on 'My Bets' tab to any position
        EXPECTED: Slider is NOT moved to the same position on 'Cash out' tab
        """
        pass

    def test_004_click_cash_out_button_on_my_bets_tab(self):
        """
        DESCRIPTION: Click 'CASH OUT' button on 'My Bets' tab
        EXPECTED: On both tabs:
        EXPECTED: * Buttons are updated with the following centered text 'CONFIRM CASH OUT: <currency symbol><value>' and becomes green
        EXPECTED: * 'CASH OUT' button animation starts playing
        """
        pass

    def test_005_click_confirm_cash_out_button_on_my_bets___cash_out_tab_on_widget_partial_cash_out(self):
        """
        DESCRIPTION: Click 'CONFIRM CASH OUT' button on 'My Bets' -> 'Cash Out' tab on Widget (Partial Cash Out)
        EXPECTED: On both tabs:
        EXPECTED: * spinners appear on the buttons instead of the text 'CONFIRM CASH OUT'
        EXPECTED: * success cash out message is displayed instead of 'CASH OUT' button and slider
        EXPECTED: * Stake and Est. Returns values are decreased within bet accordion and bet line, new values are shown
        EXPECTED: * once the success messages completely fade out 'CASH OUT' buttons with new cash out values
        EXPECTED: * user balance is increased on previously cashed out value
        EXPECTED: Available from OX 99:
        EXPECTED: On 'My Bets' tab on EDP:
        EXPECTED: * Spinner WITHOUT count down timer appears on the button instead of the text 'CONFIRM CASH OUT'
        EXPECTED: On 'Cashout tab Widget:
        EXPECTED: * Spinner with count down timer in format XX:XX appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_006_click_cash_out_button_and_then_confirm_cash_out_button_on_my_bets_tab_on_edp_on_the_event_page___my_bets(self):
        """
        DESCRIPTION: Click 'CASH OUT' button and then 'CONFIRM CASH OUT' button on 'My Bets' tab on EDP (on the event page -> MY BETS)
        EXPECTED: On both tabs:
        EXPECTED: * spinners with count down timer appear on the buttons instead of the text 'CONFIRM CASH OUT'
        EXPECTED: * 'You Cashed Out:<value>' message is displayed above the bet with green tick icon
        EXPECTED: * 'Cash Out Successful' message is displayed below the bet
        EXPECTED: * user balance is increased on full cash out value
        EXPECTED: * bet does not disappear from the UI (till page refresh or going back to the page)
        EXPECTED: Available from OX 99:
        EXPECTED: On 'My Bets' tab on EDP:
        EXPECTED: * Spinner with count down timer in format XX:XX appears on the button instead of the text 'CONFIRM CASH OUT'
        EXPECTED: On 'Cashout tab Widget:
        EXPECTED: * Spinner WITHOUT count down timer appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_007_trigger_cashout_value_filtered_by_proxy_eg_cashout_seln_suspended_or_cashout_legsort_not_allowed_during_cash_out_attempt(self):
        """
        DESCRIPTION: Trigger Cashout value **filtered by proxy** (e.g. 'CASHOUT_SELN_SUSPENDED' OR 'CASHOUT_LEGSORT_NOT_ALLOWED') during cash out attempt
        EXPECTED: 'Cash out suspended' message is displayed on green disabled button instead of Cashout text
        """
        pass

    def test_008_navigate_to_another_bet_and_trigger_cashout_value_not_filtered_by_proxy_cashout_seln_no_cashout__during_cash_out_attempt(self):
        """
        DESCRIPTION: Navigate to another bet and trigger cashout value **not filtered by proxy** 'CASHOUT_SELN_NO_CASHOUT'  during cash out attempt
        EXPECTED: * Bet is displayed on on 'My Bets' and 'Cash Out' tabs with an error message **CASH OUT NOT AVAILABLE** (instead of 'CASH OUT' button)
        EXPECTED: * After 5 seconds (Only for Cash Out tab, NOT for Open Bets and Settled Bets):
        EXPECTED: * bet disappears from 'Cash Out' tab
        EXPECTED: * bet is displayed as non cash out bet (without 'CASH OUT' button)
        """
        pass

    def test_009_in_ob_backoffice_trigger_cashoutstatus_filtered_by_proxy_eg_cashout_seln_suspended_or_cashout_legsort_not_allowed_in_getbetdetail_responsesuspend_event_or_market_or_selection_for_event_with_placed_bet(self):
        """
        DESCRIPTION: In OB Backoffice trigger **cashoutStatus filtered by proxy** (e.g. "CASHOUT_SELN_SUSPENDED" OR "CASHOUT_LEGSORT_NOT_ALLOWED") in getbetDetail response
        DESCRIPTION: (Suspend event or market or selection for event with placed bet)
        EXPECTED: 'Cash out suspended' message is displayed instead of 'CASH OUT' text on the button on 'My Bets' and 'Cash out' tabs
        """
        pass

    def test_010_in_ob_backoffice_trigger_cashoutstatus_not_filtered_by_proxy_eg_cashout_seln_no_cashout_in_getbetdetail_response_for_the_same_betdisable_cashout_available_option_and_undisplay_eventmarketselection(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashOutStatus **not filtered by proxy** (e.g. "CASHOUT_SELN_NO_CASHOUT") in getbetDetail response for the same bet
        DESCRIPTION: (disable 'Cashout Available' option and undisplay event/market/selection)
        EXPECTED: * On 'Cash Out' tab bet is displayed with an error message **CASH OUT NOT AVAILABLE**  during 5 seconds. After 5 seconds bet disappears from 'Cash Out' tab
        EXPECTED: * On 'My Bets' bet is displayed as non cash out bet (without 'CASH OUT' button and slider) at once
        """
        pass

    def test_011_in_ob_backoffice_trigger_price_change_for_any_bet(self):
        """
        DESCRIPTION: In OB Backoffice trigger price change for any bet
        EXPECTED: Cash out values are updated on 'CASH OUT' buttons on both tabs
        """
        pass

    def test_012_repeat_steps_2_8_on_cash_out_tab(self):
        """
        DESCRIPTION: Repeat steps #2-8 on 'Cash Out' tab
        EXPECTED: Results are the same for OX<99
        EXPECTED: Results from OX 99:
        EXPECTED: On 'Cashout tab:
        EXPECTED: * Spinner with count down timer appears on the button instead of the text 'CONFIRM CASH OUT'
        EXPECTED: On 'My Bets' tab:
        EXPECTED: * Spinner WITHOUT count down timer appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass
