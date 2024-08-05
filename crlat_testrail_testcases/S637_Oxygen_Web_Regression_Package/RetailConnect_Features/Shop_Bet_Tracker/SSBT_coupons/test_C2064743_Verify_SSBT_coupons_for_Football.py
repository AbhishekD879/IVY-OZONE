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
class Test_C2064743_Verify_SSBT_coupons_for_Football(Common):
    """
    TR_ID: C2064743
    NAME: Verify SSBT coupons for Football
    DESCRIPTION: This test case verify coupon codes view in General
    DESCRIPTION: Bets can be placed on any sport so
    DESCRIPTION: please note that there is 3 different design only for 3 sports: Football, Tennis and Racing,
    DESCRIPTION: if there is coupon that contains bet placed on any other sport except  Football, Tennis and Racing then Football design will be applied
    PRECONDITIONS: Request creation of SSBT coupons
    PRECONDITIONS: *   Valid Cash Out Coupon Codes should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about event in Preview tab of 'coupon?id=<coupon code>' request expand the following elements : bet -> leg -> sportsLeg -> legPart -> otherAttributes
    PRECONDITIONS: *   To find details about price/odds on which bet was placed in Preview tab of 'coupon?id=<coupon code>' request expand the following elements: bet -> leg -> sportsLeg -> price
    PRECONDITIONS: *   To check correctness of Multiple sub-section name please see https://confluence.egalacoral.com/display/MOB/Multiple+Bet+Types
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

    def test_002_submit_valid_coupon_code(self):
        """
        DESCRIPTION: Submit valid coupon code
        EXPECTED: * Coupon codes is submitted successfully
        EXPECTED: * Page is automatically scrolled up after code adding
        EXPECTED: * Add Code notification is shown
        EXPECTED: * Coupon is shown to the user expanded by default
        EXPECTED: * It is possible to collapse/expand coupon section
        EXPECTED: * All associated bets are shown within the coupon
        """
        pass

    def test_003_verify_add_code_notification(self):
        """
        DESCRIPTION: Verify Add Code notification
        EXPECTED: * Add Code notification 'Cash Out code added' is shown under the entry field
        EXPECTED: * Add Code notification disappears in 3 seconds after after code submitting
        """
        pass

    def test_004_verify_coupon_section_header(self):
        """
        DESCRIPTION: Verify Coupon section header
        EXPECTED: Coupon section header consists of:
        EXPECTED: * Icon to collapse/expand section
        EXPECTED: * Coupon Code in format format 'XXXXXXXXXXXXX'
        EXPECTED: * Date of bet placement associated with coupon in format: DD/MM/YYYY
        EXPECTED: * Time of bet placement associated with coupon in format: HH:MM using 24-hour clock
        EXPECTED: * Date and time of Bet placement correspond to the '**bet.timeStamp**' attribute in user's time zone
        EXPECTED: * 'Delete' button for deleting coupon
        """
        pass

    def test_005_verify_coupons_type_is_displayed_correctly(self):
        """
        DESCRIPTION: Verify coupon's type is displayed correctly
        EXPECTED: * Name of bet type is displayed under the header
        EXPECTED: * It says 'Betstation bet'
        """
        pass

    def test_006_verify_content_of_coupon(self):
        """
        DESCRIPTION: Verify content of Coupon
        EXPECTED: * Coupon can contain one or more bets
        EXPECTED: * Bets can be singles or multiples
        EXPECTED: * Each bet is shown as sub-section of Coupon section
        """
        pass

    def test_007_verify_sub_section_details_within_added_coupon_with_pre_play_events(self):
        """
        DESCRIPTION: Verify sub-section details within added coupon with *pre-play* events
        EXPECTED: * Sub-section is titled: '<**currency symbol XX.XX**>**<Bet Type Name>' **(based on bet.betTypeRef.id attribute e.g. id=DBL => 'Double' is shown on the front-end - see preconditions)
        EXPECTED: * 'i' button containing bet details
        EXPECTED: * Selection Name (outcomeName attribute)
        EXPECTED: * Market Name (marketName attribute)
        EXPECTED: * Event Name (eventName attribute)
        EXPECTED: * Football icon (grey)
        EXPECTED: * Match Start Time (startTime attribute)
        EXPECTED: * 'Stake' field that corresponds to the '**bet**.**stake.amount**' attribute (in **<currency symbol XX.XX> **format)
        EXPECTED: * 'Estimated Returns' field that corresponds to the '**bet**.**payout.potential**' attribute (in **<currency symbol XX.XX> **format)
        EXPECTED: * 'Cash Out' button says 'Event not started'
        """
        pass

    def test_008_once_event_goes_into_in_playverify_the_next(self):
        """
        DESCRIPTION: Once event goes into *in-play*
        DESCRIPTION: Verify the next
        EXPECTED: * Ball icon is green / red - depending on selection winning/ lousing status (..legPart > 0 > otherAttributes > Progress)
        EXPECTED: * Match timer/ match periods under ball icon
        EXPECTED: * Scores appears (from the right)
        EXPECTED: * "Cash Out" button is available and it shows cash out value or it says 'Cashout suspended' when cash out value is not available
        """
        pass

    def test_009_verify_coupon_view_when_bet_is_placed_on_any_other_sport_except_football_tennis_and_racing(self):
        """
        DESCRIPTION: Verify coupon view when bet is placed on any other sport except Football, Tennis and Racing
        EXPECTED: * Coupons view remains the same, the only difference is:
        EXPECTED: *  Sport icon is missed
        EXPECTED: *  No opportunity to track game progress; score; price updates
        EXPECTED: *  No information about bet settlement
        """
        pass

    def test_010_go_to_my_bets__in_shop_bets_sub_tub__repeat_steps_3_9(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat steps #3-9
        EXPECTED: 
        """
        pass
