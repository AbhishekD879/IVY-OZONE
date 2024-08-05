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
class Test_C2553176_Accepting_split_bet_without_linked_parts__both_bets_placed(Common):
    """
    TR_ID: C2553176
    NAME: Accepting split bet without linked parts - both bets placed
    DESCRIPTION: This test case verifies splitting Overask bets without linking its parts
    DESCRIPTION: Instruction how to split Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
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

    def test_003_tap_bet_now_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        EXPECTED: **From OX 99**
        EXPECTED: ![](index.php?/attachments/get/33504) ![](index.php?/attachments/get/33505)
        """
        pass

    def test_004_triggerbet_split_and_stakeoddsprice_type_modificationby_trader(self):
        """
        DESCRIPTION: Trigger Bet Split and Stake/Odds/Price Type modification by Trader.
        EXPECTED: 
        """
        pass

    def test_005_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify Bet parts with modified values displaying in Betslip
        EXPECTED: *   The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *   Splitted parts of the selection are expanded
        EXPECTED: *   Enabled pre-ticked check boxes are shown next to each selection instead of '-'(expand)/'+'(collapse) icon
        EXPECTED: *   "You're accepting this Trade Offer" message is shown under each part of the selecion on the gray background
        EXPECTED: *   'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are displayed enabled
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Splitted parts of the selection are displayed
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: NEW design:
        EXPECTED: ![](index.php?/attachments/get/33507) ![](index.php?/attachments/get/33508)
        """
        pass

    def test_006_tap_accept__bet_2_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap 'Accept & Bet (2)' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: Bets are placed as per normal process
        """
        pass

    def test_007_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        EXPECTED: Selections are successfully added
        """
        pass

    def test_008_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps 3-6
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        pass
