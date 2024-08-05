import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15470947_Vanilla__Quick_Bet__REQ_RESPONSE_between_iFrame_Bet_Slip(Common):
    """
    TR_ID: C15470947
    NAME: [Vanilla] - Quick Bet - REQ/RESPONSE between iFrame & Bet Slip
    DESCRIPTION: OXYGEN Quick Bet Component & the iFrame to handle various events during the QD process.
    DESCRIPTION: [C24281912]
    PRECONDITIONS: * Login into the app with User that has a positive balance;
    """
    keep_browser_open = True

    def test_001__select_any_desired_event_and_tap_on_any_selection(self):
        """
        DESCRIPTION: * Select any desired event and tap on any selection;
        EXPECTED: * Quick Bet pop up is displayed;
        """
        pass

    def test_002_enter_stake_that_exceeds_over_the_balance(self):
        """
        DESCRIPTION: Enter Stake that exceeds over the balance;
        EXPECTED: 'Place bet' button is changed to "Make a Deposit";
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass

    def test_003__click_on_make_a_deposit(self):
        """
        DESCRIPTION: * Click on 'Make a Deposit";
        EXPECTED: * QD GVC Overlay is displayed with all available payment methods for User;
        """
        pass

    def test_004__select_any_desired_payment_method(self):
        """
        DESCRIPTION: * Select any desired payment method;
        EXPECTED: * Payment method is selected;
        """
        pass

    def test_005_observe_amount_field_in_the_qd_iframe(self):
        """
        DESCRIPTION: Observe "Amount" field in the QD iFrame;
        EXPECTED: The difference between the amount of stake and balance should be prepopulated; (if difference between amount of stake and balance is less than 5, the prepopulated amount is 5 - depends on settings on Cashier side)
        """
        pass

    def test_006_observe_the_qd_iframe_for_the_total_stake__estimated_return_values_presence(self):
        """
        DESCRIPTION: Observe the QD iFrame for The Total Stake & Estimated Return values presence;
        EXPECTED: The Total Stake & Estimated Return values are displayed on the GVC QD.
        """
        pass

    def test_007_close_qd_overlay_and_change_the_stake_decrease_or_increase_for_chosen_selectiontap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Close QD overlay and change the stake (decrease or increase) for chosen selection;
        DESCRIPTION: Tap on Make a Deposit button
        EXPECTED: Estimated Returns are recalculated and redisplayed on QD iFrame:
        EXPECTED: * Initial URL with parameters was resent;
        EXPECTED: * Values recalculated;
        """
        pass

    def test_008_check_that_iframe_can_be_resizable_enabledisable_embedded_keyboard(self):
        """
        DESCRIPTION: Check that iFrame can be resizable:
        DESCRIPTION: * Enable/Disable embedded keyboard
        EXPECTED: QD iFrame height is changed for every resize event;
        """
        pass

    def test_009_enter_secure_id_and_click_on_deposit_and_place_bet(self):
        """
        DESCRIPTION: Enter Secure Id and click on 'Deposit and Place Bet'
        EXPECTED: Quick Deposit iFrame is closed
        """
        pass

    def test_010_observe_the_place_bet_button_on_quick_bet(self):
        """
        DESCRIPTION: Observe the 'Place Bet' button on Quick Bet
        EXPECTED: Spinner is displayed on the 'Place Bet' button without text
        EXPECTED: * User balance is refilled with a diff (balance stake);
        EXPECTED: * Bet is placed automatically;
        EXPECTED: * Betslip receipt is displayed;
        """
        pass
