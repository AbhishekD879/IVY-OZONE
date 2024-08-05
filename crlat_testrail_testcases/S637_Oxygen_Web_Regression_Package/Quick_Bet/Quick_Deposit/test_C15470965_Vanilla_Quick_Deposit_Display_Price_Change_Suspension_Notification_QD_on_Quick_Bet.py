import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C15470965_Vanilla_Quick_Deposit_Display_Price_Change_Suspension_Notification_QD_on_Quick_Bet(Common):
    """
    TR_ID: C15470965
    NAME: [Vanilla] :: Quick Deposit: Display Price Change/Suspension Notification (QD on Quick Bet)
    DESCRIPTION: This test case verifies Price Change Notifications and Event Suspension on Quick Bet pop-up;
    PRECONDITIONS: Link to backoffice tool for event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Login into the app with User that has a positive balance;
    PRECONDITIONS: The test event was created in Openbet and opened in a separate browser tab;
    PRECONDITIONS: The test event details were opened in the Oxygen application so User can see test markets for price change and suspension;
    """
    keep_browser_open = True

    def test_001__add__selection_to_the_quick_bet(self):
        """
        DESCRIPTION: * Add  selection to the Quick Bet;
        EXPECTED: * Selection is added;
        """
        pass

    def test_002__make_a_stake_that_is_less_than_user_balance__stake__user_balance__check_that_place_bet__button_is_active(self):
        """
        DESCRIPTION: * Make a stake that is less than User balance _(stake < User balance)_;
        DESCRIPTION: * Check that **'Place Bet'**  button is active;
        EXPECTED: * __'Place Bet'__ button is activated (changed color from greyed out to green);
        """
        pass

    def test_003__make_stake_bigger_than_user_balance__stake__user_balance__check_that_place_bet__button_is_changed_to_make_a_deposit_button(self):
        """
        DESCRIPTION: * Make Stake bigger than User balance _(stake > User balance)_;
        DESCRIPTION: * Check that **'Place Bet'**  button is changed to **'Make a Deposit'** button;
        EXPECTED: * __'Place Bet'__ button is changed to __'Make a Deposit'__ after rising stake to bigger than User balance;
        """
        pass

    def test_004__click_on___make_a_deposit___button(self):
        """
        DESCRIPTION: * Click on __'Make a Deposit'__ button;
        EXPECTED: * __'Quick Deposit'__ iFrame overlay is displayed with available payment methods set for User;
        """
        pass

    def test_005__observe_the_qd_overlay_and_select_the_desired_payment_method_enter_secure_id(self):
        """
        DESCRIPTION: * Observe the QD overlay and select the desired payment method;
        DESCRIPTION: * Enter Secure ID
        EXPECTED: * Payment method is selected;
        EXPECTED: * Sum for Quick Deposit is calculated;
        EXPECTED: * 'Deposit & Place Bet' button is highlighted in green;
        """
        pass

    def test_006__in_ti_trigger_price_change_for_a_selection__while_the_bet_is_being_processed(self):
        """
        DESCRIPTION: * In TI: Trigger price change for a selection  while the bet is being processed;
        EXPECTED: * Price is changed for a selection;
        """
        pass

    def test_007__navigate_to_app_and_check_if_price_change_notification_is_triggered(self):
        """
        DESCRIPTION: * Navigate to App and check if "Price Change" notification is triggered
        EXPECTED: * The ___"Price change from * to *"___  message is displayed above the Quick Deposit overlay header.
        """
        pass

    def test_008__observe_the__quick_deposit_iframe_content(self):
        """
        DESCRIPTION: * Observe the  "Quick Deposit" iFrame content;
        EXPECTED: * Payment method is displayed;
        EXPECTED: * CTA button is changed  to __'Accept (Deposit and Place Bet)'__ instead of  __'Deposit and Place Bet'__
        """
        pass

    def test_009_navigate_to_the_event_in_ti_and_perform_suspension_for_this_event_and_save_changes_eventstatuscodes(self):
        """
        DESCRIPTION: Navigate to the event in TI and perform "Suspension" for this event and 'Save' changes;
        DESCRIPTION: * "eventStatusCode="S""
        EXPECTED: Event changes are saved in TI;
        """
        pass

    def test_010_navigate_to_the_application_and_observe_event_page(self):
        """
        DESCRIPTION: Navigate to the Application and observe event page;
        EXPECTED: * Previous message  ___"Price change from * to *"___ is disappeared;
        EXPECTED: * The event suspension message ___'‘Your event has been suspended’'___ is displayed above the Quick Deposit overlay header and replaced "Price change" message;
        EXPECTED: * 'Accept (Deposit and Place Bet)' button becomes disabled
        """
        pass

    def test_011_make_the_event_active_againeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: eventStatusCode="A"
        EXPECTED: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Previous message  ___"Price change from * to *"___ is shown
        EXPECTED: The event suspension message ‘Your event has been suspended' disappears
        EXPECTED: 'Accept (Deposit and Place Bet)' button becomes enabled
        """
        pass
