import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C874316_Place_Horse_Racing_Virtual_bet_SIS(Common):
    """
    TR_ID: C874316
    NAME: Place Horse Racing Virtual bet SIS
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on Horse Racing Virtual event ( all Virtual Horse Racing event from Horse Racing page are provided by SIS)
    DESCRIPTION: AUTOTEST [C9770826]
    PRECONDITIONS: Login to Oxygen app (user with GBP currency)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: **to be verified manually
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing page
        EXPECTED: The Horse Racing page is loaded
        """
        pass

    def test_002_scroll_down_to_virtual_section_and_open_one_event(self):
        """
        DESCRIPTION: Scroll down to Virtual section and open one event
        EXPECTED: The event page is loaded
        """
        pass

    def test_003_add_a_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add a selection to bet slip
        EXPECTED: The selection is added to bet slip
        """
        pass

    def test_004_navigate_to_bet_slip(self):
        """
        DESCRIPTION: Navigate to bet slip
        EXPECTED: Bet slip is loaded
        """
        pass

    def test_005_add_a_stake_and_place_the_bet(self):
        """
        DESCRIPTION: Add a stake and place the bet
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £.
        """
        pass

    def test_006_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: The bet type is displayed: (Singles);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: 'Cashout' label between the bet and Bet ID (if cashout is available for this event)
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: Odds are exactly the same as when bet has been placed;
        EXPECTED: Stake is correctly displayed;
        EXPECTED: Total Stake is correctly displayed;
        EXPECTED: Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Go betting" buttons are displayed.
        """
        pass

    def test_007_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on "Go betting" button
        EXPECTED: The customer is redirected to Horse Racing page
        """
        pass

    def test_008_click_on_my_bets_button_from_the_header_and_select_open_bets_tab(self):
        """
        DESCRIPTION: Click on My Bets button from the header and select "Open Bets" tab
        EXPECTED: My Bets page is opened
        """
        pass

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: Time and Date
        EXPECTED: Market where the bet has been placed
        EXPECTED: E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: Correct Stake is correctly displayed;
        EXPECTED: Total Stake is correctly displayed (for E/W);
        """
        pass
