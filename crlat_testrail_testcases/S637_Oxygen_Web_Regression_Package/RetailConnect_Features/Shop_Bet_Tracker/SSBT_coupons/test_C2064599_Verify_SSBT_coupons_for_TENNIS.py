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
class Test_C2064599_Verify_SSBT_coupons_for_TENNIS(Common):
    """
    TR_ID: C2064599
    NAME: Verify SSBT coupons for TENNIS
    DESCRIPTION: Jira tickets:
    DESCRIPTION: - HMN-3423 Proxy: Implement SSBT for tennis
    DESCRIPTION: - HMN-3424 Web: Integrate SSBT tennis
    PRECONDITIONS: Need to request (generate) SSBT tennis bets with different markets.
    PRECONDITIONS: Tennis markets available:
    PRECONDITIONS: - Match Winner
    PRECONDITIONS: - Set Winner => Set1
    PRECONDITIONS: - Set Winner => Set2
    PRECONDITIONS: - Total Games Over and Under (Over 21.5 / Under 21.5) - (total of Games Score of all sets of Team A and Team B)
    PRECONDITIONS: - 1 Set - Total Games Over and Under (Over 6.5 / Under 6.5)
    PRECONDITIONS: - 2 Set - Total Games Over and Under (Over 6.5 / Under 6.5)
    PRECONDITIONS: - Handicap - If the selection is Team A +5.5
    PRECONDITIONS: Then If (total Games Scores of all sets of Team A + 5.5) > total Games Scores of all sets of Team B
    PRECONDITIONS: then its winning
    PRECONDITIONS: else its losing
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

    def test_002_submit_ssbt_tennis_code(self):
        """
        DESCRIPTION: Submit SSBT tennis code
        EXPECTED: * Betslip code is submitted successfully (page is scrolled up)
        EXPECTED: * Betslip is expanded by default
        EXPECTED: * Betslip header allows to collapse/expand bet details
        EXPECTED: * Header contain betslip code 'XXXXXXXXXXXXX' and date/time of bet creation
        EXPECTED: * Delete icon - allows delete betslip from the list
        """
        pass

    def test_003_verify_coupons_type_is_displayed_correctly(self):
        """
        DESCRIPTION: Verify coupon's type is displayed correctly
        EXPECTED: * Name of bet type is displayed under the header
        EXPECTED: * It says Betstation bet'
        """
        pass

    def test_004_verify_content_of_coupon(self):
        """
        DESCRIPTION: Verify content of Coupon
        EXPECTED: * Coupon can contain one or more bets
        EXPECTED: * Bets can be singles or multiples
        EXPECTED: * Each bet is shown as sub-section of Coupon section
        """
        pass

    def test_005_verify_sub_section_details_for_tennis_codes_for_pre_play_events(self):
        """
        DESCRIPTION: Verify sub-section details for Tennis codes for **pre-play** events
        EXPECTED: * Sub-section is titled: '<**currency symbol XX.XX**>**<Bet Type Name>' **(based on bet.betTypeRef.id attribute e.g. id=DBL => 'Double' is shown on the front-end - see preconditions)
        EXPECTED: * Selection Name (outcomeName attribute)
        EXPECTED: * Market Name (marketName attribute)
        EXPECTED: * EventParticipants (with separation line) (eventName attribute)
        EXPECTED: * Tennis icon (grey)
        EXPECTED: * Match Start DateTime (startTime attribute)
        EXPECTED: * 'Stake' field that corresponds to the '**bet**.**stake.amount**' attribute (in **<currency symbol XX.XX> **format)
        EXPECTED: * 'Estimated Returns' field that corresponds to the '**bet**.**payout.potential**' attribute (in **<currency symbol XX.XX> **format)
        EXPECTED: * 'Cash out' button says 'Event not started'
        """
        pass

    def test_006_once_event_goes_into_in_playverify_the_next(self):
        """
        DESCRIPTION: Once event goes into **in-play**
        DESCRIPTION: Verify the next
        EXPECTED: * Racket icon is green / red - depending on selection winning/ lousing status (..legPart > 0 > otherAttributes > Progress)
        EXPECTED: * Match Start DateTime is hidden
        EXPECTED: * Grid with the scores appears (from the right)
        EXPECTED: * "Cash Out" button is available and it shows cash out value or it says 'Cashout suspended' when cash out value is not available
        """
        pass

    def test_007_verify_score_grid_for_on_going_game(self):
        """
        DESCRIPTION: Verify Score grid for **on-going** game
        EXPECTED: * Labels read S (Event participant -> score), G (Event participant -> sets -> the last set), P (Event participant -> game)
        EXPECTED: * Tennis match is made up of **2-5 sets**
        EXPECTED: * To win a set, you must win at least **6 games**
        EXPECTED: * The games are scored starting at "love" (or zero) and go up to 40, but that's actually just **four points (0, 15, 30, 40)**
        EXPECTED: * Racket icon (black / green / red - depending on ..legPart > 0 > otherAttributes > Progress)
        """
        pass

    def test_008_verify_p_for_match_point(self):
        """
        DESCRIPTION: Verify P for Match point
        EXPECTED: * If Points > 40 - we show 'A' (Advantage) instead of P value
        """
        pass

    def test_009_verify_score_grid_for_game_just_finished(self):
        """
        DESCRIPTION: Verify Score grid for **game just finished**
        EXPECTED: * Only Sets (Event participant -> score) & ALL Games (Event participant -> sets) are shown
        EXPECTED: * Racket icon (black / green / red - depending on ..legPart > 0 > otherAttributes > Result)
        """
        pass

    def test_010_verify_score_grid_for_game_finished_10h_ago(self):
        """
        DESCRIPTION: Verify Score grid for **game finished 10h ago**
        EXPECTED: * After a while (can be 2h-10h-15h) server stops sending Games in the response, so we show final Sets only (Event participant -> score)!
        EXPECTED: * Racket icon (black / green / red - depending on ..legPart > 0 > otherAttributes > Result)
        """
        pass

    def test_011_go_to_my_bets__in_shop_bets_sub_tub__repeat_steps_3_10(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat steps #3-10
        EXPECTED: 
        """
        pass
