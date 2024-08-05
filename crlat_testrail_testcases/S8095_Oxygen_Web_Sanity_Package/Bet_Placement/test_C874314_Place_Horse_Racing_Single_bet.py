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
class Test_C874314_Place_Horse_Racing_Single_bet(Common):
    """
    TR_ID: C874314
    NAME: Place Horse Racing Single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on Horse Racing
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    DESCRIPTION: 3 TCs should be created for Mobile - (place bet from QuickBet, redirect to main Betslip from QuickBet, disable QuickBet functionality)
    DESCRIPTION: AUTOTESTS [C46795215]
    PRECONDITIONS: Quick Bet should be deactivated (navigate to 'My Account' Menu -> Settings -> disable "Quick Bet')
    PRECONDITIONS: Steps:
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in with user
    PRECONDITIONS: - Navigate to Horse Racing Page
    """
    keep_browser_open = True

    def test_001_add_a_horse_racing_selection_to_bet_slip_eg_from_the_next_races_module_coralnext_races_tab_ladbrokes(self):
        """
        DESCRIPTION: Add a Horse racing selection to bet slip (e.g. from the "NEXT RACES" module (**CORAL**)/"NEXT RACES" tab (**LADBROKES**))
        EXPECTED: The selection is added to the Betslip
        EXPECTED: The customer is automatically redirected to Betslip (only if bet is added from the "NEXT RACES" tab or module on Homepage or Next Races tab or module on HR page)
        """
        pass

    def test_002_add_a_stake_eg_1_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£), click on "PLACE BET" button
        EXPECTED: The bet is successfully placed
        EXPECTED: The currency is in £.
        """
        pass

    def test_003_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: Correct information is displayed in bet receipt:
        EXPECTED: - sign ![](index.php?/attachments/get/53866970)
        EXPECTED: with text 'Bet Placed Successfully' at the left side and date/time when the bet was placed at the right side
        EXPECTED: - 'Your Bets: (1)' text
        EXPECTED: - Bet Type ('Single')
        EXPECTED: - Odds (@1/2 or @SP)
        EXPECTED: - Bet ID
        EXPECTED: - Selection name
        EXPECTED: - Market name
        EXPECTED: - Event name
        EXPECTED: - 'Cash Out' label (if available)
        EXPECTED: - Stake (**CORAL**)/ Stake for this bet (**LADBROKES**)
        EXPECTED: - Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: - Total Stake
        EXPECTED: - Estimated Returns (**CORAL**)/Total Potential Returns(**LADBROKES**)
        EXPECTED: - 'REUSE SELECTIONS' and 'GO BETTING' buttons
        EXPECTED: - Currency is correct
        EXPECTED: - The balance is correctly updated
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/53866973)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/53866974)
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
        EXPECTED: - Bet Type (SINGLE)
        EXPECTED: - Selection name with odds (@1/4)
        EXPECTED: - Market name
        EXPECTED: - Event name and event off time
        EXPECTED: - Event time and date
        EXPECTED: - 'WATCH LIVE' (**CORAL**)/'WATCH' (**LADBROKES**) label (if available)
        EXPECTED: - Sign that redirects to the event detail page ![](index.php?/attachments/get/53866977)
        EXPECTED: - Stake
        EXPECTED: - Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/53866975)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/53866976)
        """
        pass

    def test_007_click_on_user_menu___logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        pass
