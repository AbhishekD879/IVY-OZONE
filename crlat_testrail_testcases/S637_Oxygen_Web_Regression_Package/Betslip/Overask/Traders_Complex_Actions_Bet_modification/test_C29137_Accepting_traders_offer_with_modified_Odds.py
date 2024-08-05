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
class Test_C29137_Accepting_traders_offer_with_modified_Odds(Common):
    """
    TR_ID: C29137
    NAME: Accepting trader's offer with modified Odds
    DESCRIPTION: This test case verifies accepting trader's offer with modified Odds
    DESCRIPTION: Instruction how modify trader's offer: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    DESCRIPTION: AUTOTEST [C528021]
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004_trigger_odds_modification_by_trader_and_verify_new_odds_value_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Odds modification by Trader and verify new Odds value displaying in Betslip
        EXPECTED: *  Info message is displayed above 'Accept & Bet ([number of accepted bets])'  and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Selection is expanded
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to selection instead of '+'/'-' icon
        EXPECTED: *   The new Odds value is shown in green
        EXPECTED: *   The Estimate returns are updated according to new Odds value (also highlighted in green)
        EXPECTED: *   "You're accepting this Trade Offer" message on the grey background is shown below the selection
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'i'icon is displayed on the left side of the message
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Odds value is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Odds value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31458)
        EXPECTED: ![](index.php?/attachments/get/31459)
        """
        pass

    def test_005_tap_on_accept__bet_number_of_accepted_bets_place_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Accept & Bet ([number of accepted bets])'/ 'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: The bet is placed as per normal process
        """
        pass

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        pass
