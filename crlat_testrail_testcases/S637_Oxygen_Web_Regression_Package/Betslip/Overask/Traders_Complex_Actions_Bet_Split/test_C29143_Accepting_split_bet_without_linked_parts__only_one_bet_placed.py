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
class Test_C29143_Accepting_split_bet_without_linked_parts__only_one_bet_placed(Common):
    """
    TR_ID: C29143
    NAME: Accepting split bet without linked parts - only one bet placed
    DESCRIPTION: This test case verifies splitting Overask bets without linking its parts
    DESCRIPTION: Instruction how to split Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    DESCRIPTION: AUTOTEST MOBILE [C2515177]
    DESCRIPTION: AUTOTEST DESKTOP [C2536488]
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

    def test_003__tap_bet_now_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: * Tap 'Bet Now' button
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
        EXPECTED: *   Enabled pre-ticked checkboxes are shown next to each selection instead of '-'(expand)/'+'(collapse) icon
        EXPECTED: *   "You're accepting this Trade Offer" message is shown under each part of the selection on the gray background
        EXPECTED: *   'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are displayed enabled
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Splitted parts of the selection are displayed
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons are enabled
        EXPECTED: NEW design:
        EXPECTED: ![](index.php?/attachments/get/33507) ![](index.php?/attachments/get/33508)
        """
        pass

    def test_006_unselect_one_of_bet_partsfrom_ox_99remove_one_of_bet_parts(self):
        """
        DESCRIPTION: Unselect one of Bet parts
        DESCRIPTION: **From OX 99**
        DESCRIPTION: REMOVE one of Bet parts
        EXPECTED: *  'Accept & Bet' button remains enabled
        EXPECTED: **From OX 99**
        EXPECTED: *  Button 'Place Bet' is enabled
        EXPECTED: *  NEW design for remove/undo feature:
        EXPECTED: ![](index.php?/attachments/get/33510) ![](index.php?/attachments/get/33511)
        """
        pass

    def test_007__tap_accept__bet_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: * Tap 'Accept & Bet' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: *   Selected Bet part is placed as per normal process
        EXPECTED: *   The removed selection is not placed
        """
        pass
