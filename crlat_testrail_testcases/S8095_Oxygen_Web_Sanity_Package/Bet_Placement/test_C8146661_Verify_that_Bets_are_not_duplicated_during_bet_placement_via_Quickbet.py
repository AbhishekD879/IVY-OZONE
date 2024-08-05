import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C8146661_Verify_that_Bets_are_not_duplicated_during_bet_placement_via_Quickbet(Common):
    """
    TR_ID: C8146661
    NAME: Verify that Bets are not duplicated during bet placement via Quickbet
    DESCRIPTION: This test case verifies that Bets are not duplicated during bet placement via Quickbet.
    DESCRIPTION: Before the issue was fixed bet was doubled if to trigger any error message in Quick Bet and to close it without bet placement.
    DESCRIPTION: If to trigger 3/4/5 messages and to close Quickbet after each of them was triggered and to place bet successfully after this - bet was x3/x4/x5 appropriately.
    DESCRIPTION: AUTOTEST [C51748958] - cannot trigger price change on prod (tst2 only)
    PRECONDITIONS: 1. User is logged in to app with positive balance
    PRECONDITIONS: 2. User added selection to the Quickbet
    PRECONDITIONS: 3. To verify info in WS please use request url: wss://remotebetslip-XXX.coralsports.prod.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket where XXX - specifies environment that is used for testing
    """
    keep_browser_open = True

    def test_001_trigger_a_price_change_for_the_selection_in_quickbet(self):
        """
        DESCRIPTION: Trigger a price change for the selection in QuickBet
        EXPECTED: * The updated price is received in WS
        EXPECTED: * The message is displayed in Quickbet
        EXPECTED: ![](index.php?/attachments/get/58771163) ![](index.php?/attachments/get/59323425)
        """
        pass

    def test_002_click_on_the_x_button_to_close_quickbet(self):
        """
        DESCRIPTION: Click on the 'X' button to close QuickBet
        EXPECTED: The Quickbet is closed
        """
        pass

    def test_003_add_any_selection_to_quickbet(self):
        """
        DESCRIPTION: Add any selection to Quickbet
        EXPECTED: The selection is added to QuickBet and received in WS
        """
        pass

    def test_004_enter_any_stake(self):
        """
        DESCRIPTION: Enter any stake
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', * 'Potential Returns' - Ladbrokes are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note The keyboard doesn't appear when using 'Quick Stake' buttons
        """
        pass

    def test_005_click_on_the_place_bet_button(self):
        """
        DESCRIPTION: Click on the 'Place bet' button
        EXPECTED: The bet is placed successfully
        """
        pass

    def test_006_verify_the_number_of_placebet_requests_in_ws(self):
        """
        DESCRIPTION: Verify the number of PlaceBet requests in WS
        EXPECTED: Only ONE PlaceBet request is sent in WS (30011)
        EXPECTED: ![](index.php?/attachments/get/58771188) ![](index.php?/attachments/get/59323428)
        """
        pass

    def test_007_verify_the_bet_receipt_and_the_correct_balance_update(self):
        """
        DESCRIPTION: Verify the bet receipt and the correct balance update
        EXPECTED: * Balance is decreased is equal to the last stake value
        EXPECTED: * Only one bet receipt is received (30012)
        EXPECTED: ![](index.php?/attachments/get/58771189) ![](index.php?/attachments/get/59323429)
        """
        pass

    def test_008_click_on_the_x_button_to_close_quickbet(self):
        """
        DESCRIPTION: Click on the 'X' button to close QuickBet
        EXPECTED: The quickbet is closed
        """
        pass

    def test_009_navigate_to_my_bets___open_betscashout_tabs_to_verify_the_number_of_placed_bets(self):
        """
        DESCRIPTION: Navigate to 'My Bets' -> 'Open Bets'/'Cashout' tabs to verify the number of placed bets
        EXPECTED: Only one placed bet with appropriate stake value and selection details is displayed in Open Bets/Cashout
        """
        pass
