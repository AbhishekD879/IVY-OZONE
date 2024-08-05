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
class Test_C82412_TO_EDITTrader_modifies_the_Price_Type_for_Multiples(Common):
    """
    TR_ID: C82412
    NAME: [TO-EDIT]Trader modifies the Price Type for Multiples
    DESCRIPTION: [TO EDIT] step 6 is outdated
    DESCRIPTION: This test case verifies additional information displaying for any multiple bet that has been modified (price type changed) by the trader.
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Price Type can be changed for Racing selections
    PRECONDITIONS: 4. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    """
    keep_browser_open = True

    def test_001_add_few_selectionsfrom_different_racing_events_to_the_betslip(self):
        """
        DESCRIPTION: Add few selections from different Racing events to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_multiples(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for Multiples
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown: 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' over 'Bet Now' button
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_004_enable_checkbox_present_next_to_selection_with_offer(self):
        """
        DESCRIPTION: Enable checkbox present next to Selection with Offer
        EXPECTED: 'Confirm' button becomes enable automatically
        EXPECTED: **From OX 99**
        EXPECTED: not available
        """
        pass

    def test_005_trigger_price_type_modification_by_trader_and_verify_message_displaying(self):
        """
        DESCRIPTION: Trigger Price Type modification by Trader and verify message displaying
        EXPECTED: *   Info message is displayed over 'Confirm' and 'Cancel' buttons: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_006_verify_new_price_type_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify new Price Type displaying in Betslip
        EXPECTED: * Selection name + @ symbol + Price + Offer + New Price
        EXPECTED: Event Name
        EXPECTED: where Price=old price ( e.g. 'SP')
        EXPECTED: New price = new modified price by Trader highlighted in green/yellow (From OX 99)
        EXPECTED: * Stake remains the same in the stake box
        EXPECTED: **NOTE** currently when price type is changed from SP to LP together with Price Odds, additional info is NOT returned from Openbet and NOT displayed on FE
        """
        pass

    def test_007_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: * The 'Est. return' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        EXPECTED: * The 'Est. return' value is highlighted in green/yellow (From OX 99)
        """
        pass

    def test_008_tap_confirm_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        EXPECTED: The bet is placed as per normal process
        """
        pass

    def test_009_repeat_steps_1_7(self):
        """
        DESCRIPTION: Repeat steps #1-7
        EXPECTED: 
        """
        pass

    def test_010_tap_cancel_button_then_cancel_offer_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button/ then 'Cancel offer' (From OX 99) button
        EXPECTED: * Bet is not placed
        EXPECTED: * Selections are cleaned from betslip
        EXPECTED: * User stays on the previously opened page
        """
        pass
