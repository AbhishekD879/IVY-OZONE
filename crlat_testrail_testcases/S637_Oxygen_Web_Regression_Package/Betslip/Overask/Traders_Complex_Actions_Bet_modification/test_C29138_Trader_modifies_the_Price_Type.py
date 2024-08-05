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
class Test_C29138_Trader_modifies_the_Price_Type(Common):
    """
    TR_ID: C29138
    NAME: Trader modifies the Price Type
    DESCRIPTION: 
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Price Type can be changed for Racing selections
    """
    keep_browser_open = True

    def test_001_add_selection_from_racing_events_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from Racing events to the Betslip
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

    def test_004_trigger_price_type_modification_by_trader_and_verify_new_price_type_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Price Type modification by Trader and verify new Price Type displaying in Betslip
        EXPECTED: *   Info message is displayed above 'Confirm' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Selection is expanded
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to selection instead of '+'/'-' icon
        EXPECTED: *   The new Price Type is shown to the user on the Betslip (in green)
        EXPECTED: *   The Estimate returns are updated according to new Price Type (also highlighted in green)
        EXPECTED: *   "You're accepting this Trade Offer" message on the grey background is shown below the selection
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Price Type is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Price Type
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31458)
        EXPECTED: ![](index.php?/attachments/get/31459)
        """
        pass

    def test_005_tap_confirm_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        EXPECTED: The bet is placed as per normal process
        """
        pass

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps 3-5
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        pass
