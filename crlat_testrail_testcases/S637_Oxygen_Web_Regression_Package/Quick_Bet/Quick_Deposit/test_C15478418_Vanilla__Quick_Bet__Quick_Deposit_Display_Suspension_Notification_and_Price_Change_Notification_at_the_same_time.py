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
class Test_C15478418_Vanilla__Quick_Bet__Quick_Deposit_Display_Suspension_Notification_and_Price_Change_Notification_at_the_same_time(Common):
    """
    TR_ID: C15478418
    NAME: [Vanilla] - Quick Bet - Quick Deposit: Display Suspension Notification and Price Change Notification at the same time
    DESCRIPTION: This test case verifies Suspension Notification and Price Change Notification triggered at the same time on Quick Bet
    PRECONDITIONS: Link to backoffice tool for price change/event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User balance is more than 0
    """
    keep_browser_open = True

    def test_001_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_002_change_value_in_stake_field_for_value_higher_than_user_balance(self):
        """
        DESCRIPTION: Change value in 'Stake' field for value higher than user balance
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass

    def test_003_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment method set for User
        """
        pass

    def test_004_change_price_for_the_selection_and_suspend_eventstatuscodes_it_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection and suspend (eventStatusCode="S") it in Backoffice tool
        EXPECTED: Changes are saved
        """
        pass

    def test_005_observe_the_quick_deposit_iframe(self):
        """
        DESCRIPTION: Observe the Quick Deposit iFrame
        EXPECTED: The event suspension message 'Your event has beeb suspended' is displayed above the Quick Deposit overlay header
        """
        pass

    def test_006_make_the_event_active_againeventstatuscodea_in_backoffice_tool_and_observe_the_quick_deposit_iframe(self):
        """
        DESCRIPTION: Make the event active again
        DESCRIPTION: (eventStatusCode="A") in Backoffice tool and observe the Quick Deposit iFrame
        EXPECTED: The event suspension message 'Your event has beeb suspended' disappears
        EXPECTED: 'Price change from * to *' message is displayed
        """
        pass
