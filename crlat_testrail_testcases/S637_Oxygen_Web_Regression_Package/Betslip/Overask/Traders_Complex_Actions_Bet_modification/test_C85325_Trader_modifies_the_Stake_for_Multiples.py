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
class Test_C85325_Trader_modifies_the_Stake_for_Multiples(Common):
    """
    TR_ID: C85325
    NAME: Trader modifies the Stake for Multiples
    DESCRIPTION: This test case verifies additional information displaying for any multiple where stake has been modified by the trader.
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    """
    keep_browser_open = True

    def test_001_add_few_selections_to_betslip(self):
        """
        DESCRIPTION: Add few selections to betslip
        EXPECTED: Multiples are available in betslip
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_multiples_for_logged_in_user(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for Multiples for logged in user
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown: 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' over 'Bet Now' button
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_004_trigger_stake_modification_by_trader_and_check_message_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Stake modification by Trader and check message displaying in Betslip
        EXPECTED: * Info message is displayed over 'Confirm' and 'Cancel' buttons: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_005_verify_new_stake_value(self):
        """
        DESCRIPTION: Verify new 'Stake' value
        EXPECTED: * Modified stake displayed in the stake box and highlighted in green/yellow (From OX 99)
        EXPECTED: * Any additional information (Selection name + @ symbol + Price + Offer + New Price Event Name) is NOT displayed in Multiples section
        """
        pass

    def test_006_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: * The 'Est. return' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        """
        pass

    def test_007_tap_confirm_buttonplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button/'Place bet' (From OX 99) button
        EXPECTED: The bet is placed as per normal process
        """
        pass

    def test_008_repeat_step_1_6(self):
        """
        DESCRIPTION: Repeat step #1-6
        EXPECTED: 
        """
        pass

    def test_009_tap_cancel_button_then_cancel_offer_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button/ then 'Cancel offer' (From OX 99) button
        EXPECTED: * Bet is not placed
        EXPECTED: * Selections are cleaned from betslip
        EXPECTED: * User stays on the previously opened page
        """
        pass
