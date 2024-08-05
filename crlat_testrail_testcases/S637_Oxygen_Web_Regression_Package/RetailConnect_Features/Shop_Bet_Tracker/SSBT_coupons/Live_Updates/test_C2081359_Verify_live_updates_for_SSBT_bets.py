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
class Test_C2081359_Verify_live_updates_for_SSBT_bets(Common):
    """
    TR_ID: C2081359
    NAME: Verify live updates for SSBT bets
    DESCRIPTION: This test case verify live updates for SSBT bets
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: Request creation of SSBT bets with events that will kick off soon
    PRECONDITIONS: (for creating SSBT coupons prod events are used so we cannot trigger any match changes, just need to wait for live match incidents)
    PRECONDITIONS: Data should refresh every 30 seconds (as no push service available for SSBT at present): '/rcomb/v3/barcode' request is sent every 30 sec to get renewed data
    PRECONDITIONS: check for live updates in Browser Console -> Network -> filter by 'barcodes?id=XXXXXXXXXXXXX'
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

    def test_002_submit_valid_ssbt_coupon_that_contains_only_not_started_events__there_more_than_5_min_before_match_kick_off(self):
        """
        DESCRIPTION: Submit valid SSBT coupon that contains only not started events  (there more than 5 min before match kick off)
        EXPECTED: Coupon is submitted successfully
        """
        pass

    def test_003_verify_live_updates_on_the_coupon_are_not_requested_until_5_min_before_match_kick_off(self):
        """
        DESCRIPTION: Verify live updates on the coupon are not requested until 5 min before match kick off
        EXPECTED: 'barcodes?id=XXXXXXXXXXXXX' was sent only once when coupon was submitted  manually and hasn't been sent automatically since that
        """
        pass

    def test_004_verify_we_start_requesting_for_live_updates_5_min_before_any_match_kick_off(self):
        """
        DESCRIPTION: Verify we start requesting for live updates 5 min before (any) match kick off
        EXPECTED: * Starting from 5 min before match kick off request 'barcodes?id=XXXXXXXXXXXXX' is sent every 30 sec automatically
        """
        pass

    def test_005_wait_until_the_match_start(self):
        """
        DESCRIPTION: Wait until the match start
        EXPECTED: * Information that match is started (isStarted:"true") is received as response on automatic request (every 30 sec)
        EXPECTED: * Events Start Date is replaced with event's clock on interface immediately
        """
        pass

    def test_006_wait_until_score_will_change(self):
        """
        DESCRIPTION: Wait until score will change
        EXPECTED: * Information about new score (eventPeriod; eventParticipants) is received as response on automatic request (every 30 sec)
        EXPECTED: * Updated score is displayed on interface immediately
        """
        pass

    def test_007_wait_to_the_end_of_first_half(self):
        """
        DESCRIPTION: Wait to the end of First Half
        EXPECTED: * Information about new event period (eventPeriod) is received as response on automatic request (every 30 sec)
        EXPECTED: * Event's clock is replaced with label 'HT' on interface immediately
        EXPECTED: *we start displaying 'HT' when it's 46th min of match but sometimes First Time can last longer than 45 min, in that case if next update sends to us 47th min that means First half is prolonged so we start displaying event's clock again*
        """
        pass

    def test_008_wait_until_second_half_will_start(self):
        """
        DESCRIPTION: Wait until Second Half will start
        EXPECTED: * Information about new event period (eventPeriod) is received as response on updates request (every 30 sec)
        EXPECTED: * Label 'HT' is replaced with event's clock started from 45th min on interface immediately
        """
        pass

    def test_009_wait_until_the_end_of_the_match(self):
        """
        DESCRIPTION: Wait until the end of the match
        EXPECTED: * Information about new event period (eventPeriod) is received as response on automatic request (every 30 sec)
        EXPECTED: * Event's clock is replaced with label 'FT' on interface immediately
        EXPECTED: *we start displaying 'FT' when it's 90th min of match but sometimes match can last longer than 90 min, in that case if next update sends to us 91th min we start displaying event's clock again until we'll receive isFinished:"true"*
        """
        pass

    def test_010_verify_live_updates_are_not_requested_any_more_after_bet_is_settled_and_all_coupons_games_are_finished(self):
        """
        DESCRIPTION: Verify live updates are not requested any more after bet is settled and all coupon's games are finished
        EXPECTED: 
        """
        pass

    def test_011_submit_settled_coupons_where_not_all_events_are_finished(self):
        """
        DESCRIPTION: Submit Settled coupons where not all events are finished
        EXPECTED: request 'barcodes?id=XXXXXXXXXXXXX' is sent every 30 sec automatically
        """
        pass

    def test_012_wait_until_all_coupons_events_are_finished(self):
        """
        DESCRIPTION: Wait until all coupon's events are finished
        EXPECTED: request 'barcodes?id=XXXXXXXXXXXXX' is not sent any more
        """
        pass
