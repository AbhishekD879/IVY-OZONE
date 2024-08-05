import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2081356_Verify_submitting_of_invalid_Cash_Out_Code_few_times_in_a_row(Common):
    """
    TR_ID: C2081356
    NAME: Verify submitting of invalid Cash Out Code few times in a row
    DESCRIPTION: This test case verify submitting of invalid Cash Out Code
    DESCRIPTION: **JARA ticket: **BMA-8026 MS: RCOMB - Error Handling/Noification for Coupon Codes
    PRECONDITIONS: Related PROXY test case:
    PRECONDITIONS: [C356019 Verify managing delays when invalid barcode is entered few times in a row](https://ladbrokescoral.testrail.com/index.php?/cases/view/356019)
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: https://***/keystone/ -> brand 'rcomb' -> System-configuration -> RCOMBDELAYS:
    PRECONDITIONS: * noOfInvalidCodes - number of unsuccessful attempts when 'delay' remains 0
    PRECONDITIONS: * firstDelay - this delay is added after last attempt from 'noOfInvalidCodes '
    PRECONDITIONS: * incrementsBy - each following unsuccessful attempt is increased on this value
    PRECONDITIONS: * stopIncrements - when after delays increasing this value is reached then delay is set as 'timeoutInvalid'
    PRECONDITIONS: * timeoutInvalid  - each following 'delay' is equal 'timeoutInvalid' until valid code is entered
    PRECONDITIONS: Make sure Bet Tracker feature is turned on in CMS: System configuration -> Connect -> shop Bet Tracker
    """
    keep_browser_open = True

    def test_001_run_following_steps_while_entering_coupon_code_manually_and_while_scanning_coupons_barcode_scanning_is_available_on_native_wrapper_only(self):
        """
        DESCRIPTION: Run following steps while entering coupon code manually and while scanning coupons barcode (scanning is available on native wrapper only)
        EXPECTED: 
        """
        pass

    def test_002_go_to_cms_and_set_following_values_for_parameters_noofinvalidcodes__3_firstdelay__10_incrementsby__15_stopincrements__60_timeoutinvalid__90(self):
        """
        DESCRIPTION: Go to CMS and set following values for parameters:
        DESCRIPTION: * noOfInvalidCodes = 3
        DESCRIPTION: * firstDelay = 10
        DESCRIPTION: * incrementsBy = 15
        DESCRIPTION: * stopIncrements = 60
        DESCRIPTION: * timeoutInvalid = 90
        EXPECTED: 
        """
        pass

    def test_003__load_spotbook_app_chose_connect_from_header_ribbon_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: * Load SpotBook App
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Tap 'Shop Bet Tracker' item
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_004_enter_invalid_coupon_code_and_click_submit_button(self):
        """
        DESCRIPTION: Enter invalid coupon code and click 'Submit' button
        EXPECTED: Message 'The coupon code entered is incorrect, please try again' is displayed
        """
        pass

    def test_005_submit_invalid_coupon_two_more_times(self):
        """
        DESCRIPTION: Submit invalid coupon two more times
        EXPECTED: * After last unsuccessful attempt message 'The coupon code entered is incorrect, please try again in 10 seconds' is displayed
        EXPECTED: * Entry field is cleared
        EXPECTED: * 'Submit' button remains disabled for 10 seconds
        """
        pass

    def test_006_submit_invalid_coupon_code_one_more_time(self):
        """
        DESCRIPTION: Submit invalid coupon code one more time
        EXPECTED: * Delay is increased on 15 seconds, so now message says 'The coupon code entered is incorrect, please try again in 25 seconds'
        EXPECTED: * Entry field is cleared
        EXPECTED: * 'Submit' button remains disabled for 25 seconds
        """
        pass

    def test_007_submit_invalid_coupon_code_3_times_to_reach_stopincrements__value(self):
        """
        DESCRIPTION: Submit invalid coupon code 3 times (to reach 'stopIncrements ' value)
        EXPECTED: * After each unsuccessful attempt delay is increased on 15 seconds
        EXPECTED: * After last unsuccessful attempt delay is equal to 90 seconds and message says 'The coupon code entered is incorrect, please try again in 90 seconds'
        EXPECTED: * Entry field is cleared
        EXPECTED: * 'Submit' button remains disabled for 90 seconds
        """
        pass

    def test_008_submit_invalid_coupon_code_one_more_time(self):
        """
        DESCRIPTION: Submit invalid coupon code one more time
        EXPECTED: Delay was dropped to 0, result of this step is the same as step4. New cycle of attempts is initiated.
        """
        pass

    def test_009_submit_valid_coupon_code(self):
        """
        DESCRIPTION: Submit valid coupon code
        EXPECTED: Code is submitted successfully
        """
        pass

    def test_010_submit_invalid_coupon_code(self):
        """
        DESCRIPTION: Submit invalid coupon code
        EXPECTED: * Delays increment is reset
        EXPECTED: * Delays increment after entering invalid codes is processed in the same way as described in steps #3-7
        """
        pass
