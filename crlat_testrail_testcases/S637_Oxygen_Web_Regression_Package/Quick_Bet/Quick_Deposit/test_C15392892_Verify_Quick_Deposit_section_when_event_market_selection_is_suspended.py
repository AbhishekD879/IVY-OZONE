import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C15392892_Verify_Quick_Deposit_section_when_event_market_selection_is_suspended(Common):
    """
    TR_ID: C15392892
    NAME: Verify Quick Deposit section when event/market/selection is suspended
    DESCRIPTION: This test case verifies Quick Deposit section when event/market/selection is suspended
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. In order to check response open Dev Tools -> select Network -> WS -> Frames section
    PRECONDITIONS: 4. Load app and log in with user has at list one cards added to his account: Visa, Visa Electron, Master Card or Maestro
    PRECONDITIONS: 5. Add selection to Quick Bet
    PRECONDITIONS: 6. Open OpenBet TI tool for updates:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: * Buttons 'ADD TO BETSLIP' and 'MAKE A DEPOSIT' are enabled
        """
        pass

    def test_002_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT'
        EXPECTED: * Quick Deposit section is displayed
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'Deposit & Place Bet' immediately
        """
        pass

    def test_003_suspend_added_selection_in_openbet_ti_tool_and_save_changes(self):
        """
        DESCRIPTION: Suspend added selection in Openbet TI tool and save changes
        EXPECTED: 
        """
        pass

    def test_004_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: * Live update is received in WS
        EXPECTED: * 'Your selection has been suspended' warning message is displayed above Quick Deposit (yellow) background for Coral; cyan background for Ladbrokes)
        EXPECTED: * 'Deposit & Place Bet' button becomes disabled
        """
        pass

    def test_005_unsuspend_added_selection_in_openbet_ti_tool_and_save_changes(self):
        """
        DESCRIPTION: Unsuspend added selection in Openbet TI tool and save changes
        EXPECTED: 
        """
        pass

    def test_006_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: * Live update is received in WS
        EXPECTED: * 'Your selection has been suspended' warning message disappears
        EXPECTED: * 'Deposit' button becomes 'Deposit & Place Bet' immediately
        """
        pass

    def test_007_repeat_steps_3_6_for_market_level_suspension(self):
        """
        DESCRIPTION: Repeat steps #3-6 for market level suspension
        EXPECTED: Expected results are the same except a warning message, for the market level, it should be: 'Your market has been suspended'
        EXPECTED: (yellow background for Coral; cyan background for Ladbrokes)
        """
        pass

    def test_008_repeat_steps_3_6_for_event_level_suspension(self):
        """
        DESCRIPTION: Repeat steps #3-6 for event level suspension
        EXPECTED: Expected results are the same except a warning message, for the event level, it should be: 'Your event has been suspended'
        EXPECTED: (yellow background for Coral; cyan background for Ladbrokes)
        """
        pass
