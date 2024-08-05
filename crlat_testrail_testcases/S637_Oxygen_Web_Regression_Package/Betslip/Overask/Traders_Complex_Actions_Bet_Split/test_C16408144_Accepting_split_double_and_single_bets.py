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
class Test_C16408144_Accepting_split_double_and_single_bets(Common):
    """
    TR_ID: C16408144
    NAME: Accepting split double and single bets
    DESCRIPTION: This test case verifies accepting split double and single bets without linked parts
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

    def test_002__enter_stakes_into_double_field_and_into_singles_fields_value_which_is_higher_than_the_maximum_limit_for_added_selections_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stakes into Double field and into Singles fields value which is higher than the maximum limit for added selections
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        pass

    def test_003_trigger_bet_split_and_stakeoddsprice_type_modification_by_trader(self):
        """
        DESCRIPTION: Trigger Bet Split and Stake/Odds/Price Type modification by Trader.
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Bets are splitted according to design for single and double selections
        EXPECTED: * The changed bets are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/34021)  ![](index.php?/attachments/get/34022)
        """
        pass

    def test_004_tap_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap 'Place bet' or 'Cancel' buttons
        EXPECTED: The bets are placed as per normal process
        """
        pass
