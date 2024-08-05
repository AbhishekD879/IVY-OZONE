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
class Test_C2069248_Cash_Out_value_is_changed_on_CONFIRM_button(Common):
    """
    TR_ID: C2069248
    NAME: Cash Out value is changed on 'CONFIRM' button
    DESCRIPTION: This test case verifies price change on 'CONFIRM' button
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Codes should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about event in Preview tab of 'coupon?id=<coupon code>' request expand the following elements : bet -> leg -> sportsLeg -> legPart -> otherAttributes
    PRECONDITIONS: **NOTE: **
    PRECONDITIONS: *   Event's ralated changes can be managed in ATS Amelco
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

    def test_003_tap_cash_out_button_of_verified_selection(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button of verified selection
        EXPECTED: 
        """
        pass

    def test_004_trigger_cash_out_value_increasingfor_the_outcome_from_thesingleselection(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for the outcome from the **Single **selection
        EXPECTED: *   Corresponding 'Price/Odds' button is not changed within added coupon
        EXPECTED: *   Corresponding priceNum/priceDen is changed on Server Side
        EXPECTED: *   'CONFIRM' button immediately displays new cash out value  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CONFIRM' button flashes blue for 4 second (pink when value decreases)
        """
        pass

    def test_005_submit_valid_cash_out_code_which_containsmultipleselectionavailable_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains **Multiple **selection available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_006_go_to_verified_multipleselection_and_tap_cash_out_button(self):
        """
        DESCRIPTION: Go to verified **Multiple **selection and tap 'CASH OUT' button
        EXPECTED: 
        """
        pass

    def test_007_trigger_cash_out_value_increasingfor_one_of_the_outcomes_from_themultipleselection(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for one of the outcomes from the **Multiple **selection
        EXPECTED: *   Corresponding 'Price/Odds' button is not changed within added coupon
        EXPECTED: *   Corresponding priceNum/priceDen are changed on Server Side
        EXPECTED: *   'CONFIRM' button immediately displays new cash out value  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CONFIRM' button flashes blue for 4 second (pink when value decreases)
        """
        pass

    def test_008_trigger_cash_out_value_increasingfor_a_few_outcomes_of_from_themultipleselection(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for a few outcomes of from the **Multiple **selection
        EXPECTED: *   Corresponding 'Price/Odds' buttons are not changed within added coupon
        EXPECTED: *   Corresponding priceNum/priceDen are changed on Server Side
        EXPECTED: *   'CONFIRM' button immediately displays new cash out values  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CONFIRM' button flashes blue for 4 second (pink when value decreases)
        """
        pass

    def test_009_tap_cash_out_buttons_for_all_added_bet_lines(self):
        """
        DESCRIPTION: Tap 'CASH OUT' buttons for all added bet lines
        EXPECTED: 
        """
        pass

    def test_010_trigger_cash_out_value_increasingfor_a_few_outcomes_of_different_bet_lines(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for a few outcomes of different bet lines
        EXPECTED: *   Corresponding 'Price/Odds' buttons are not changed within added coupons
        EXPECTED: *   Corresponding priceNum/priceDen are changed on Server Side
        EXPECTED: *   Corresponding 'CONFIRM' buttons immediately display new cash out values  (corresponds to 'bet.cashoutValue.amount' attribute of the last 'coupon' request)
        EXPECTED: *   'CONFIRM' buttons flashe blue for 4 second (pink when value decreases)
        """
        pass

    def test_011_verify_cash_out_value_increasingbefore_coupon_is_added(self):
        """
        DESCRIPTION: Verify cash out value INCREASING before coupon is added
        EXPECTED: If coupon was not added and value was changed, after coupon is added - updated value will be shown there
        """
        pass

    def test_012_repeat_steps_2_11_with_decreased_value(self):
        """
        DESCRIPTION: Repeat steps №2-11 with DECREASED value
        EXPECTED: 
        """
        pass
