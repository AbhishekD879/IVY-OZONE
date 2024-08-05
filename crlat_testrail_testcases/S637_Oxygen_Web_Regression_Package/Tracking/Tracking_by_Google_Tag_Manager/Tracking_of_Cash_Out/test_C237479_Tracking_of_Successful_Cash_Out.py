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
class Test_C237479_Tracking_of_Successful_Cash_Out(Common):
    """
    TR_ID: C237479
    NAME: Tracking of Successful Cash Out
    DESCRIPTION: This test case verifies tracking of successful Cash Out
    PRECONDITIONS: * User is logged in and has placed cash out availbale single and multiple bets
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet and Desktop
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to **'Cash out' tab** on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Navigate to **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_make_successful_partial_cash_out_move_slider_to_any_percentage_other_than_100_remember_percentage_and_cash_out_offer_value_click_cash_out_button_click_confirm_cash_out_button(self):
        """
        DESCRIPTION: Make **successful Partial Cash Out:**
        DESCRIPTION: * Move slider to any percentage, other than 100%
        DESCRIPTION: * Remember percentage and cash out offer value
        DESCRIPTION: * Click 'Cash Out' button
        DESCRIPTION: * Click 'Confirm Cash Out' button
        EXPECTED: * Success partial cash out message is displayed and is replaced with cash out button again
        EXPECTED: * User balance is updated
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response__second_from_the_end_object(self):
        """
        DESCRIPTION: Type in console dataLayer, tap 'Enter' and check the response (~ second from the end object)
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * 'event':  'trackEvent'
        EXPECTED: * 'eventCategory': 'cash out'
        EXPECTED: * 'eventAction': ' 'attempt'
        EXPECTED: * 'eventLabel': 'success'
        EXPECTED: * 'cashOutType' : 'partial'
        EXPECTED: * 'cashOutOffer' : <cash out offer>
        EXPECTED: * 'partialPercentage' : <partial percentage>
        EXPECTED: * 'successMessage' : <success message>
        EXPECTED: * 'location' : 'cash out page'
        EXPECTED: where
        EXPECTED: * <cashOutOffer> and <partial percentage> are equal to chosen in step #3
        EXPECTED: * <success message> is equal to the front end messages that a customer sees (the whole text of both messages should be fired to the data layer and both of them are sent in **lower case and without underscore** and separated by comma)
        """
        pass

    def test_005_verify_absence_of_cashout_pending_data_in_datalayer_response(self):
        """
        DESCRIPTION: Verify absence of 'CASHOUT_PENDING' data in dataLayer response
        EXPECTED: 'CASHOUT_PENDING' data is not sent (it was received in cashoutBet response)
        """
        pass

    def test_006_for_the_same_bet_make_successful_full_cash_out_leave_slider_at_100_remember_cash_out_offer_value_click_cash_out_button_click_confirm_cash_out_button(self):
        """
        DESCRIPTION: For the same bet make **successful Full Cash Out:**
        DESCRIPTION: * Leave slider at 100%
        DESCRIPTION: * Remember cash out offer value
        DESCRIPTION: * Click 'Cash Out' button
        DESCRIPTION: * Click 'Confirm Cash Out' button
        EXPECTED: * Success full cash out message is displayed
        EXPECTED: * User balance is updated
        EXPECTED: * bet disappears after few seconds
        """
        pass

    def test_007_repeats_steps_4_5(self):
        """
        DESCRIPTION: Repeats steps #4-5
        EXPECTED: The same as #4-5 except:
        EXPECTED: * 'cashOutType' : 'full'
        EXPECTED: * 'partialPercentage' : <partial percentage> is NOT sent
        """
        pass

    def test_008_repeats_steps_3_7_for_multiple_bet(self):
        """
        DESCRIPTION: Repeats steps #3-7 for **Multiple** bet
        EXPECTED: The same as #3-6
        """
        pass

    def test_009_navigate_to_my_bets_tab_on_event_details_page_with_placed_single_and_multiple_cash_out_available_bets(self):
        """
        DESCRIPTION: Navigate to **'My bets' tab on Event Details page** with placed single and multiple cash out available bets
        EXPECTED: 
        """
        pass

    def test_010_repeats_steps_2_7(self):
        """
        DESCRIPTION: Repeats steps #2-7
        EXPECTED: The same as #2-7 except:
        EXPECTED: * 'location' : 'event page'
        """
        pass
