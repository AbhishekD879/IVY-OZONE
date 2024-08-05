import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.other
@vtest
class Test_C14835383_Vanilla__Betslip__REQ_RESPONSE_between_iFrame_Bet_Slip(Common):
    """
    TR_ID: C14835383
    NAME: [Vanilla] - Betslip - REQ/RESPONSE between iFrame & Bet Slip
    DESCRIPTION: OXYGEN Bet Slip Component & the iFrame to handle various events during the QD process.
    PRECONDITIONS: 1. User account with at least one available previously added credit card
    PRECONDITIONS: Make sure that user has 3DS Card added to the account https://confluence.egalacoral.com/display/SPI/How+to+create+test+user+for+GVC+Vanilla+automatically+by-passing+KYC
    PRECONDITIONS: 2. User Logged into app with a positive balance;
    """
    keep_browser_open = True

    def test_001__add_one_selection_to_the_betslip_click_on_add_to_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobileopen__betslip_view(self):
        """
        DESCRIPTION: * Add one selection to the Betslip (Click on 'Add to Betslip' button on "Quick Bet" pop up if accessing from mobile)
        DESCRIPTION: Open  Betslip view;
        EXPECTED: Betslip is opened;
        """
        pass

    def test_002__enter_stake_that_exceeds_over_the_balance(self):
        """
        DESCRIPTION: * Enter Stake that exceeds over the balance;
        EXPECTED: * 'Place bet' button is changed to "Make a Deposit";
        EXPECTED: * A warning message is displayed above 'Total Stake':
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

    def test_005__check_the_url_which_is_sent_as_initial_url_params_to_the_iframe(self):
        """
        DESCRIPTION: * Check the URL which is sent as initial url params to the iframe
        EXPECTED: URL is:
        EXPECTED: https://re-coralcashier.ivycomptech.co.in/cashierapp/cashier.html?userId=cl_testuser&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=fdsadsffdsafds&stake=xxxx&estimatedReturn=xxx
        EXPECTED: * Contains Stake;
        EXPECTED: * Contains Estimated returns;
        """
        pass

    def test_006__observe_amount_field_in_the_qd_iframe(self):
        """
        DESCRIPTION: * Observe "Amount" field in the QD iFrame;
        EXPECTED: The difference between the amount of stake and balance should be prepopulated; (if difference between amount of stake and balance is less than 5, prepopulated amount is 5)
        """
        pass

    def test_007__observe_the_qd_iframe_for_the_total_stake__potential_return_values_presence(self):
        """
        DESCRIPTION: * Observe the QD iFrame for The Total Stake & Potential Return values presence;
        EXPECTED: The Total Stake & Potential Return values are displayed on the GVC QD.
        """
        pass

    def test_008__change_the_stake_decrease_or_increase_for_chosen_selectionnotice_hide_qd_overlay_via_inspect_elements(self):
        """
        DESCRIPTION: * Change the stake (decrease or increase) for chosen selection;
        DESCRIPTION: Notice: (Hide QD overlay via Inspect elements);
        EXPECTED: Estimated Returns are recalculated and redisplayed on QD iFrame:
        EXPECTED: * Initial URL with parameters was resent;
        EXPECTED: * Values recalculated;
        """
        pass

    def test_009__check_that_iframe_can_be_resizable_enabledisable_embedded_keyboard(self):
        """
        DESCRIPTION: * Check that iFrame can be resizable:
        DESCRIPTION: * Enable/Disable embedded keyboard
        EXPECTED: QD iFrame height is changed for every resize event;
        """
        pass

    def test_010__click_on_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: * Click on 'Deposit and Place Bet' button
        EXPECTED: Quick Deposit iFrame is closed
        """
        pass

    def test_011__observe_the_place_bet_button_on_betslip(self):
        """
        DESCRIPTION: * Observe the 'Place Bet' button on Betslip
        EXPECTED: Spinner is displayed on the 'Place Bet' button without text
        EXPECTED: * User balance is refilled with a diff (balance stake);
        EXPECTED: * Bet is placed automatically;
        EXPECTED: * Betslip receipt is displayed;
        """
        pass
