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
class Test_C874310_Place_In_Play_single_bet(Common):
    """
    TR_ID: C874310
    NAME: Place In Play single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on "In Play" selections
    DESCRIPTION: AUTOTEST [C47658981]
    PRECONDITIONS: 1. Login to Oxygen app
    """
    keep_browser_open = True

    def test_001_navigate_to_in_play_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to In Play page from the menu
        EXPECTED: The In Play page is opened
        """
        pass

    def test_002_add_a_selection_to_bet_slip_from_an_in_play_event(self):
        """
        DESCRIPTION: Add a selection to bet slip from an in Play event
        EXPECTED: Selection is added to betslip
        """
        pass

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        pass

    def test_004_add_a_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a stake and click on "Place Bet" button
        EXPECTED: * The bet is successfully placed and bet receipt is displayed.
        EXPECTED: * The currency is in £  (or another due to customer currency set while registration)
        """
        pass

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: - The currency is in £  (or another due to customer currency set while registration)
        EXPECTED: - The bet type is displayed: (e.g: single);
        EXPECTED: - Same Selection and Market is displayed where the bet was placed;
        EXPECTED: - Correct Time (of bet placement) and Event is displayed;
        EXPECTED: - 'Cashout' label between the bet and stake info area (if cashout is available for this event)
        EXPECTED: - Unique Bet ID is displayed;
        EXPECTED: - The balance is correctly updated;
        EXPECTED: - Odds are exactly the same as when bet has been placed;
        EXPECTED: - 'Stake' is correctly displayed;
        EXPECTED: - 'Total Stake' is correctly displayed;
        EXPECTED: - 'Estimated Returns' is exactly the same as when bet has been placed;
        EXPECTED: - "Reuse Selection" and "Go Betting" buttons are displayed at the bottom of Bet receipt
        """
        pass

    def test_006_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on 'Go betting' button
        EXPECTED: In Play page loads
        """
        pass

    def test_007_click_on_my_bets_button_from_the_header_mobileclick_on_my_bets_tab_betslip_element___desktop(self):
        """
        DESCRIPTION: Click on 'My Bets' button from the header (mobile)
        DESCRIPTION: Click on 'My Bets' tab (Betslip element - desktop)
        EXPECTED: Cashout/Open Bets page is opened
        """
        pass

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet fields are correct.
        EXPECTED: - The currency is in £ (or another due to customer currency set while registration)
        EXPECTED: - The bet type (eg. Single)
        EXPECTED: - Selection Name where the bet has been placed
        EXPECTED: - Odds are the same as while placing the bet
        EXPECTED: - Market where the bet has been placed
        EXPECTED: - Event Name is displayed
        EXPECTED: - Time and Date (except live events)
        EXPECTED: - Correct Stake is correctly displayed;
        """
        pass
