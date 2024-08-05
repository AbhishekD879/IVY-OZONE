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
class Test_C896779_Verify_Quick_Deposit_section_when_price_for_bet_is_changed(Common):
    """
    TR_ID: C896779
    NAME: Verify Quick Deposit section when price for bet is changed
    DESCRIPTION: This test case verifies Quick Deposit section when price for bet is changed
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in, has 0 or very low balance
    PRECONDITIONS: * Users have the payment cards added to his account
    PRECONDITIONS: * Open OpenBet TI tool for price changing:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_and_login_under_user_from_preconditions(self):
        """
        DESCRIPTION: Load Oxygen app and login under user from preconditions
        EXPECTED: 
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        EXPECTED: * Buttons 'ADD TO BETSLIP' and 'MAKE A DEPOSIT' are enabled
        """
        pass

    def test_004_change_price_in_backoffice_ti_and_save_changes(self):
        """
        DESCRIPTION: Change price in Backoffice TI and save changes
        EXPECTED: * Price is updated
        """
        pass

    def test_005_check_quick_bet_displaying(self):
        """
        DESCRIPTION: Check Quick Bet displaying
        EXPECTED: * 'Price change from 'n' to 'n'' warning message is displayed on yellow(for Coral) / cyan(for Ladbrokes) background below 'QUICK BET' header
        EXPECTED: * 'Estimated Returns' (for Coral) / 'Potential Returns' (for Ladbrokes) value is recalculated
        """
        pass

    def test_006_click_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Click on 'MAKE A DEPOSIT' button
        EXPECTED: * 'Quick Deposit' section is opened
        EXPECTED: * Warning Message on a yellow/cyan background is not shown
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET'
        """
        pass

    def test_007_change_price_in_backoffice_ti_and_check_quick_deposit_section(self):
        """
        DESCRIPTION: Change price in Backoffice TI and check Quick Deposit section
        EXPECTED: * Warning Message on yellow/cyan background appears with text: 'Price change from 'n' to 'n''
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes 'ACCEPT (DEPOSIT & PLACE BET)'
        """
        pass

    def test_008_tap_on_close_x_button(self):
        """
        DESCRIPTION: Tap on close (X) button
        EXPECTED: 
        """
        pass

    def test_009_tap_make_a_deposit_button_and_hange_price_in_backoffice_ti(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button and сhange price in Backoffice TI
        EXPECTED: * Warning Message on yellow/cyan background appears 'Price change from 'n' to 'n''
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes 'ACCEPT (DEPOSIT & PLACE BET)'
        """
        pass

    def test_010_make_a_successful_deposit_and_check_bet_is_placed(self):
        """
        DESCRIPTION: Make a successful deposit and check bet is placed
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown to user with new price and recalculated 'Estimated Returns'(for Coral) / 'Potential Returns'(for ladbrokes) value
        """
        pass
