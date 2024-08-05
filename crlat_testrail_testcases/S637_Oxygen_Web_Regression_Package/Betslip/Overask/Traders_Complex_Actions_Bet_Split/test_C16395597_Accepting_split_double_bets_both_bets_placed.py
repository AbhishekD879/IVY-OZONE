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
class Test_C16395597_Accepting_split_double_bets_both_bets_placed(Common):
    """
    TR_ID: C16395597
    NAME: Accepting split double bets- both bets placed
    DESCRIPTION: This test case verifies accepting split double bets without linked parts - both bets placed
    DESCRIPTION: Instruction how to split Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: * For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: * User is logged in to the application
    """
    keep_browser_open = True

    def test_001_add_2_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 2 selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        pass

    def test_002__enter_stake_into_a_double_field_value_which_is_higher_than_the_maximum_limit_for_added_selection_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stake into a 'Double' field value which is higher than the maximum limit for added selection
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_003_trigger_bet_split_and_stakeoddsprice_type_modification_by_trader(self):
        """
        DESCRIPTION: Trigger Bet Split and Stake/Odds/Price Type modification by Trader.
        EXPECTED: 
        """
        pass

    def test_004_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify Bet parts with modified values displaying in Betslip
        EXPECTED: *  'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Splitted parts of the selection are displayed
        EXPECTED: * Only parent part has Remove button (Double(x1), Treble, etc.)
        EXPECTED: * The new values are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons are enabled
        EXPECTED: ![](index.php?/attachments/get/33889) ![](index.php?/attachments/get/33888)
        """
        pass

    def test_005_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap button 'Place Bet'
        EXPECTED: Bet is successfully placed with all selections from the trader's offer
        """
        pass
