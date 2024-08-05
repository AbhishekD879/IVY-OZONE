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
class Test_C2069255_Verify_Cash_Out_functionality(Common):
    """
    TR_ID: C2069255
    NAME: Verify Cash Out functionality
    DESCRIPTION: This test case verifies Cash Out functionality.
    DESCRIPTION: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    DESCRIPTION: *   To find all details related to the cashed out coupon open browser console (F12) -> Network -> request 'readbet?delayId=<delayId>' -> Preview -> bet
    DESCRIPTION: * To make Cash Out available for your test bet go to AMS Amelco and start at least one event from the bet
    PRECONDITIONS: *   Valid Cash Out Coupon Code should be generated (support is needed from RCOMB team)
    PRECONDITIONS: * Load Sportbook App
    PRECONDITIONS: * Log in
    PRECONDITIONS: * Chose 'Connect' from header ribbon
    PRECONDITIONS: * Select 'Shop Bet Tracker'
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001_bet_tracker_page_is_opened(self):
        """
        DESCRIPTION: Bet Tracker page is opened
        EXPECTED: 
        """
        pass

    def test_002_submit_valid_cash_out_code_available_for_cash_out_at_least_one_bets_event_should_be_in_play(self):
        """
        DESCRIPTION: Submit valid Cash Out Code available for cash out (at least one bet's event should be in-play)
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_003_verify_cash_out_section_of_added_coupon(self):
        """
        DESCRIPTION: Verify Cash Out section of added coupon
        EXPECTED: *   '**CASH OUT **<currency_symbol>** XX.XX**' enabled button is shown alongside cash out bet line
        EXPECTED: *   Amount corresponds to '**bet.cashoutValue.****amount**' attribute
        EXPECTED: *   Cash out is available to perform
        """
        pass

    def test_004_tap_cash_out_xxxx_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT XX.XX' button
        EXPECTED: *   The button text changes to "CONFIRM"
        EXPECTED: *   "CONFIRM" button is enabled
        EXPECTED: *   The same cash out value is shown on button in format XX.XX
        EXPECTED: *   "CONFIRM" button will be changed back to "CASH OUT" after 10 sec if no actions were taken during that period
        EXPECTED: *    "CONFIRM" button will be changed back to "CASH OUT" if user tap anywhere outside the button
        """
        pass

    def test_005_tap_confirm_xxxx_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM XX.XX' button
        EXPECTED: *   The button text changes to loading spinner
        EXPECTED: *   Button is disabled
        """
        pass

    def test_006_wait_untilloading_spinner_disappears(self):
        """
        DESCRIPTION: Wait until loading spinner disappears
        EXPECTED: *   "CASH OUT SUCCESSFUL XX.XX" button is shown within the cashed out bet
        EXPECTED: *   Button is disabled and untappable
        EXPECTED: *   'Collect your Cash Out from any Coral shop using your bet receipt' label appears below the button
        EXPECTED: *   '(Complete)' label is added to the coupon header
        """
        pass

    def test_007_verifycash_out_successful_xxxx_button(self):
        """
        DESCRIPTION: Verify "CASH OUT SUCCESSFUL XX.XX" button
        EXPECTED: *   Cash out value is shown on button in format XX.XX with 2 decimal paces
        EXPECTED: *   Button remains shown till the page refresh or coupon code re-submitting
        """
        pass

    def test_008_check_readbet_request_after_successful_cash_out_in_browser_console(self):
        """
        DESCRIPTION: Check 'readbet' request after successful cash out in browser console
        EXPECTED: *   Attributes 'isCashedOut: "Y"', 'isConfirmed: "Y"', 'isFunded: "Y"' are present in 'Preview' section after request opening (see preconditions)
        EXPECTED: *   '**bet.payout.winnings**' attribute value corresponds to confirmed cash out value in step #5
        """
        pass

    def test_009__refresh_the_page_or_re_submit_coupon_code_from_previous_steps_verify_view_of_cash_out_button(self):
        """
        DESCRIPTION: * Refresh the page (or re-submit coupon code from previous steps)
        DESCRIPTION: * Verify view of Cash Out button
        EXPECTED: * '**CASHED OUT £XX.XX ON DD/MM/YYY AT HH:MM**' disabled button is shown alongside cash out bet
        EXPECTED: * Amount corresponds to '**bet.payout.****winnings**' attribute
        EXPECTED: * Date and time of cash out correspond to the ''**bet.settleDate**'' attributes in user's time zone
        EXPECTED: * Cash out is NOT available to perform
        """
        pass

    def test_010_verify_estimated_returns_fields_presence_for_cashed_out_bet(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' fields presence for cashed out bet
        EXPECTED: * 'Estimated Return' field is NOT shown for already cashed out coupons
        EXPECTED: * 'Returns' field in shown instead
        EXPECTED: * Amount corresponds to '**bet.payout.****winnings**' attribute
        """
        pass

    def test_011_go_to_my_bets__in_shop_bets_sub_tub__repeat_steps_3_10(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat steps #3-10
        EXPECTED: 
        """
        pass
