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
class Test_C874315_Place_Horse_Racing_EW_Treble_bet(Common):
    """
    TR_ID: C874315
    NAME: Place Horse Racing EW Treble bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Multiple E/W bet on Horse Racing
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    DESCRIPTION: AUTOTEST [C48975614]
    PRECONDITIONS: Steps:
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in with user
    PRECONDITIONS: - Navigate to Horse Racing Page
    """
    keep_browser_open = True

    def test_001_add_3_horse_racing_selections_to_betslip_from_different_events_eg_from_the_next_races_module_coralnext_races_tab_ladbrokes(self):
        """
        DESCRIPTION: Add 3 Horse racing selections to Betslip from different events (e.g. from the "NEXT RACES" module (**CORAL**)/"NEXT RACES" tab (**LADBROKES**))
        EXPECTED: The selections are added to Betslip
        """
        pass

    def test_002_add_a_stake_eg_1_to_the_treble_acca_tick_the_each_way_checkbox_and_then_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£) to the Treble ACCA, tick the "Each Way" checkbox and then click on "PLACE BET" button
        EXPECTED: The bet is successfully placed
        """
        pass

    def test_003_verify_the_bet_confirmation_eg_bet_receipt_details(self):
        """
        DESCRIPTION: Verify the Bet Confirmation (e.g. bet receipt details)
        EXPECTED: Correct information is displayed in bet receipt:
        EXPECTED: - sign ![](index.php?/attachments/get/53866838)
        EXPECTED: with text 'Bet Placed Successfully' at the left side and date/time when the bet was placed at the right side
        EXPECTED: - 'Your Bets: (1)' text
        EXPECTED: - Bet Type ('Treble (X2)')
        EXPECTED: - Bet ID
        EXPECTED: - Selections name
        EXPECTED: - Markets name
        EXPECTED: - Events name
        EXPECTED: - Each Way conditions
        EXPECTED: - 'X Lines at £X.XX per line' text
        EXPECTED: - 'Cash Out' label (if available)
        EXPECTED: - Stake
        EXPECTED: - Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: - Total Stake
        EXPECTED: - Estimated Returns (CORAL)/Total Potential Returns(LADBROKES)
        EXPECTED: - 'REUSE SELECTIONS' and 'GO BETTING' buttons
        EXPECTED: - Currency is correct
        EXPECTED: - The balance is correctly updated
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/53866871)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/53866872)
        """
        pass

    def test_004_click_on_the_go_betting_button(self):
        """
        DESCRIPTION: Click on the 'GO BETTING' button
        EXPECTED: The customer is redirected to Horse Racing Page
        """
        pass

    def test_005_click_on_my_bets_button_from_the_header_coral_my_account__my_bets_ladbrokes(self):
        """
        DESCRIPTION: Click on
        DESCRIPTION: -'My Bets' button from the header (**CORAL**)
        DESCRIPTION: -'My Account'-> 'My Bets' (**LADBROKES**)
        EXPECTED: My Bets page is opened
        """
        pass

    def test_006_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: Correct information is displayed in bet history:
        EXPECTED: - Bet Type (TREBLE(EACH WAY))
        EXPECTED: - Selections name with odds (@1/4)
        EXPECTED: - Markets name
        EXPECTED: - Each Way conditions
        EXPECTED: - Event name and event off time
        EXPECTED: - Event time and date
        EXPECTED: - 'WATCH LIVE' (**CORAL**)/'WATCH' (**LADBROKES**) label (if available)
        EXPECTED: - Sign that redirects to the event detail page ![](index.php?/attachments/get/53866895)
        EXPECTED: - Unit Stake
        EXPECTED: - Total Stake
        EXPECTED: - Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/53866943)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/53866945)
        """
        pass

    def test_007_click_on_user_menu___logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        pass
