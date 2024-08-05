import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@vtest
class Test_C874321_Place_Lotto_Bet(Common):
    """
    TR_ID: C874321
    NAME: Place Lotto Bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Lotto bet
    DESCRIPTION: AUTOTEST [C47132692]
    PRECONDITIONS: Login to Oxygen app
    PRECONDITIONS: Make sure that there are funds available (if not - top up the account)
    """
    keep_browser_open = True

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to Lotto page
        EXPECTED: Lotto page is loaded
        """
        pass

    def test_002_clicktap_on_a_random_lottery_49s_german_french_etc(self):
        """
        DESCRIPTION: Click/Tap on a random Lottery (49's/ German/ French etc.)
        EXPECTED: Specific Lottery page is displayed.
        """
        pass

    def test_003_click_on_lucky_5_button(self):
        """
        DESCRIPTION: Click on Lucky 5 button
        EXPECTED: 5 Random numbers are selected and displayed to the customer
        """
        pass

    def test_004_add_a_random_stake(self):
        """
        DESCRIPTION: Add a random Stake
        EXPECTED: 1£-10£ - currency sign should be the same as account's currency
        """
        pass

    def test_005_click_on_place_bet_for_xxxx(self):
        """
        DESCRIPTION: Click on "Place Bet for £xx.xx"
        EXPECTED: The button changes it's state form "Place Bet" green button to "Confirm?" orange button
        EXPECTED: Currency sign should be the same as account's currency
        """
        pass

    def test_006_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on "Confirm?" button
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is the same as account's currency.
        """
        pass

    def test_007_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is the same as account's currency.
        EXPECTED: Lottery Name (Draw);
        EXPECTED: Date when the Draw Starts;
        EXPECTED: The bet type is displayed: (e.g: Match 5);
        EXPECTED: Same Selection of numbers is displayed where the bet was placed;
        EXPECTED: Odds are exactly the same as when bet has been placed;
        EXPECTED: Stake is correctly displayed;
        EXPECTED: Total Stake is correctly displayed;
        EXPECTED: Potential Returns is exactly the same as when bet has been placed;
        EXPECTED: Date and time when Bet was placed.
        """
        pass

    def test_008_click_on_done_button(self):
        """
        DESCRIPTION: Click on "Done" button
        EXPECTED: The customer is redirected back to Lotto page
        """
        pass

    def test_009_click_on_my_bets_button_from_the_header_and_navigate_to_open_bets___lotto_page(self):
        """
        DESCRIPTION: Click on My Bets button from the header and navigate to Open Bets -> Lotto page
        EXPECTED: The Lotto page from My Bets -> Open Bets is opened
        """
        pass

    def test_010_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: User's picks : X, x, x, x, x
        EXPECTED: Draw Type : e.g. Monday Draw
        EXPECTED: Draw Date : date of draw
        EXPECTED: Stake: stake value
        EXPECTED: Bet Receipt #
        EXPECTED: Bet placed at : date of lotto bet placement
        """
        pass
