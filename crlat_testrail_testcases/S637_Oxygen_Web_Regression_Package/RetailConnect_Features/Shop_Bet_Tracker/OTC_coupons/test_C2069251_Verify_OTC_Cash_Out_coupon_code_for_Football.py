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
class Test_C2069251_Verify_OTC_Cash_Out_coupon_code_for_Football(Common):
    """
    TR_ID: C2069251
    NAME: Verify OTC Cash Out coupon code for Football
    DESCRIPTION: This test case verify coupon codes view in General
    DESCRIPTION: Bets can be placed on any sport so
    DESCRIPTION: please note that there is 3 different design only for 3 sports: Football, Tennis and Racing,
    DESCRIPTION: if there is coupon that contains bet placed on any other sport except Football, Tennis and Racing then Football design will be applied
    PRECONDITIONS: *   Valid Cash Out Coupon Code should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about date and time of bet placement in Preview tab of 'coupon?id=<coupon code>' request expand the following elements: bet -> timeStamp
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

    def test_002_submit_valid_cash_out_code(self):
        """
        DESCRIPTION: Submit valid Cash Out Code
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        EXPECTED: *   Add Code notification is shown under entry field: ''Cash Out code added', it desapears in 3 sec
        EXPECTED: *   It is possible to collapse/expand coupon section
        EXPECTED: *   All associated bets are shown within the coupon
        """
        pass

    def test_003_verify_cash_out_coupon_section_header(self):
        """
        DESCRIPTION: Verify Cash Out Coupon section header
        EXPECTED: Cash Out Coupon section header consists of:
        EXPECTED: *   Icon to collapse/expand section
        EXPECTED: *   Coupon Code in format 'XXX-XXXX' OR 'XXXXXXXXXXXX' where 'X...' - entered Cash Out Code
        EXPECTED: *   Date of bet placement associated with coupon in format: DD/MM/YYYY
        EXPECTED: *   Time of bet placement associated with coupon in format: HH:MM using 24-hour clock
        EXPECTED: *   Date and time of Bet placement correspond to the '**bet.timeStamp**' attribute in user's time zone
        EXPECTED: *   'Delete' button for deleting coupon
        EXPECTED: *   'Over the counter bet' title is displayed underneath
        """
        pass

    def test_004_verify_content_of_cash_out_coupon(self):
        """
        DESCRIPTION: Verify content of Cash Out Coupon
        EXPECTED: *   Cash Out coupon can contain one or more associated with entered Cash Out Code bets
        EXPECTED: *   Bets can be singles or multiples
        EXPECTED: *   Each bet has it's own cash out option
        EXPECTED: *   Each bet is shown as sub-section of Cash Out Coupon section
        """
        pass

    def test_005_verify_selection_details_within_added_coupon_with_pre_play_events(self):
        """
        DESCRIPTION: Verify selection details within added coupon with **pre-play** events
        EXPECTED: 1.  Sub-section is titled: '<**currency symbol XX.XX**>**<Bet Type Name>' **(based on bet.betTypeRef.id attribute e.g. id=DBL => 'Double' is shown on the front-end - see preconditions)
        EXPECTED: 2.  Selections Names (outcomeName attributes)
        EXPECTED: 3.  Market Names (marketName attributes)
        EXPECTED: 4.  Selections Price/Odds (not tappable) (num/den attributes)
        EXPECTED: 5.  Event Names (eventName attributes)
        EXPECTED: 6.  Football icons
        EXPECTED: 7.  Match time (for upcoming events - startTime attributes)
        EXPECTED: 8.  'Stake' field that corresponds to the '**bet**.**stake.amount**' attribute (in **<currency symbol XX.XX> **format)
        EXPECTED: 9. 'Estimated Returns' field that corresponds to the '**bet**.**payout.potential**' attribute (in **<currency symbol XX.XX> **format)
        EXPECTED: * 'Cash Out' button says 'Event not started'
        """
        pass

    def test_006_once_event_goes_into_in_playverify_the_next(self):
        """
        DESCRIPTION: Once event goes into **in-play**
        DESCRIPTION: Verify the next
        EXPECTED: * Ball icon is green / red - depending on selection winning/ lousing status
        EXPECTED: * Match timer/ match periods under ball icon
        EXPECTED: * Scores appears (from the right)
        EXPECTED: * "Cash Out" button is available and it shows cash out value or it says 'Cashout suspended' when cash out value is not available
        """
        pass

    def test_007_go_to_my_bets__in_shop_bets__sub_tub__repeat_steps_3_6(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets'  sub-tub ->
        DESCRIPTION: repeat steps #3-6
        EXPECTED: 
        """
        pass
