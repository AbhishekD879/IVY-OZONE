import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C874317_Verify_placing_Trixies_bet_on_Football_Coupon_Selections(Common):
    """
    TR_ID: C874317
    NAME: Verify placing Trixies bet on  Football Coupon Selections
    DESCRIPTION: Bet Placement - Verify that the customer can place a Trixie bet on Football Coupon selections
    DESCRIPTION: AUTOTEST [C48912005], [C48879277]
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment - 'Featured Coupon' section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    PRECONDITIONS: 1. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 2. List of Coupons depends on TI tool configuration data for Coupons. All available Coupons from OB response will be displayed on the page
    PRECONDITIONS: Preconditions:
    PRECONDITIONS: 1. Login to Oxygen app
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: The Football page is opened. 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_002_navigate_to_the_coupons_tab(self):
        """
        DESCRIPTION: Navigate to the Coupons tab
        EXPECTED: Coupons tab is displayed
        """
        pass

    def test_003_add_3_selections_from_3_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 3 selections from 3 different events to the betslip
        EXPECTED: Selections are added to the betslip
        """
        pass

    def test_004_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        pass

    def test_005_add_a_stake_in_the_trixie_stake_box_and_click_on_bet_now_button_from_ox_99___place_bet_button(self):
        """
        DESCRIPTION: Add a stake in the Trixie stake box and click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £.(Currency should be the same as it was set during registration)
        """
        pass

    def test_006_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: Trixie(n));
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Go Betting" buttons are displayed.
        """
        pass

    def test_007_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on "Go Betting" button
        EXPECTED: Football Coupons page is loading
        """
        pass

    def test_008_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: My Bets page is opened
        """
        pass

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: **Bet Receipt unique ID
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: **Correct Stake is correctly displayed;
        """
        pass
