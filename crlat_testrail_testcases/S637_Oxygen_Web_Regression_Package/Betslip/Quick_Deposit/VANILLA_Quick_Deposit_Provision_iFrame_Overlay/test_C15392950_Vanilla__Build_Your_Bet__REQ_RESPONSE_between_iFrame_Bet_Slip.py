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
class Test_C15392950_Vanilla__Build_Your_Bet__REQ_RESPONSE_between_iFrame_Bet_Slip(Common):
    """
    TR_ID: C15392950
    NAME: [Vanilla] - Build Your Bet -  REQ/RESPONSE between iFrame & Bet Slip
    DESCRIPTION: OXYGEN Bet Slip Component & the iFrame to handle various events during the QD process - Build Your Bet area.
    DESCRIPTION: Acceptance criteria:
    DESCRIPTION: * The difference amount i.e. stake - balance shall be sent via the iframe so that the GVC QD can pre-populate this amount.
    DESCRIPTION: * The Total Stake & Potential Return values shall be sent via the iframe so that these values are displayed on the GVC QD.
    DESCRIPTION: * Price Change & Event suspension notifications shall be sent via the iframe so that the GVC QD can display appropriate messages on the confirmation button.
    DESCRIPTION: * iFrame - height to be sent on every resize event, so that the content within the iframe is displayed proportionally.
    DESCRIPTION: Note:
    DESCRIPTION: * Please refer to the story - VANO-138 for QD functional requirements.
    DESCRIPTION: Autotest: [C31542973]
    PRECONDITIONS: 1. Login into the app with User that has a positive balance;
    PRECONDITIONS: 2. The test event was created in Openbet and opened in a separate browser tab;
    PRECONDITIONS: 3. The test event details were opened in the Oxygen application so User can see test markets for price change and suspension;
    PRECONDITIONS: 4. Navigate to event details page > Build your bet tab
    """
    keep_browser_open = True

    def test_001__add_2_selection_to_the_betslip_from_below_build_your_bet_tab(self):
        """
        DESCRIPTION: * Add 2 selection to the betslip from below Build your bet tab
        EXPECTED: * Selection are added;
        EXPECTED: A tab with selections appears with a "Place Bet" button
        """
        pass

    def test_002__tap_on_place_bet_button(self):
        """
        DESCRIPTION: * Tap on "Place Bet" button
        EXPECTED: *Betslip is opened at the bottom of page (UI is similar to quick bet);
        """
        pass

    def test_003__enter_stake_that_exceeds_over_the_balance__eg___155_usdeugbp(self):
        """
        DESCRIPTION: * Enter Stake that exceeds over the balance  (e.g. - 155 USD/EU/GBP);
        EXPECTED: * 'Place bet' button is changed to "Make a Deposit";
        """
        pass

    def test_004__click_on_make_a_deposit(self):
        """
        DESCRIPTION: * Click on 'Make a Deposit";
        EXPECTED: * QD GVC Overlay is displayed with all available payment methods for User;
        """
        pass

    def test_005__select_any_desired_payment_method(self):
        """
        DESCRIPTION: * Select any desired payment method;
        EXPECTED: * Payment method is selected;
        """
        pass

    def test_006_check_the_url_which_is_sent_as_initial_url_params_to_the_iframe(self):
        """
        DESCRIPTION: Check the URL which is sent as initial url params to the iframe
        EXPECTED: URL is:
        EXPECTED: https://cashier.coral.co.uk/cashierapp/cashier.html?userId=[username]&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=[session_key]]&stake=[stake_amount]&estimatedReturn=[estimated_returns_amount]
        EXPECTED: (e.g. - https://cashier.coral.co.uk/cashierapp/cashier.html?userId=cl_testgvccl-API4&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=0600d4bcc1bd40dc875734924d94fb0e&stake=3000&estimatedReturn=75#/)
        EXPECTED: * Contains Stake;
        EXPECTED: * Contains Estimated returns;
        """
        pass

    def test_007_observe_amount_field_in_the_qd_iframe(self):
        """
        DESCRIPTION: Observe "Amount" field in the QD iFrame;
        EXPECTED: The difference between the amount of stake and ballance should be prepopulated on the Payment page;
        """
        pass

    def test_008_observe_the_qd_iframe_for_the_total_stake__potential_return_values_presence(self):
        """
        DESCRIPTION: Observe the QD iFrame for The Total Stake & Potential Return values presence;
        EXPECTED: The Total Stake & Potential Return values are displayed on the GVC QD.
        """
        pass

    def test_009_change_the_stake_decrease_or_increase_for_chosen_selection(self):
        """
        DESCRIPTION: Change the stake (decrease or increase) for chosen selection;
        EXPECTED: Estimated Returns are recalculated and redisplayed on QD iFrame:
        EXPECTED: * Initial URL with parameters was resent;
        EXPECTED: * Values recalculated;
        """
        pass

    def test_010_check_that_iframe_can_be_resizable_enabledisable_embedded_keyboard(self):
        """
        DESCRIPTION: Check that iFrame can be resizable:
        DESCRIPTION: * Enable/Disable embedded keyboard
        EXPECTED: QD iFrame height is changed for every resize event;
        """
        pass

    def test_011_click_on_deposit_and_place_bet(self):
        """
        DESCRIPTION: Click on 'Deposit and Place Bet'
        EXPECTED: * Quick Deposit iFrame is closed
        EXPECTED: * User balance is refilled with a diff (balance stake);
        EXPECTED: * Bet is placed automatically;
        EXPECTED: * Betslip receipt is displayed;
        """
        pass
