import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C9726422_Verify_displaying_EDIT_MY_ACCA_Bet_button_during_Partial_Cash_Out_Journey(Common):
    """
    TR_ID: C9726422
    NAME: Verify displaying 'EDIT MY ACCA/Bet' button during Partial Cash Out Journey
    DESCRIPTION: This test case verifies displaying 'EDIT MY ACCA' button during Partial Cashout Journey
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login and place a multiple bet with Partial Cash Out available
    PRECONDITIONS: 2. Navigate to My Bets page -> Cash Out tab
    PRECONDITIONS: 3. Navigate to My Bets page -> Open Bets tab
    PRECONDITIONS: Need to verify on both Cash Out tab and Open Bets tab
    """
    keep_browser_open = True

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        pass

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_accabet_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY ACCA/Bet' button is shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out value is changing
        """
        pass

    def test_003_tap_x_button_to_close_partial_cash_outverify_that_partial_cash_out_bar_is_closed_and_edit_my_accabet_button_is_shown(self):
        """
        DESCRIPTION: Tap 'X' button to close partial cash out
        DESCRIPTION: Verify that Partial Cash Out bar is closed and 'EDIT MY ACCA/Bet' button is shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is closed
        EXPECTED: - 'Cash Out' and 'Partial Cash Out' buttons are shown
        """
        pass

    def test_004_tap_partial_cash_out_button_one_more_timeverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button one more time
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        pass

    def test_005_tap_partial_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button
        DESCRIPTION: Verify that 'Confirm Cash Out' and 'EDIT MY ACCA/Bet' buttons are shown and enabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - 'Confirm Cash Out' button is shown and enabled
        EXPECTED: - 'Confirm Cash Out' button is flashing 3 times
        """
        pass

    def test_006_wait_while_confirm_cash_out_button_disappearverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Wait while 'Confirm Cash Out' button disappear
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        pass

    def test_007_tap_partial_cash_out_button_againverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button again
        DESCRIPTION: Verify that 'Confirm Cash Out' and 'EDIT MY ACCA/Bet' buttons are shown and enabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - 'Confirm Cash Out' button is shown and enabled
        EXPECTED: - 'Confirm Cash Out' button is flashing 3 times
        """
        pass

    def test_008_tap_confirm_cash_out_buttonverify_that_edit_my_accabet_button_is_shown_and_disabled(self):
        """
        DESCRIPTION: Tap 'Confirm Cash Out' button
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button is shown and disabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and disabled
        EXPECTED: - Spiner for partial cash out is shown
        EXPECTED: - 'Partial Cash Out Successful' is shown
        """
        pass

    def test_009_verify_that_after_partial_cash_out_successful_message_disappearnavigate_between_tabs_the_edit_my_accabet_button_is_shown_and_enabled(self):
        """
        DESCRIPTION: Verify that after 'Partial Cash Out Successful' message disappear(navigate between tabs) the 'EDIT MY ACCA/Bet' button is shown and enabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enabled
        EXPECTED: - On Open Betds tab: 'Partial Cash Out History' drop down is shown with cashed out value in the table
        """
        pass
