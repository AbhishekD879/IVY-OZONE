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
class Test_C874313_Place_Private_Market_bet(Common):
    """
    TR_ID: C874313
    NAME: Place Private Market bet
    DESCRIPTION: Verify that the customer can see Private Markets and can bet on Private Markets
    DESCRIPTION: AUTOTEST [C50361101] for tst2 envs only due to VOL-2895
    PRECONDITIONS: Make sure that the Private Markets Offer is valid
    PRECONDITIONS: Make sure that the customer is qualified to see the Private Market
    PRECONDITIONS: Login to Oxygen
    PRECONDITIONS: NOTE: Production/HL users: In order to create a user with an available private market, without the need to use OB Prod backoffice, follow guidelines here:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets
    """
    keep_browser_open = True

    def test_001_check_that_the_private_market_is_available_on_homepage(self):
        """
        DESCRIPTION: Check that the Private Market is available on Homepage
        EXPECTED: * The customer can see the Private Market in the first 'Your Enhanced Markets' tab selected by default **For Mobile/Tablet**
        EXPECTED: * The customer can see the Private Market in the first 'Your Enhanced Markets' section at the Homepage **For Desktop**
        """
        pass

    def test_002_add_one_selection_from_the_private_market_to_bet_slip(self):
        """
        DESCRIPTION: Add one selection from the Private Market to bet slip
        EXPECTED: The customer is able to add selection from private market to bet slip
        """
        pass

    def test_003_navigate_to_bet_slip(self):
        """
        DESCRIPTION: Navigate to bet slip
        EXPECTED: The selection was correctly added to bet slip
        """
        pass

    def test_004_add_a_stake_and_click_on_bet_now_button_from_ox_99___place_bet_button(self):
        """
        DESCRIPTION: Add a stake and click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £.
        """
        pass

    def test_005_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        pass

    def test_006_click_on_done_button(self):
        """
        DESCRIPTION: Click on Done button
        EXPECTED: The customer stays on the Homepage
        """
        pass

    def test_007_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: The private market is no longer available
        """
        pass

    def test_008_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: My Bets page is opened
        """
        pass

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: **Bet Receipt unique ID
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: **Correct Stake is correctly displayed;
        """
        pass
