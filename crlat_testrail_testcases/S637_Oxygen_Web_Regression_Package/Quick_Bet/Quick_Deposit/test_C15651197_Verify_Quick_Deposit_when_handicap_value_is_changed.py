import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C15651197_Verify_Quick_Deposit_when_handicap_value_is_changed(Common):
    """
    TR_ID: C15651197
    NAME: Verify Quick Deposit when handicap value is changed
    DESCRIPTION: This test case verifies market line(handicap) changes visibility during switch from QuickBet to QuickDeposit screens(and vice versa)
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: In order to check response open Dev Tools -> select Network -> WS -> Frames section
    PRECONDITIONS: Load app and log in with a user has at least one card added to his account with a positive balance and no restrictions on betting
    PRECONDITIONS: Add selection from Handicap market to Quick Bet
    PRECONDITIONS: Open OpenBet TI tool for updates: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for Ladbrokes brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for Coral brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: Buttons 'ADD TO BETSLIP' and 'MAKE A DEPOSIT' are enabled
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventchange_rawhandicapvalue_on_market_level(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change** rawHandicapValue **on market level
        EXPECTED: 'Line Change from #OLD to #NEW' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: 'MAKE A DEPOSIT' button remains enabled
        """
        pass

    def test_003_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: Quick Deposit section is displayed
        EXPECTED: 'Line Change' message is no longer shown.
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below 'Quick Deposit' header for both brands
        EXPECTED: 'Deposit & Place Bet' button is enabled
        """
        pass

    def test_004_trigger_the_following_situation_for_this_eventchange_rawhandicapvalue_on_market_level(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change** rawHandicapValue **on market level
        EXPECTED: 'Line Change from #OLD to #NEW' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background above 'Quick Deposit' header
        EXPECTED: 'Accept (Deposit & Place Bet)' button remains enabled
        """
        pass

    def test_005_tap_on_x_buttonexit_the_quick_deposit_window(self):
        """
        DESCRIPTION: Tap on 'x' button(exit the Quick Deposit window)
        EXPECTED: Quick Bet section is displayed
        EXPECTED: 'Line Change' message is no longer shown.
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the Quick Stake buttons immediately for Ladbrokes brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for Coral brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'MAKE A DEPOSIT' button remains enabled
        """
        pass
