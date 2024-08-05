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
class Test_C874320_Place_Greyhounds_EW_Single_bet(Common):
    """
    TR_ID: C874320
    NAME: Place Greyhounds EW Single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single E/W bet on Greyhounds
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    DESCRIPTION: AUTOTEST [C47659225]
    PRECONDITIONS: Login to Oxygen
    PRECONDITIONS: **Mobile Only** Quick Bet should be switch off for your user:
    PRECONDITIONS: **CORAL** Account Menu ->Settings ->Betting Settings ->Allow Quick Bet (switch off)
    PRECONDITIONS: **Ladbrokes** Account Menu ->Settings ->Quick Bet (switch off)
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds Page
        EXPECTED: Greyhounds Page is loaded
        """
        pass

    def test_002_click_on_one_event_from_all_races_section(self):
        """
        DESCRIPTION: Click on one event from All Races section
        EXPECTED: The event page is loaded
        """
        pass

    def test_003_add_one_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add one selection to bet slip
        EXPECTED: The selection is added to bet slip
        """
        pass

    def test_004_add_a_stake_eg_1_tick_the_ew_checkbox_and_then_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£), tick the "E/W" checkbox and then click on 'Place Bet' button
        EXPECTED: The bet is successfully placed
        """
        pass

    def test_005_verify_the_bet_confirmation_eg_bet_receipt_details(self):
        """
        DESCRIPTION: Verify the Bet Confirmation (e.g. bet receipt details)
        EXPECTED: Correct information is displayed in bet receipt:
        EXPECTED: - sign ![](index.php?/attachments/get/19830152)
        EXPECTED: with text 'Bet Placed Successfully' at the left side and date/time when the bet was placed at the right side
        EXPECTED: - 'Your Bets: (1)' text
        EXPECTED: - Bet Type ('Single') and odds (@1/4 or @SP)
        EXPECTED: - Bet ID
        EXPECTED: - Selection name
        EXPECTED: - Market name
        EXPECTED: - Event name
        EXPECTED: - Each Way conditions
        EXPECTED: - Stake
        EXPECTED: - Total Stake
        EXPECTED: - Est. Returns (CORAL)/Potential Returns(LADBROKES) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: - 'REUSE SELECTIONS' and 'GO BETTING' buttons
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/19764606)
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/19764607)
        """
        pass

    def test_006_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on 'Go Betting' button
        EXPECTED: The customer is redirected to Greyhounds Page
        """
        pass

    def test_007_click_on_my_bets_button_from_the_header_and_select_open_bets_tab(self):
        """
        DESCRIPTION: Click on My Bets button from the header and select 'Open Bets' tab
        EXPECTED: 
        """
        pass

    def test_008_check_that_the_bet_is_displayed_in_open_bets(self):
        """
        DESCRIPTION: Check that the bet is displayed in 'Open Bets'
        EXPECTED: Correct information is displayed in bet history:
        EXPECTED: - Bet Type (SINGLE(EACH WAY))
        EXPECTED: - Selection name with odds (@1/4)
        EXPECTED: - Market name
        EXPECTED: - Event name and event off time
        EXPECTED: - Event time and date
        EXPECTED: - Sign that redirects to the event detail page ![](index.php?/attachments/get/19830149)
        EXPECTED: - Unit Stake
        EXPECTED: - Total Stake
        EXPECTED: - Est. Returns (CORAL)/Potential Returns(LADBROKES) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/19830151)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/19830150)
        """
        pass
