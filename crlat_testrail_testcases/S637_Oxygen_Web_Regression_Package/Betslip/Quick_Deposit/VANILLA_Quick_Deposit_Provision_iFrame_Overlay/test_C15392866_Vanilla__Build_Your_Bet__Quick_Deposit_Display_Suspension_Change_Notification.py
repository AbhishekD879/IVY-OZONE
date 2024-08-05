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
class Test_C15392866_Vanilla__Build_Your_Bet__Quick_Deposit_Display_Suspension_Change_Notification(Common):
    """
    TR_ID: C15392866
    NAME: [Vanilla] - Build Your Bet - Quick Deposit: Display Suspension Change Notification
    DESCRIPTION: This TC verifies the appearance of suspension notifications over Quick Deposit overlay - Build Your Bet area.
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

    def test_007_trigger_the_following_situation_in_backoffice_tool_for_this_eventeventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation in Backoffice tool for this event:
        DESCRIPTION: eventStatusCode="S"
        EXPECTED: The event suspension message 'Please beware one of your selections have been suspended' is displayed above the Quick Deposit overlay header
        EXPECTED: 'Accept (Deposit&Place Bet)' button becomes disabled
        """
        pass

    def test_008_make_the_event_active_againeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: The event suspension message 'Please beware one of your selections have been suspended' disappears
        EXPECTED: 'Accept (Deposit&Place Bet)' button becomes enabled
        """
        pass
