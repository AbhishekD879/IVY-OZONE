import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C874309_Place_Football_Single_prematch_bet(Common):
    """
    TR_ID: C874309
    NAME: Place Football Single prematch bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on pre-match Football events
    DESCRIPTION: *Pre-match events:
    DESCRIPTION: Event should not be started (isStarted=false)
    DESCRIPTION: Event should NOT have attribute isMarketBetInRun=true
    DESCRIPTION: AUTOTESTS [C45158730]
    PRECONDITIONS: - Login to Oxygen app
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Football page from the menu
        EXPECTED: Football landing page is loaded
        """
        pass

    def test_002_add_1_selection_to_bet_slip_from_pre_match_events(self):
        """
        DESCRIPTION: Add 1 selection to bet slip from pre-match events
        EXPECTED: Selection is added to bet slip
        """
        pass

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        pass

    def test_004_add_a_stake_in_the_single_stake_box_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a stake in the Single Stake box and click on "Place Bet" button
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £ (or another due to customer currency set while registration).
        """
        pass

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: ** The currency is in £ (or another due to customer currency set while registration)
        EXPECTED: ** The bet type is displayed: (e.g: single);
        EXPECTED: ** Odds are exactly the same as when bet has been placed;
        EXPECTED: ** Same Selection and Market is displayed where the bet was placed;
        EXPECTED: ** Correct Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet stake info area (if cashout is available for this event)
        EXPECTED: ** Unique Bet ID is displayed;
        EXPECTED: ** The balance is correctly updated;
        EXPECTED: ** Stake is correctly displayed;
        EXPECTED: ** Total Stake is correctly displayed;
        EXPECTED: ** Estimated Returns are exactly the same as on Bet Slip;
        EXPECTED: ** "Reuse Selection" and "Go Betting" buttons are displayed.
        """
        pass

    def test_006_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on "Go Betting" button
        EXPECTED: - Betslip is closed
        EXPECTED: - The customer is on Football page
        """
        pass

    def test_007_click_on_my_bets_button_from_the_header_and_select_open_bets_tab(self):
        """
        DESCRIPTION: Click on My Bets button from the header and select "Open Bets" tab
        EXPECTED: Open Bets page is opened
        """
        pass

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_event_card(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify event card
        EXPECTED: ** The currency is in £ (or another due to customer currency set while registration)
        EXPECTED: ** The bet type , Selection Name and odds are displayed
        EXPECTED: ** Event Name is displayed
        EXPECTED: ** Market where the bet has been placed
        EXPECTED: ** Time and Date - 24 hours format:
        EXPECTED: **HH:MM, Today** (e.g. "14:00 or 05:00, Today")
        EXPECTED: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov) - future dates
        EXPECTED: ** Correct Stake is correctly displayed;
        """
        pass
