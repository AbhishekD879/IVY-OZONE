import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C237480_Tracking_of_Failed_Cash_Out(Common):
    """
    TR_ID: C237480
    NAME: Tracking of Failed Cash Out
    DESCRIPTION: This test case verifies tracking of failed Cash Out
    PRECONDITIONS: * User is logged in and has placed cash out availbale single and multiple bets
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Backoffice with chosen event is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet and Desktop
    PRECONDITIONS: **cashoutStatuses filtered by the proxy:**
    PRECONDITIONS: * SELN_SUSP
    PRECONDITIONS: * SELN_NOT_DISP
    PRECONDITIONS: * LINE_NO_CASHOUT
    PRECONDITIONS: * BET_WORTH_NOTHING
    PRECONDITIONS: * INTERNAL_ERROR
    PRECONDITIONS: [How to use Fiddler][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+mock+proxy+responses+using+Fiddler
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Navigate to **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_make_failed_partial_cash_out_with_suberrorcode_with_filtered_by_proxy_cashoutstatus_in_cashoutbet_response_move_slider_to_any_percentage_other_than_100_remember_percentage_and_cash_out_offer_value_trigger_suberrorcode_with_filtered_by_proxy_cashoutstatus_ie_suspension_seln_susp_in_backoffice_click_cash_out_button_click_confirm_cash_out_button(self):
        """
        DESCRIPTION: Make **failed Partial Cash Out: with subErrorCode with filtered by proxy cashoutStatus in cashoutBet response**
        DESCRIPTION: * Move slider to any percentage, other than 100%
        DESCRIPTION: * Remember percentage and cash out offer value
        DESCRIPTION: * Trigger subErrorCode with filtered by proxy cashoutStatus (i.e. suspension SELN_SUSP) in backoffice
        DESCRIPTION: * Click 'Cash Out' button
        DESCRIPTION: * Click 'Confirm Cash Out' button
        EXPECTED: * Failure cash out message is displayed
        EXPECTED: * User balance is NOT updated
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response__second_from_the_end_object(self):
        """
        DESCRIPTION: Type in console dataLayer, tap 'Enter' and check the response (~ second from the end object)
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * 'event':  'trackEvent'
        EXPECTED: * 'eventCategory': 'cash out'
        EXPECTED: * 'eventAction': ' 'attempt'
        EXPECTED: * 'eventLabel': 'failure
        EXPECTED: * 'errorMessage': <error message>
        EXPECTED: * 'errorCode': <error code>
        EXPECTED: * 'cashOutType' : 'partial'
        EXPECTED: * 'cashOutOffer' : <cash out offer>
        EXPECTED: * 'partialPercentage' : <partial percentage>
        EXPECTED: * 'location' : 'cash out page'
        EXPECTED: where
        EXPECTED: * <error message> is equal to the front end message(s) that a customer sees (the whole text of all messages should be fired to the data layer, separated by comma)
        EXPECTED: * <error code> is equal to the back end error code (is taken from  'subErrorCode' attribute from cashoutBet or readBet response)
        EXPECTED: * all of them are sent in **lower case and without underscore**
        EXPECTED: * <cashOutOffer> and <partial percentage> are equal to chosen in step #3
        """
        pass

    def test_005_make_failed_partial_cash_out_with_suberrorcode_with_non_filtered_by_proxy_cashoutstatus_in_cashoutbet_response_move_slider_to_any_percentage_other_than_100_remember_percentage_and_cash_out_offer_value_trigger_suberrorcode_with_non_filtered_by_proxy_cashoutstatus_ie_make_cash_out_unavailable_seln_no_cashout_in_backoffice_click_cash_out_button_click_confirm_cash_out_button(self):
        """
        DESCRIPTION: Make **failed Partial Cash Out: with subErrorCode with non-filtered by proxy cashoutStatus in cashoutBet response**
        DESCRIPTION: * Move slider to any percentage, other than 100%
        DESCRIPTION: * Remember percentage and cash out offer value
        DESCRIPTION: * Trigger subErrorCode with non-filtered by proxy cashoutStatus (i.e. make cash out unavailable SELN_NO_CASHOUT) in backoffice
        DESCRIPTION: * Click 'Cash Out' button
        DESCRIPTION: * Click 'Confirm Cash Out' button
        EXPECTED: 
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_007_make_failed_partial_cash_out_without_suberrorcode_in_cashoutbet_response_using_fiddler_to_remove_it(self):
        """
        DESCRIPTION: Make **failed Partial Cash Out: without subErrorCode in cashoutBet response** using Fiddler to remove it
        EXPECTED: * Failure cash out message is displayed
        EXPECTED: * User balance is NOT updated
        """
        pass

    def test_008_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: All the same except 'errorCode': <error code> is NOT sent
        """
        pass

    def test_009_make_failed_partial_cash_out_with_suberrorcode_with_filtered_by_proxy_cashoutstatus_in_readbet_response_move_slider_to_any_percentage_other_than_100_remember_percentage_and_cash_out_offer_value_click_cash_out_button_click_confirm_cash_out_button_trigger_suberrorcode_with_filtered_by_proxy_cashoutstatus_ie_suspension_seln_susp(self):
        """
        DESCRIPTION: Make **failed Partial Cash Out: with subErrorCode with filtered by proxy cashoutStatus in readBet response**
        DESCRIPTION: * Move slider to any percentage, other than 100%
        DESCRIPTION: * Remember percentage and cash out offer value
        DESCRIPTION: * Click 'Cash Out' button
        DESCRIPTION: * Click 'Confirm Cash Out' button
        DESCRIPTION: * Trigger subErrorCode with filtered by proxy cashoutStatus (i.e. suspension SELN_SUSP)
        EXPECTED: * Failure cash out message is displayed
        EXPECTED: * User balance is NOT updated
        """
        pass

    def test_010_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_011_verify_absence_of_cashout_pending_data_in_datalayer_response(self):
        """
        DESCRIPTION: Verify absence of 'CASHOUT_PENDING' data in dataLayer response
        EXPECTED: 'CASHOUT_PENDING' data is not sent (it was received in cashoutBet response)
        """
        pass

    def test_012_make_failed_partial_cash_out_with_suberrorcode_with_non_filtered_by_proxy_cashoutstatus_in_readbet_response_move_slider_to_any_percentage_other_than_100_remember_percentage_and_cash_out_offer_value_click_cash_out_button_click_confirm_cash_out_button_trigger_suberrorcode_with_non_filtered_by_proxy_cashoutstatus_ie_make_cash_out_unavailable_seln_no_cashout_in_backoffice(self):
        """
        DESCRIPTION: Make **failed Partial Cash Out: with subErrorCode with non-filtered by proxy cashoutStatus in readBet response**
        DESCRIPTION: * Move slider to any percentage, other than 100%
        DESCRIPTION: * Remember percentage and cash out offer value
        DESCRIPTION: * Click 'Cash Out' button
        DESCRIPTION: * Click 'Confirm Cash Out' button
        DESCRIPTION: * Trigger subErrorCode with non-filtered by proxy cashoutStatus (i.e. make cash out unavailable SELN_NO_CASHOUT) in backoffice
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_4_and_11(self):
        """
        DESCRIPTION: Repeat steps #4 and #11
        EXPECTED: 
        """
        pass

    def test_014_make_failed_partial_cash_out_without_suberrorcode_in_readbet_response_using_fiddler_to_remove_it(self):
        """
        DESCRIPTION: Make **failed Partial Cash Out: without subErrorCode in readBet response** using Fiddler to remove it
        EXPECTED: * Failure cash out message is displayed
        EXPECTED: * User balance is NOT updated
        """
        pass

    def test_015_repeat_steps_4_and_11(self):
        """
        DESCRIPTION: Repeat steps #4 and #11
        EXPECTED: All the same except in step #4
        EXPECTED: * 'errorCode': <error code> is NOT sent
        """
        pass

    def test_016_repeat_steps_2_15_for_failed_full_cash_out_dont_move_slider_to_any_percentage_before_cash_out_attempt(self):
        """
        DESCRIPTION: Repeat steps #2-15 for **failed Full Cash Out** (don't move slider to any percentage before cash out attempt)
        EXPECTED: The same as #2-11 except in step #4
        EXPECTED: * 'cashOutType' : 'full'
        EXPECTED: * 'partialPercentage' : <partial percentage> is NOT sent
        """
        pass

    def test_017_repeats_steps_3_16_for_multiple_bet(self):
        """
        DESCRIPTION: Repeats steps #3-16 for **Multiple** bet
        EXPECTED: 
        """
        pass

    def test_018_navigate_to_my_bets_tab_on_event_details_page_with_placed_single_and_multiple_cash_out_available_bets(self):
        """
        DESCRIPTION: Navigate to **'My bets' tab on Event Details page** with placed single and multiple cash out available bets
        EXPECTED: 
        """
        pass

    def test_019_repeats_steps_2_17(self):
        """
        DESCRIPTION: Repeats steps #2-17
        EXPECTED: The same as #2-17 except  in step #4:
        EXPECTED: * 'location' : 'event page'
        """
        pass
