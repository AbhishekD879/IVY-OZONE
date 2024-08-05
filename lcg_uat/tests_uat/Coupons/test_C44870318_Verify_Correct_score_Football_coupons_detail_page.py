import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870318_Verify_Correct_score_Football_coupons_detail_page(Common):
    """
    TR_ID: C44870318
    NAME: "Verify  Correct score Football coupons detail page"
    DESCRIPTION: "Verify below on the Correct score Football coupons detail page"
    PRECONDITIONS: Launch oxygen application - Home page opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Home Page is displayed
        """
        pass

    def test_002_go_to_football_coupons_and_select_correct_score_coupon(self):
        """
        DESCRIPTION: Go to Football coupons and Select 'correct score' coupon
        EXPECTED: Correct score coupon detail page opened
        """
        pass

    def test_003_verify_the_cs_coupon_page_header(self):
        """
        DESCRIPTION: Verify the CS Coupon page header
        EXPECTED: Header contains:
        EXPECTED: 'Back' button
        EXPECTED: 'Coupons' header name
        """
        pass

    def test_004_verify_the_cs_coupon_page_sub_header(self):
        """
        DESCRIPTION: Verify the CS Coupon page sub-header
        EXPECTED: Coupons sub-header is located below Coupons header
        EXPECTED: "Name of selected coupon" is displayed at the left side of Coupons sub-header
        EXPECTED: "Change Coupon" link and image is displayed at the right side of Coupons sub-header
        """
        pass

    def test_005_verify_the_cs_coupon_page_content(self):
        """
        DESCRIPTION: Verify the CS Coupon page content
        EXPECTED: Content is the table of events, those added to the coupon. Each row of the table contains
        EXPECTED: In the first column
        EXPECTED: Time and date of the match
        EXPECTED: Home and Away teams names (Home in the top)
        EXPECTED: In the Home column: Score switcher for Home Team, default score: 0
        EXPECTED: In the Away column: Score switcher for Away Team, default score: 0
        EXPECTED: Price button that displays the odd of the selection
        """
        pass

    def test_006_verify_the_events_ordering(self):
        """
        DESCRIPTION: Verify the Events ordering
        EXPECTED: Event are ordered by date/time and alphabetically:
        EXPECTED: Soonest go first
        EXPECTED: In alphabet order if date and time are the same, by Home team name
        """
        pass

    def test_007_add_selections_to_the_quickbetbetslip(self):
        """
        DESCRIPTION: Add selection(s) to the QuickBet/Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        pass

    def test_008_enter_stake_for_a_bet_manually_or_using_quick_stakes_buttons_tap_place_bet_in_quick_betbet_now_in_betslip(self):
        """
        DESCRIPTION: Enter 'Stake' for a bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet' in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: -Bet is successfully placed
        EXPECTED: -'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: -Balance is decreased accordingly
        """
        pass

    def test_009_verify_correct_score_coupon_is_available_only_for_pre_play_events(self):
        """
        DESCRIPTION: Verify correct score coupon is available only for Pre-play events
        EXPECTED: 
        """
        pass
