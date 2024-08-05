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
class Test_C15392893_Verify_Quick_Deposit_section_when_event_market_selection_is_suspended(Common):
    """
    TR_ID: C15392893
    NAME: Verify Quick Deposit section when event/market/selection is suspended
    DESCRIPTION: This test case verifies Quick Deposit section when event/market/selection is suspended in Betslip
    PRECONDITIONS: * In order to check response open Dev Tools -> select Network -> WS -> Frames section
    PRECONDITIONS: * Load app and log in with user has at list one cards added to his account: Visa, Visa Electron, Master Card or Maestro
    PRECONDITIONS: * Add selection to Betslip
    PRECONDITIONS: * Open OpenBet TI tool for updates: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Please deposit a min <currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: * 'BET NOW' button becomes 'MAKE A DEPOSIT'
        """
        pass

    def test_002_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT'
        EXPECTED: * Quick Deposit section is displayed
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET' immediately
        """
        pass

    def test_003_suspend_added_selection_on_selection_market_eventlevel_in_openbet_ti_tool_and_save_changes(self):
        """
        DESCRIPTION: Suspend added selection on
        DESCRIPTION: * selection
        DESCRIPTION: * market
        DESCRIPTION: * event
        DESCRIPTION: level in Openbet TI tool and save changes
        EXPECTED: 
        """
        pass

    def test_004_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: * Live update is received in WS
        EXPECTED: * *Selection is suspended in Betslip*
        EXPECTED: * 'DEPOSIT & PLACE BET'' button becomes 'DEPOSIT' immediately
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
        EXPECTED: * *Selection is no more suspended in Betslip*
        EXPECTED: * 'DEPOSIT' button becomes 'DEPOSIT & PLACE BET'' immediately
        """
        pass

    def test_007_suspend_added_selection_in_openbet_ti_tool_and_save_changes(self):
        """
        DESCRIPTION: Suspend added selection in Openbet TI tool and save changes
        EXPECTED: * *Selection is suspended in Betslip*
        EXPECTED: * 'DEPOSIT & PLACE BET'' button becomes 'DEPOSIT' immediately
        """
        pass

    def test_008_enter_valid_cvv_amount_value_and_tap_deposit_button(self):
        """
        DESCRIPTION: Enter valid CVV, Amount value and tap 'DEPOSIT' button
        EXPECTED: * Success message and pop-up about the deposit is NOT displayed
        EXPECTED: * User`s balance is increased
        EXPECTED: * Quick Deposit stays displayed
        EXPECTED: * Bet is not placed
        """
        pass

    def test_009_close_quick_deposit_via_x_button(self):
        """
        DESCRIPTION: Close Quick Deposit via 'X' button
        EXPECTED: * Quick Deposit section is closed
        EXPECTED: * 'DEPOSIT' button becomes 'PLACE BET'and is disabled
        """
        pass
