import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.virtual_sports
@vtest
class Test_C874323_Place_VS_Virtual_Horses_bet_Inspired(Common):
    """
    TR_ID: C874323
    NAME: Place VS Virtual Horses bet Inspired
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on a Virtual Sport
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C47866794](https://ladbrokescoral.testrail.com/index.php?/cases/view/47866794)
    DESCRIPTION: Desktop - [C48047421](https://ladbrokescoral.testrail.com/index.php?/cases/view/48047421)
    DESCRIPTION: Note: this test case should be updated for Ladbrokes brand.
    PRECONDITIONS: Login to Oxygen app
    """
    keep_browser_open = True

    def test_001_navigate_to_virtuals_page(self):
        """
        DESCRIPTION: Navigate to Virtuals page
        EXPECTED: The Virtuals page is loaded
        """
        pass

    def test_002_open_virtual_horses(self):
        """
        DESCRIPTION: Open Virtual Horses
        EXPECTED: Virtual Horses page is loaded
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
        """
        pass

    def test_006_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: Unique Bet ID is displayed;
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
        DESCRIPTION: Click on 'Go betting' button
        EXPECTED: The customer is redirected to Virtual sport page (ie: Virtuals Horse Racing)
        """
        pass

    def test_008_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to My Bets page
        EXPECTED: My Bets page is opened
        """
        pass

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: Bet Receipt unique ID
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: Market where the bet has been placed
        EXPECTED: E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: Correct Stake is correctly displayed
        EXPECTED: Total Stake is correctly displayed (for E/W)
        """
        pass
