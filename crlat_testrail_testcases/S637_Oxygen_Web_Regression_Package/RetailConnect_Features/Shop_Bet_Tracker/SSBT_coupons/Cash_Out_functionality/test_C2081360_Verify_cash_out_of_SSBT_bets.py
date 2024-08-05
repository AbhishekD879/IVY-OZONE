import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2081360_Verify_cash_out_of_SSBT_bets(Common):
    """
    TR_ID: C2081360
    NAME: Verify cash out of SSBT bets
    DESCRIPTION: This test case verify cash out functionality for SSBT bets
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: Request creation of SSBT bets with in-play and pre-play events
    PRECONDITIONS: * Load https://coral-retail-bpp-dev.symphony-solutions.eu/
    PRECONDITIONS: * Use /rcomb/v3/barcode endpoint to check barcode details (Cash Out value, Cash Out status/ reason etc.)
    PRECONDITIONS: Note that SSBT barcodes can be created for pre-prod env, real events from prod are used there,  so we cannot trigger any match changes, just need to wait for live match incidents. To test all cases you need to request bets placed on events that should start during work hours.
    PRECONDITIONS: __________________
    PRECONDITIONS: Live updates functionality for SSBT barcodes is implemented in following way:
    PRECONDITIONS: * Front end is sending '/rcomb/v3/barcode' request every 30 sec to get renewed data
    PRECONDITIONS: * Front end starts sending  '/rcomb/v3/barcode' request 5 min before match kick off
    PRECONDITIONS: * Front end stops sending '/rcomb/v3/barcode' request 5 min after last coupons match is finished
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_to_verify_that_cash_out_is_not_available_when_all_coupons_events_are_not_started_submit_valid_ssbt_barcode_all_coupons_events_are_not_started_yet(self):
        """
        DESCRIPTION: To verify that Cash Out is not available when all coupon's events are not started:
        DESCRIPTION: * Submit valid SSBT barcode
        DESCRIPTION: * All coupon's events are not started yet
        EXPECTED: * Coupon is submitted successfully
        EXPECTED: * Cash out is not available
        EXPECTED: * Disabled border button is shown and it says "Event Not Started"
        """
        pass

    def test_003_to_verify_that_cash_out_is_not_available_when_cash_out_value_is_equal_to_zero_submit_valid_ssbt_barcode_at_least_one_event_is_started_cashoutvalue__0_use__rcombv2barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeusingget_to_check_cash_out_value(self):
        """
        DESCRIPTION: To verify that Cash out is not available when Cash Out value is equal to zero:
        DESCRIPTION: * Submit valid SSBT barcode
        DESCRIPTION: * At least one event is started
        DESCRIPTION: * "cashoutValue" = 0 (use  [/rcomb/v2/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeUsingGET) to check Cash Out value)
        EXPECTED: * Coupon is submitted successfully
        EXPECTED: * Cash out is not available
        EXPECTED: * Disabled border button is shown and it says "Cashout Unavailable"
        """
        pass

    def test_004_to_verify_that_cash_out_cannot_be_done_when_price_has_been_changed_right_after_tapping_cash_out_button_and_before_next_30_sec_update_submit_valid_ssbt_barcode_at_least_one_event_is_started_cashoutvalue__0_to_catch_the_moment_when_price_has_changed_use_rcombv2barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeusingget_frequently_once_youve_notices_cash_out_value_is_different_than_on_interface_tap_cash_out_button_before_next_30_sec_update_happens_price_is_changing_quite_frequently_so_it_shouldnt_take_long_to_catch_the_moment(self):
        """
        DESCRIPTION: To verify that Cash out cannot be done when price has been changed right after tapping Cash Out button and before next 30 sec update:
        DESCRIPTION: * Submit valid SSBT barcode
        DESCRIPTION: * At least one event is started
        DESCRIPTION: * "cashoutValue" > 0
        DESCRIPTION: * To catch the moment when price has changed use [/rcomb/v2/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeUsingGET) frequently, once you've notices Cash Out value is different than on interface tap 'Cash Out' button before next 30 sec update happens (price is changing quite frequently so it shouldn't take long to catch the moment)
        EXPECTED: * Right after tapping 'Cash Out' -> 'Confirm' buttons user sees message (above the button on red background) "Cash Out value for this bet has changed"
        EXPECTED: * Button itself is turned to pink color if price has decreased or to blue if price has increased for 4 sec
        EXPECTED: * New price will be displayed on Cash Out button after next 30 sec update
        """
        pass

    def test_005_to_verify_that_cash_out_can_be_done_successfully_submit_valid_ssbt_barcode_at_least_one_event_is_started_cashoutvalue__0(self):
        """
        DESCRIPTION: To verify that Cash out can be done successfully:
        DESCRIPTION: * Submit valid SSBT barcode
        DESCRIPTION: * At least one event is started
        DESCRIPTION: * "cashoutValue" > 0
        EXPECTED: * Tap 'Cash Out' button
        EXPECTED: * 'Cash Out' button is turned to 'Confirm' button
        EXPECTED: * "CONFIRM" button will be changed back to "CASH OUT" after 10 sec if no actions were taken during that period
        EXPECTED: * "CONFIRM" button will be changed back to "CASH OUT" if user tap anywhere outside the button
        EXPECTED: * Tap 'Confirm' button
        EXPECTED: * Button is greyed and it says 'Cash Out successful'
        EXPECTED: * Message underneath says 'Collect your Cash Out from any Coral shop using bet receipt'
        EXPECTED: * After next 30 sec update bet is moved to 'Settled bets' tab and border button says 'Bet settled'
        EXPECTED: * 'Returns' value is equal to Cashed Out value
        """
        pass

    def test_006_to_verify_that_cash_out_cannot_be_done_when_bet_is_settled_submit_valid_ssbt_barcode_at_least_one_event_is_started_cashoutvalue__0_cash_out_this_bet_right_after_that_try_to_cash_out_the_same_bet_on_different_device_or_browser_tab(self):
        """
        DESCRIPTION: To verify that Cash out cannot be done when bet is settled:
        DESCRIPTION: * Submit valid SSBT barcode
        DESCRIPTION: * At least one event is started
        DESCRIPTION: * "cashoutValue" > 0
        DESCRIPTION: * Cash out this bet
        DESCRIPTION: * Right after that try to Cash out the same bet on different device or browser tab
        EXPECTED: * Right after tapping 'Cash Out' -> 'Confirm' border button says "Cashout Unavailable"
        EXPECTED: * After next 30 sec update it turned to 'Bet settled'
        """
        pass
