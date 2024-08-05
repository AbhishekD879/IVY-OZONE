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
class Test_C22329884_Accepting_split_double_and_single_Races_bets(Common):
    """
    TR_ID: C22329884
    NAME: Accepting split double and single Races bets
    DESCRIPTION: This test case verifies accepting split double and single bets without linked parts
    PRECONDITIONS: * For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: * User is logged in to the application
    """
    keep_browser_open = True

    def test_001_add_2_race_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 2 race selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        pass

    def test_002__enter_stakes_into_double_field_and_into_singles_fields_value_which_is_higher_than_the_maximum_limit_for_added_selections_tap_ew_checkbox_for_1_single_and_multiple_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stakes into Double field and into Singles fields value which is higher than the maximum limit for added selections
        DESCRIPTION: * Tap 'E/W' checkbox for 1 Single and Multiple
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        pass

    def test_003__trigger_bet_split_and_stakeoddsprice_type_modification_by_trader_for_1_single_and_multiple_trigger_leg_type_modification_for_both_bets_from_1_splitted_single_and__for_all_splitted_multiple_from_ewto_win_only(self):
        """
        DESCRIPTION: * Trigger Bet Split and Stake/Odds/Price Type modification by Trader for 1 Single and Multiple
        DESCRIPTION: * Trigger Leg type modification for both bets from 1 splitted Single and  for all splitted Multiple from 'E/W'to 'Win Only'
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Bets are splitted according to design for single and double selections
        EXPECTED: * 'Win Only'is shown for both bets from 1 splitted Single and all splitted Multiple
        EXPECTED: * The changed bets are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_004_tap_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap 'Place bet' or 'Cancel' buttons
        EXPECTED: The bets are placed as per normal process
        """
        pass

    def test_005_repeat_steps_1_4_for_not_enabled_ew_checkbox(self):
        """
        DESCRIPTION: Repeat steps 1-4 for NOT enabled 'E/W' checkbox
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Bets are splitted according to design for single and double selections
        EXPECTED: * 'E/W' is shown for both bets from 1 splitted Singlee and all splitted Multiple
        EXPECTED: * The changed bets are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass
