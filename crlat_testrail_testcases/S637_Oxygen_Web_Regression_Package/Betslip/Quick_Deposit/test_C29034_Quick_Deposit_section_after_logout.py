import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29034_Quick_Deposit_section_after_logout(Common):
    """
    TR_ID: C29034
    NAME: 'Quick Deposit' section after logout
    DESCRIPTION: This test scenario verifies Quick Deposit section displaying after user is logged out by server
    PRECONDITIONS: *   Open Oxygen app in two separate tabs(within same browser window)
    PRECONDITIONS: *   Login to Oxygen app in both browser tabs under the same user account credentials
    PRECONDITIONS: User account should have positive balance and at least 1 added(and active) card
    """
    keep_browser_open = True

    def test_001_tab_1_add_selection_into_betslip_through_browser_tab_1_and_open_bet_slip_page__widget_there(self):
        """
        DESCRIPTION: (Tab #1) Add selection into Betslip through browser tab #1 and open Bet Slip page / widget there
        EXPECTED: - Selection is displayed within Bet Slip area
        EXPECTED: - Numeric keyboard is NOT displayed (mobile only)
        """
        pass

    def test_002_tab_1_enter_stake_that_exceeds_users_balance(self):
        """
        DESCRIPTION: (Tab #1) Enter Stake that exceeds user's balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately
        """
        pass

    def test_003_tab_1_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: (Tab #1) Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        """
        pass

    def test_004_tab_1_set_all_fields_with_correct_values_in_quick_deposit_sectioncvv_deposit_amount(self):
        """
        DESCRIPTION: (Tab #1) Set all fields with correct values in 'Quick Deposit' section
        DESCRIPTION: (CVV, Deposit Amount)
        EXPECTED: - 'QUICK DEPOSIT' section remains expanded
        """
        pass

    def test_005_logout_from_the_app_through_browser_tab_2users_balance___logout_and_switch_to_browser_tab_1_after_that(self):
        """
        DESCRIPTION: Logout from the app through browser tab #2(User's Balance -> Logout) and switch to browser tab #1 after that
        EXPECTED: -  Pop-up message about logging out is shown
        EXPECTED: -  User is logged out from the application without performing any actions in tab #1
        """
        pass

    def test_006_tab_1_close_log_out_pop_up_open_betslip_and_verify_presence_of_quick_deposit_section_there(self):
        """
        DESCRIPTION: (Tab #1) Close 'Log out' pop-up, Open Betslip and verify presence of 'Quick Deposit' section there
        EXPECTED: * 'Quick Deposit' section is no more present within Betslip
        EXPECTED: * 'LOGIN AND PLACE BET' button is shown
        EXPECTED: * Numeric keyboard is NOT displayed (mobile only)
        """
        pass
