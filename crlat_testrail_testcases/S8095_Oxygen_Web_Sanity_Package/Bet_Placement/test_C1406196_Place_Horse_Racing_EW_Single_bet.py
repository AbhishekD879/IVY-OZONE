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
class Test_C1406196_Place_Horse_Racing_EW_Single_bet(Common):
    """
    TR_ID: C1406196
    NAME: Place Horse Racing EW Single bet
    DESCRIPTION: To edit: the description should be consistent with platforms (betplacement should be checked on desktop too, just without QB)
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single E/W bet on Horse Racing
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    DESCRIPTION: 3 TCs should be created - (place bet from QuickBet, redirect to main Betslip from QuickBet, disable QuickBet functionality)
    DESCRIPTION: AUTOTESTS [C53045935]
    PRECONDITIONS: Quick Bet should be deactivated (navigate to Menu -> Settings).
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page from the Menu
        EXPECTED: Navigate to Horse Racing Page from the Menu
        """
        pass

    def test_002_add_a_horse_racing_selection_to_bet_slip_eg_from_the_next_races_widget(self):
        """
        DESCRIPTION: Add a Horse racing selection to bet slip (e.g. from the "NEXT RACES" widget)
        EXPECTED: The selection is added to bet slip
        EXPECTED: The customer is automatically redirected to bet slip
        """
        pass

    def test_003_add_a_stake_eg_1_tick_the_each_way_checkbox_and_then_click_on_bet_now_button_from_ox_99___place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£), tick the "Each Way" checkbox and then click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed
        EXPECTED: The currency is in £.
        """
        pass

    def test_004_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet ID (if cashout is available for this event)
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        pass

    def test_005_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on 'Go betting' button
        EXPECTED: The customer is redirected to Horse Racing Page
        """
        pass

    def test_006_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: My Bets page is opened
        """
        pass

    def test_007_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: **Bet Receipt unique ID (only on settled bets tab )
        EXPECTED: Selection Details:
        EXPECTED: **Selection Name where the bet has been placed
        EXPECTED: **Event name and event off time
        EXPECTED: **Event time and date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms
        EXPECTED: **Correct Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed (for E/W);
        """
        pass

    def test_008_click_on_user_menu___logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        pass
