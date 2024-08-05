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
class Test_C82410_TO_EDITTrader_modifies_the_Price_Odds_for_Multiples(Common):
    """
    TR_ID: C82410
    NAME: [TO EDIT]Trader modifies the Price/Odds for Multiples
    DESCRIPTION: [TO EDIT] - step 5 is outdated for Ladbrokes double bets
    DESCRIPTION: This test case verifies additional information displaying for any multiple bet that has been  price/odds modified  by the trader.
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-16714 Overask Improvement - Show leg offers for mulitples
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    PRECONDITIONS: 4. Price/Odds is displayed for Multiples if **payout.potential**>=2 from 'readBet' response
    """
    keep_browser_open = True

    def test_001_add_few_selections_to_betslip(self):
        """
        DESCRIPTION: Add few selections to betslip
        EXPECTED: Multiples are available in betslip
        """
        pass

    def test_002_enter_stake_value_which_is_higher_than_maximum_limit_for_multiples(self):
        """
        DESCRIPTION: Enter stake value which is higher than maximum limit for Multiples
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

    def test_004_trigger_priceodds_modification_by_trader_and_check_message_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Price/Odds modification by Trader and check message displaying in Betslip
        EXPECTED: * Info message is displayed over 'Confirm' and 'Cancel' buttons: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: **From OX 99**
        EXPECTED: * CMS configurable 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_005_verify_additional_information_displaying_for_multiples(self):
        """
        DESCRIPTION: Verify additional information displaying for multiples
        EXPECTED: * Selection name + @ symbol + Price + Offer + New Price
        EXPECTED: Event Name
        EXPECTED: where Price = old price
        EXPECTED: New price = new modified price by Trader highlighted in green/yellow (From OX 99)
        EXPECTED: * Stake remains the same in the stake box
        """
        pass

    def test_006_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: * The 'Est. return' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        EXPECTED: * The 'Est. return' value is highlighted in green/not highlighted (From OX 99)
        """
        pass

    def test_007_verify_priceodds_value_for_multiple_applicable_to_double_with_1_bet_or_multiple_in_place_your_acca_section_if_available(self):
        """
        DESCRIPTION: Verify 'Price/Odds' value for Multiple (applicable to Double with 1 bet or Multiple in 'Place your ACCA' section) if available
        EXPECTED: * New 'Price/Odds' value is calculated according to formula
        EXPECTED: ** Odds from each Single selections are multiplied and new Odds value is displayed
        EXPECTED: ** Conversion from decimal to fractional odds is according to attached OddsLadder table
        EXPECTED: * New 'Price/Odds' value is equal to **N/A** if one of the single selection contains SP price
        EXPECTED: * New 'Price/Odds' value is highlighted in green
        """
        pass

    def test_008_tap_confirm_buttonplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button/'Place bet' (From OX 99) button
        EXPECTED: The bet is placed as per normal process
        """
        pass

    def test_009_repeat_step_1_7(self):
        """
        DESCRIPTION: Repeat step #1-7
        EXPECTED: 
        """
        pass

    def test_010_tap_cancel_button_then_cancel_offer_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button/ then 'Cancel offer' (From OX 99) button
        EXPECTED: * Bet is not placed
        EXPECTED: * Selections are present in betslip without offer and without entered stake
        EXPECTED: **From OX 99**
        EXPECTED: Betslip is cleared and closed
        """
        pass
