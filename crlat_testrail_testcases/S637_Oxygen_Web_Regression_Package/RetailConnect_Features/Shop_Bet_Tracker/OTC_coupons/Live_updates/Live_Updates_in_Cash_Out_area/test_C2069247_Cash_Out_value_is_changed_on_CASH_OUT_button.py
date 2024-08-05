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
class Test_C2069247_Cash_Out_value_is_changed_on_CASH_OUT_button(Common):
    """
    TR_ID: C2069247
    NAME: Cash Out value is changed on 'CASH OUT' button
    DESCRIPTION: This test case verifies price change on 'CASH OUT' button.
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Codes should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about event in Preview tab of 'coupon?id=<coupon code>' request expand the following elements : bet -> leg -> sportsLeg -> legPart -> otherAttributes
    PRECONDITIONS: **NOTE: **
    PRECONDITIONS: *   events score can be managed in ATS Amelco
    PRECONDITIONS: *   In order to get increased Cashed Out value Price/Odds should be decreased. In order to get decreased Cashed Out value Price/Odds should be increased.
    PRECONDITIONS: **Live Price Updates behaviour:**
    PRECONDITIONS: *   Application reacts on WebSockets with new prices and unsuspended Event/Market/Outome from LiveServer
    PRECONDITIONS: *   After that application makes 'coupon?id=<coupon code>' request in order to get new Cash Out value
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

    def test_002_submit_valid_cash_out_code_which_containssingleselection_available_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains **Single **selection available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_003__trigger_cash_out_value_increasingfor_the_outcome_from_the_single_selection_verify_result_on_both_shop_bet_tracker_page_and_my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger cash out value INCREASING for the outcome from the **Single **selection
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and 'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: *   Corresponding 'Price/Odds' button is not changed within added coupon
        EXPECTED: *   Corresponding priceNum/priceDen is changed on Server Side
        EXPECTED: *   'CASH OUT' button immediately displays new cash out value (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CASH OUT' button flashes blue for 4 second (pink when value decreases)
        """
        pass

    def test_004_submit_valid_cash_out_code_which_containsmultipleselectionavailable_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains **Multiple **selection available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_005__trigger_cash_out_value_increasingfor_one_of_the_outcomes_from_the_multipleselection_verify_result_on_both_shop_bet_tracker_page_and_my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger cash out value INCREASING for one of the outcomes from the **Multiple **selection
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and 'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: *   Corresponding 'Price/Odds' button is not changed within added coupon
        EXPECTED: *   Corresponding priceNum/priceDen are changed on Server Side
        EXPECTED: *   'CASH OUT' button immediately displays new cash out value  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CASH OUT' button flashes blue for 4 second (pink when value decreases)
        """
        pass

    def test_006__trigger_cash_out_value_increasingfor_a_few_outcomes_of_from_the_multiple_selection_verify_result_on_both_shop_bet_tracker_page_and_my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger cash out value INCREASING for a few outcomes of from the **Multiple **selection
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and 'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: *   Corresponding 'Price/Odds' buttons are not changed within added coupon
        EXPECTED: *   Corresponding priceNum/priceDen are changed on Server Side
        EXPECTED: *   'CASH OUT' button immediately displays new cash out values  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CASH OUT' button flashes blue for 4 second (pink when value decreases)
        """
        pass

    def test_007__trigger_cash_out_value_increasingfor_a_few_outcomes_of_different_bet_lines_verify_result_on_both_shop_bet_tracker_page_and_my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Trigger cash out value INCREASING for a few outcomes of different bet lines
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and 'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: *   Corresponding 'Price/Odds' buttons are not changed within added coupons
        EXPECTED: *   Corresponding priceNum/priceDen are changed on Server Side
        EXPECTED: *   Corresponding 'CASH OUT' buttons immediately display new cash out values  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CASH OUT' buttons flashe blue for 4 second (pink when value decreases)
        """
        pass

    def test_008__verify_cash_out_value_increasingbefore_coupon_is_added_verify_result_on_both_shop_bet_tracker_page_and_my_bets___in_shop_bets_sub_tub(self):
        """
        DESCRIPTION: * Verify cash out value INCREASING before coupon is added
        DESCRIPTION: * Verify result on both 'Shop Bet Tracker' page and 'My Bets' -> 'In-Shop Bets' sub-tub
        EXPECTED: If coupon was not added and value was changed, after coupon is added - updated value will be shown there
        """
        pass

    def test_009_repeat_steps_2_8_with_decreasedcash_out_value(self):
        """
        DESCRIPTION: Repeat steps №2-8 with DECREASED cash out value
        EXPECTED: 
        """
        pass

    def test_010_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
