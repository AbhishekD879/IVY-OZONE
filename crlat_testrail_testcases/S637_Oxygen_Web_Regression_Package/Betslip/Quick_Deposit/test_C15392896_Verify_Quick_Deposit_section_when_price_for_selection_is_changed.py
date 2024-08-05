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
class Test_C15392896_Verify_Quick_Deposit_section_when_price_for_selection_is_changed(Common):
    """
    TR_ID: C15392896
    NAME: Verify Quick Deposit section when price for selection is changed
    DESCRIPTION: This test case verifies Quick Deposit section when price for selection is changed
    PRECONDITIONS: * In order to check response open Dev Tools -> select Network -> WS -> Frames section
    PRECONDITIONS: * Load app and log in with user has at list one cards added to his account: Visa, Visa Electron, Master Card or Maestro
    PRECONDITIONS: * Add selection to Betslip
    PRECONDITIONS: * Open OpenBet TI tool for updates: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Please deposit a min <currency symbol>XX.XX to continue placing your bet' error message is displayed on red background at the bottom of Betslip
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: * 'BET NOW' button becomes 'MAKE A DEPOSIT'
        """
        pass

    def test_002_tap_make_a_quick_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A QUICK DEPOSIT'
        EXPECTED: * Quick Deposit section is displayed
        EXPECTED: * 'MAKE A QUICK DEPOSIT' button becomes 'DEPOSIT & PLACE BET' immediately
        """
        pass

    def test_003_trigger_price_change_for_added_selection_in_openbet_ti_tool_and_save_changes(self):
        """
        DESCRIPTION: Trigger price change for added selection in Openbet TI tool and save changes
        EXPECTED: 
        """
        pass

    def test_004_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: * Live update is received in WS
        EXPECTED: * Notification about price change is displayed next to added selection
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes 'ACCEPT(DEPOSIT & PLACE BET)' immediately
        """
        pass

    def test_005_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: Quick Deposit section is closed
        """
        pass

    def test_006_tap_make_a_deposit_again(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' again
        EXPECTED: * Quick Deposit section is displayed
        EXPECTED: * Bet placement button remains 'ACCEPT(DEPOSIT & PLACE BET)'
        """
        pass
