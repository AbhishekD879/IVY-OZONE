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
class Test_C874311_Place_Football_Double_bet(Common):
    """
    TR_ID: C874311
    NAME: Place Football Double bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Double bet on pre-match Football events
    DESCRIPTION: AUTOTEST [C45158731]
    PRECONDITIONS: Login to Oxygen app with user that has currency in £
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Football page from the menu
        EXPECTED: Football page is loaded
        """
        pass

    def test_002_add_2_selections_to_bet_slip_from_2_different_pre_match_events_not_live_eg_from_matches_tab(self):
        """
        DESCRIPTION: Add 2 selections to bet slip from 2 different pre-match events (not live) e.g. from Matches tab
        EXPECTED: Selections are added to bet slip
        """
        pass

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        pass

    def test_004_add_a_stake_in_the_double_stake_box__and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a stake in the Double Stake box  and click on "Place Bet" button
        EXPECTED: - The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: - The currency is in £ (or other currency set during user registration)
        """
        pass

    def test_005_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: - The currency is in £ (or other currency set during user registration)
        EXPECTED: - The bet type is displayed: DOUBLE;
        EXPECTED: - Same Selection and Market is displayed where the bet was placed;
        EXPECTED: - Event name is displayed;
        EXPECTED: - 'Cashout' label between last bet and stake info area (if cashout is available for both selections)
        EXPECTED: - Unique Bet ID is displayed;
        EXPECTED: - The balance is correctly updated;
        EXPECTED: - Odds are exactly the same as when bet has been placed;
        EXPECTED: - Stake is correctly displayed;
        EXPECTED: - Total Stake is correctly displayed;
        EXPECTED: - Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: - "Reuse Selection" and "Go betting" buttons are displayed at the bottom
        """
        pass

    def test_006_tap_on_go_betting_button(self):
        """
        DESCRIPTION: Tap on 'Go betting' button
        EXPECTED: The customer is redirected back to Football page
        """
        pass

    def test_007_tap_on_my_bets___open_bets_button_from_the_header(self):
        """
        DESCRIPTION: Tap on My Bets -> Open Bets button from the header
        EXPECTED: My Bets page is opened
        """
        pass

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct
        EXPECTED: The currency is in £ (or other user currency)
        EXPECTED: - The bet type: DOUBLE
        EXPECTED: - Selection Names correspond to the placed outcome name
        EXPECTED: - Odds (for 2 selections) are displayed
        EXPECTED: - Event Name is displayed
        EXPECTED: - Market where the bet has been placed
        EXPECTED: - Time and Date - 24 hours format:
        EXPECTED: **HH:MM, Today**  (e.g. "14:00 or 05:00, Today")
        EXPECTED: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov) - future dates
        EXPECTED: - E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: - Stake is correctly displayed;
        """
        pass
