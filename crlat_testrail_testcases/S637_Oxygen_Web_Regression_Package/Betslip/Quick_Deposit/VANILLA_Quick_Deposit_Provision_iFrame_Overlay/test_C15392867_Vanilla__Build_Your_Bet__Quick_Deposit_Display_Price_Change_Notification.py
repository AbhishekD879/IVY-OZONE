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
class Test_C15392867_Vanilla__Build_Your_Bet__Quick_Deposit_Display_Price_Change_Notification(Common):
    """
    TR_ID: C15392867
    NAME: [Vanilla] - Build Your Bet - Quick Deposit: Display Price Change Notification
    DESCRIPTION: To update: ER in Step 9 - why should amount to deposit change? How can we trigger price change in ByB?
    DESCRIPTION: This TC verifies the appearance of "Price Change" notifications over Quick Deposit overlay - Build Your Bet area.
    DESCRIPTION: Messages should be triggered manually via OpenBet TI.
    PRECONDITIONS: Link to backoffice tool for event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
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
        EXPECTED: * A tab with selections appears with a "Place Bet" button
        """
        pass

    def test_002__tap_on_place_bet_button(self):
        """
        DESCRIPTION: * Tap on "Place Bet" button
        EXPECTED: * Betslip is opened at the bottom of page (UI is similar to quick bet);
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
        EXPECTED: * 'Deposit & Place Bet' button is highlighted in green;
        """
        pass

    def test_007__in_ti_trigger_price_change_for_a_selection_while_the_bet_is_being_processed(self):
        """
        DESCRIPTION: * In TI: Trigger price change for a selection while the bet is being processed;
        EXPECTED: * Price is changed for a selection;
        """
        pass

    def test_008__navigate_to_app_and_check_if_price_change_notification_is_triggered(self):
        """
        DESCRIPTION: * Navigate to App and check if "Price Change" notification is triggered
        EXPECTED: * The ___"Some of your prices have changed!"___  message is displayed above the Quick Deposit overlay header.
        """
        pass

    def test_009__observe_the__quick_deposit_iframe_content(self):
        """
        DESCRIPTION: * Observe the  "Quick Deposit" iFrame content;
        EXPECTED: * Payment method is displayed;
        EXPECTED: * Amount of money needed for deposit is changed;
        EXPECTED: * CTA button is changed  to __'Accept (Deposit & Place Bet)'__ instead of  __'Deposit & Place Bet'__
        """
        pass

    def test_010__click_on_the_button____accept_deposit__place_bet__(self):
        """
        DESCRIPTION: * Click on the button  __'Accept (Deposit & Place Bet)'__
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown to the user with a new price and recalculated Total Est. Returns
        """
        pass
