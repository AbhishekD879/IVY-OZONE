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
class Test_C15478417_Vanilla__Betslip__Quick_Deposit_Display_Suspension_Notification_and_Price_Change_Notification_at_the_same_time(Common):
    """
    TR_ID: C15478417
    NAME: [Vanilla] - Betslip - Quick Deposit: Display Suspension Notification and Price Change Notification at the same time
    DESCRIPTION: This test case verifies Suspension Notification and Price Change Notification triggered at the same time on Betslip
    PRECONDITIONS: Link to backoffice tool for price change/event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User balance is more than 0
    """
    keep_browser_open = True

    def test_001_add_1_selection_to_the_betslip_click_on_add_to_the_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Add 1 selection to the betslip (click on 'Add to the Betslip' button on "Quick Bet" pop up if accessing from mobile)
        EXPECTED: Selection is added
        """
        pass

    def test_002_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_003_enter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass

    def test_004_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment method set for User
        """
        pass

    def test_005_change_price_for_the_selection_and_suspend_eventstatuscodes_it_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection and suspend (eventStatusCode="S") it in Backoffice tool
        EXPECTED: Changes are saved
        """
        pass

    def test_006_observe_the_quick_deposit_iframe(self):
        """
        DESCRIPTION: Observe the Quick Deposit iFrame
        EXPECTED: For Coral - The event suspension message 'Please beware one of your selections have been suspended' is displayed above the Quick Deposit overlay header
        EXPECTED: For Ladbrokes - The event suspension message 'One of your selections has been suspended' is displayed in the top and disappears after few minutes
        """
        pass

    def test_007_make_the_event_active_againeventstatuscodea_in_backoffice_tool_and_observe_the_quick_deposit_iframe(self):
        """
        DESCRIPTION: Make the event active again
        DESCRIPTION: (eventStatusCode="A") in Backoffice tool and observe the Quick Deposit iFrame
        EXPECTED: The event suspension message disappears
        EXPECTED: For Coral - 'Some of your prices have changed!' message is displayed above the selection
        EXPECTED: For Ladbrokes - 'Price Changed from * to *' message is displayed above the selection
        """
        pass
