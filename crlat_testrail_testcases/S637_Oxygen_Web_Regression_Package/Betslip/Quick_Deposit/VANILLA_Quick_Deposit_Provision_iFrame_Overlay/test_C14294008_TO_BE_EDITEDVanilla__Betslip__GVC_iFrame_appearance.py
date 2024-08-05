import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C14294008_TO_BE_EDITEDVanilla__Betslip__GVC_iFrame_appearance(Common):
    """
    TR_ID: C14294008
    NAME: [TO BE EDITED][Vanilla] - Betslip - GVC iFrame appearance
    DESCRIPTION: This TC will check the appearance of GVC iFrame
    PRECONDITIONS: * User logged in App
    PRECONDITIONS: * **NOTE** Netteller is NOT supported anymore - check this case with other card ( User has payment method set (for Vanilla use  Netteller Card:  Account ID: Any 12 Digit Number, Secure / Authentication Code: Any 6 Digit Number);
    PRECONDITIONS: * User has balance that is > 0
    """
    keep_browser_open = True

    def test_001_select_any_desired_event(self):
        """
        DESCRIPTION: Select any desired event;
        EXPECTED: 
        """
        pass

    def test_002_add_1_selection_to_the_betslip_click_on_add_to_the_betslip_on_quick_bet_pop_up_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Add 1 selection to the betslip (click on 'Add to the Betslip' on "Quick Bet" pop up if accessing from mobile);
        EXPECTED: Selection is added;
        """
        pass

    def test_003_navigate_to_betslip_view_via_a_click_on_betslip_button_in_vanilla_header(self):
        """
        DESCRIPTION: Navigate to Betslip view (via a click on 'Betslip' button in Vanilla Header);
        EXPECTED: Betslip is opened;
        """
        pass

    def test_004_make_a_stake_that_is_less_than_user_balance__stake__user_balance_check_that_place_bet__button_is_active(self):
        """
        DESCRIPTION: Make a stake that is less than User balance _(stake < User balance)_;
        DESCRIPTION: Check that 'Place Bet'  button is active;
        EXPECTED: 'Place Bet' button is activated (changed color from greyed out to green);
        """
        pass

    def test_005_make_stake_bigger_than_user_balance__stake__user_balance_check_that_place_bet__button_is_changed_to_make_a_deposit_button(self):
        """
        DESCRIPTION: Make Stake bigger than User balance _(stake > User balance)_;
        DESCRIPTION: Check that 'Place Bet'  button is changed to 'Make a Deposit' button;
        EXPECTED: * __'Place Bet'__ button is changed to 'Make a Deposit' after rising stake to bigger than User balance;
        """
        pass

    def test_006_tap_on_make_a_deposit_buttonobserve_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button;
        DESCRIPTION: Observe 'Make a Deposit' button
        EXPECTED: Spinner and 'Make a Deposit' text is displayed on the 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay appears with available payment methods set for User;
        """
        pass

    def test_007_add_one_more_selection_to_the_betslip_from_step_1(self):
        """
        DESCRIPTION: Add One more selection to the betslip from step 1;
        EXPECTED: One more selection is added and betslip contains 2 selections;
        """
        pass

    def test_008_place_a_stake_that_is__bigger_than_user_balance_amount_stake__user_balancecheck_that_that_quick_deposit_overlay_is_displayed_for_betslip_with_several_selections(self):
        """
        DESCRIPTION: Place a stake that is  bigger than User balance amount (stake > User balance);
        DESCRIPTION: Check that that 'Quick Deposit' overlay is displayed for betslip with several selections;
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment methods set for User;
        """
        pass

    def test_009_check_that_quick_deposit_overlay_can_be_closed_via_x_button(self):
        """
        DESCRIPTION: Check that 'Quick Deposit' overlay can be closed via 'X' button;
        EXPECTED: Overlay is closed and User can see previously opened betslip;
        """
        pass

    def test_010_check_that_betslip_contains_all_previously_added_selections_after_closing_the_quick_deposit_overlay__the_warning_message_displayed(self):
        """
        DESCRIPTION: Check that betslip contains all previously added selections after closing the "Quick Deposit" overlay & the warning message displayed.
        EXPECTED: All selections are present in the opened betslip & the warning message displayed;
        """
        pass

    def test_011_check_that_iframe_overlay_is_resizablenavigate_to_deposit_amount_field_on_quick_deposit_overlayclick_on_deposit_amount_fieldcheck_that_digital_keyboard_is_displayed_only_for_mobile_tablet(self):
        """
        DESCRIPTION: Check that iFrame Overlay is resizable:
        DESCRIPTION: Navigate to "Deposit Amount" field on "Quick Deposit" overlay;
        DESCRIPTION: Click on "Deposit Amount" field;
        DESCRIPTION: Check that Digital keyboard is displayed (only for mobile, tablet);
        EXPECTED: Keyboard is displayed;
        EXPECTED: Overlay is resized after Keyboard appeared;
        EXPECTED: No scrollbars were displayed; (for small screens on Android scrollbar is displayed)
        """
        pass
