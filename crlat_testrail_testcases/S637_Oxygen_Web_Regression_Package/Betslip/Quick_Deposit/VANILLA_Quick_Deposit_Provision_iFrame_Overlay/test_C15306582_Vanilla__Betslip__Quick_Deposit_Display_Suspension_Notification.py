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
class Test_C15306582_Vanilla__Betslip__Quick_Deposit_Display_Suspension_Notification(Common):
    """
    TR_ID: C15306582
    NAME: [Vanilla] - Betslip - Quick Deposit: Display Suspension Notification
    DESCRIPTION: This test case verifies suspension notification above the Quick Deposit iframe on Betslip
    PRECONDITIONS: Link to backoffice tool for event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_1_selection_to_the_betslip_click_on_add_to_the_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Add 1 selection to the betslip (click on 'Add to the Betslip' button on "Quick Bet" pop up if accessing from mobile)
        EXPECTED: Selection is added
        """
        pass

    def test_003_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_004_enter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass

    def test_005_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment method set for User
        EXPECTED: 'Deposit&Place Bet' button is enabled
        """
        pass

    def test_006_fill_in_cvv2_fieldtrigger_the_following_situation_in_backoffice_tool_for_this_eventeventstatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Fill in CVV2 field
        DESCRIPTION: Trigger the following situation in Backoffice tool for this event:
        DESCRIPTION: eventStatusCode="S"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: For Coral - The event suspension message 'Please beware one of your selections have been suspended' is displayed above the Quick Deposit overlay header
        EXPECTED: For Ladbrokes - The event suspension message 'One of your selections has been suspended' is displayed in the top and disappears after few minutes
        EXPECTED: 'Deposit&Place Bet' button becomes disabled
        """
        pass

    def test_007_make_the_event_active_againeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: For Coral - The event suspension message 'Please beware one of your selections have been suspended' disappears
        EXPECTED: 'Deposit&Place Bet' button becomes enabled
        """
        pass
