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
class Test_C15229158_Vanilla__Betslip__Quick_Deposit_Display_Price_Change_Notification(Common):
    """
    TR_ID: C15229158
    NAME: [Vanilla] - Betslip - Quick Deposit: Display Price Change Notification
    DESCRIPTION: This TC verifies the appearance of "Price Change" notification over Quick Deposit overlay. Messages should be triggered manually via OpenBet TI.
    PRECONDITIONS: 1. Login into the app with User that has a positive balance;
    PRECONDITIONS: 2. The test event was created in Openbet and opened in a separate browser tab;
    PRECONDITIONS: 3. The test event details were opened in the Oxygen application so User can see test markets for price change and suspension;
    """
    keep_browser_open = True

    def test_001__add_1_selection_to_the_betslip_click_on_add_to_the_betslip_on_quick_bet_pop_up_if_accessing_from_mobile__using_the__event_created_in_the_preconditions(self):
        """
        DESCRIPTION: * Add 1 selection to the betslip (click on 'Add to the Betslip' on "Quick Bet" pop up if accessing from mobile)  using the  event created in the preconditions;
        EXPECTED: * Selection is added;
        """
        pass

    def test_002__navigate_to_betslip_view_via_a_click_on_betslip_button_in_vanilla_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: * Navigate to Betslip view (via a click on 'Betslip' button in Vanilla Header if accessing from mobile);
        EXPECTED: * Betslip is opened;
        """
        pass

    def test_003__make_a_stake_that_is_less_than_user_balance__stake__user_balance__check_that_place_bet__button_is_active(self):
        """
        DESCRIPTION: * Make a stake that is less than User balance _(stake < User balance)_;
        DESCRIPTION: * Check that **'Place Bet'**  button is active;
        EXPECTED: * __'Place Bet'__ button is activated (changed color from greyed out to green);
        """
        pass

    def test_004__make_stake_bigger_than_user_balance__stake__user_balance__check_that_place_bet__button_is_changed_to_make_a_deposit_button(self):
        """
        DESCRIPTION: * Make Stake bigger than User balance _(stake > User balance)_;
        DESCRIPTION: * Check that **'Place Bet'**  button is changed to **'Make a Deposit'** button;
        EXPECTED: * __'Place Bet'__ button is changed to __'Make a Deposit'__ after rising stake to bigger than User balance;
        EXPECTED: * A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass

    def test_005__click_on___make_a_deposit___button(self):
        """
        DESCRIPTION: * Click on __'Make a Deposit'__ button;
        EXPECTED: * __'Quick Deposit'__ iFrame overlay is displayed with available payment methods set for User;
        """
        pass

    def test_006__observe_the_qd_overlay_and_select_the_desired_payment_method(self):
        """
        DESCRIPTION: * Observe the QD overlay and select the desired payment method;
        EXPECTED: * Payment method is selected;
        EXPECTED: * Sum for Quick Deposit is calculated;
        """
        pass

    def test_007__in_ti_trigger_price_change_for_a_selection__while_the_bet_is_being_processed(self):
        """
        DESCRIPTION: * In TI: Trigger price change for a selection  while the bet is being processed;
        EXPECTED: * Price is changed for a selection;
        """
        pass

    def test_008__navigate_to_app_and_check_if_price_change_notification_is_triggered(self):
        """
        DESCRIPTION: * Navigate to App and check if "Price Change" notification is triggered
        EXPECTED: For Coral * The ___"Some of your prices have changed!"___  message is displayed above the Quick Deposit overlay header
        EXPECTED: For Ladbrokes  * The ___"Some of the prices have changed!"___  message is displayed on the top and disappears after few seconds
        """
        pass

    def test_009__observe_the__quick_deposit_iframe_content(self):
        """
        DESCRIPTION: * Observe the  "Quick Deposit" iFrame content;
        EXPECTED: * Payment method is displayed;
        EXPECTED: * CTA button is changed  to __'Accept (Deposit & Place Bet)'__ instead of  __'Deposit & Place Bet'__
        """
        pass

    def test_010__enter_secure_id_code_click_on_the_button____accept_deposit__place_bet__(self):
        """
        DESCRIPTION: * Enter Secure ID code
        DESCRIPTION: * Click on the button  __'Accept (Deposit & Place Bet)'__
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown to the user with a new price and recalculated Total Est. Returns
        """
        pass
