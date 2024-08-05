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
class Test_C2069250_Verify_Suspensions_occurrence_on_CONFIRM_stage(Common):
    """
    TR_ID: C2069250
    NAME: Verify Suspensions occurrence on CONFIRM stage
    DESCRIPTION: This test case verifies suspensions occurrence on CONFIRM stage
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Codes should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about event in Preview tab of 'coupon?id=<coupon code>' request expand the following elements : bet -> leg -> sportsLeg -> legPart -> otherAttributes
    PRECONDITIONS: To get SiteServer info about event use the following url, where XXX - event id:
    PRECONDITIONS: https://backoffice-tst2.coralbip.co.uk/openbet-ssviewer/Drilldown/2.15/EventToOutcomeForEvent/XXX
    PRECONDITIONS: **Live Price Updates behaviour:**
    PRECONDITIONS: *   Application reacts on WebSockets with new prices and unsuspended Event/Market/Outome from LiveServer
    PRECONDITIONS: *   After that application makes 'coupon?id=<coupon code>' request in order to get new Cash Out value
    PRECONDITIONS: NOTE: Events related changes can be managed in ATS Amelco
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
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

    def test_003_tap_cash_out_button_within_verified_selection(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button within verified selection
        EXPECTED: Button text is changed to 'CONFIRM' button
        """
        pass

    def test_004_trigger_suspension_of_eventmarketoutcome_assosiated_with_verified_selection(self):
        """
        DESCRIPTION: Trigger suspension of event/market/outcome assosiated with verified selection
        EXPECTED: 'CONFIRM'  button is changed to **'CASHOUT SUSPENDED' **disabled button
        """
        pass

    def test_005_trigger_unsuspension_of_eventmarketoutcome_assosiated_with_verified_selection(self):
        """
        DESCRIPTION: Trigger UNsuspension of event/market/outcome assosiated with verified selection
        EXPECTED: **'CASHOUT SUSPENDED' **disabled button is changed back to clickable 'CASH OUT' button and it is possible to cash out again
        """
        pass

    def test_006_submit_valid_cash_out_code_which_containsmultipleselectionavailable_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains **Multiple **selection available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_007_tap_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        EXPECTED: Button text is changed to 'CONFIRM' button
        """
        pass

    def test_008_trigger_the_situation_when_whole_multiple_bet_becomes_unavailablesuspended(self):
        """
        DESCRIPTION: Trigger the situation when whole Multiple bet becomes unavailable/suspended
        EXPECTED: 'CONFIRM'  button is changed to **'CASHOUT SUSPENDED' **disabled button
        """
        pass

    def test_009_trigger_the_situation_when_the_same_multiple_bet_line_becomes_active_again(self):
        """
        DESCRIPTION: Trigger the situation when the same Multiple bet line becomes active again
        EXPECTED: **'CASHOUT SUSPENDED' **disabled button is changed back to clickable 'CASH OUT' button and it is possible to cash out again
        """
        pass
