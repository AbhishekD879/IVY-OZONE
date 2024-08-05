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
class Test_C858591_Numeric_keyboard__quick_stake_buttons(Common):
    """
    TR_ID: C858591
    NAME: Numeric keyboard - quick stake buttons
    DESCRIPTION: This test case verifies 'Quick Stakes' buttons on bet slip keyboard
    PRECONDITIONS: 1. Quick Stake functionality is available for Mobile ONLY
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile device
    PRECONDITIONS: 3. There is no selections added to Bet Slip
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add one selection to Bet Slip
        EXPECTED: Added selection is available within the Betslip
        """
        pass

    def test_002_navigate_to_bet_slip(self):
        """
        DESCRIPTION: Navigate to Bet Slip
        EXPECTED: * Bet Slip slide is opened
        EXPECTED: * 'Singles (1)'/'Your Selections: 1' section with added selection is displayed
        """
        pass

    def test_003_set_focus_on_the_stake_field_verify_if_all_buttons_are_shown_with_plus_sign(self):
        """
        DESCRIPTION: Set focus on the 'Stake' field. Verify if all buttons are shown with '+' sign
        EXPECTED: Keyboard with 'Quick stakes' buttons are displayed with the next values:
        EXPECTED: * +<currency symbol>5
        EXPECTED: * +<currency symbol>10
        EXPECTED: * +<currency symbol>50
        EXPECTED: * +<currency symbol>100
        EXPECTED: where <currency symbol> may be :
        EXPECTED: * 'GBP': symbol = £;
        EXPECTED: * 'USD': symbol = $;
        EXPECTED: * 'EUR': symbol = €;
        EXPECTED: * 'SEK': symbol = Kr'
        EXPECTED: **NOTE** that for SEK currency the values of quick stakes are: 50, 100, 500, 1000
        """
        pass

    def test_004_tap_pluscurrency_symbol5_button_eg_5(self):
        """
        DESCRIPTION: Tap '+<currency symbol>5' button (e.g. £5)
        EXPECTED: * Value of 5 is added to 'Stake' field
        EXPECTED: * 'Est. Returns' value is calculated according to added value
        """
        pass

    def test_005_tap_pluscurrency_symbol10_button_eg_10(self):
        """
        DESCRIPTION: Tap '+<currency symbol>10' button (e.g. £10)
        EXPECTED: * Value of 10 is added to 'Stake' field
        EXPECTED: * 'Est. Returns' value is calculated according to added value
        """
        pass

    def test_006_tap_pluscurrency_symbol50_button_eg_50(self):
        """
        DESCRIPTION: Tap '+<currency symbol>50' button (e.g. £50)
        EXPECTED: * Value of 50 is added to 'Stake' field
        EXPECTED: * 'Est. Returns' value is calculated according to added value
        """
        pass

    def test_007_tap_pluscurrency_symbol100_button_eg_100(self):
        """
        DESCRIPTION: Tap '+<currency symbol>100' button (e.g. £100)
        EXPECTED: * Value of 100 is added to 'Stake' field
        EXPECTED: * 'Est. Returns' value is calculated according to added value
        """
        pass

    def test_008_add_several_amounts_from_quick_stakes_buttons_eg_plus5_and_plus10(self):
        """
        DESCRIPTION: Add several amounts from 'Quick stakes' buttons (e.g. +£5 and +£10)
        EXPECTED: Amounts on the 'Stake' field are added. Sum of all entered 'quick stake' amounts are shown (e.g. £15 should be shown)
        """
        pass

    def test_009_enter_any_amount_manually_from_keyboard_and_tap_on_the_any_quick_stakes_button_eg_plus10(self):
        """
        DESCRIPTION: Enter any amount manually from keyboard and tap on the any 'quick stakes' button (e.g. +£10)
        EXPECTED: Quick stake value is added on top of entered manually  value. Sum of entered amount is shown
        """
        pass

    def test_010_enter_any_amount_from_quick_stakes_buttons_and_then_enter_any_amount_from_keyboard(self):
        """
        DESCRIPTION: Enter any amount from 'quick stakes' buttons and then enter any amount from keyboard
        EXPECTED: Manually entered stake overwrites the previously selected quick stake value
        """
        pass

    def test_011_click_bet_now_button(self):
        """
        DESCRIPTION: Click 'Bet Now' button
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed
        EXPECTED: - Balance is reduced accordingly
        """
        pass
