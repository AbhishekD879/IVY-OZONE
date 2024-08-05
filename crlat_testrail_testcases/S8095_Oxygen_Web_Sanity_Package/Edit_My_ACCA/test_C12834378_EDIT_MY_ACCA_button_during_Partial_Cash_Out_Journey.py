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
class Test_C12834378_EDIT_MY_ACCA_button_during_Partial_Cash_Out_Journey(Common):
    """
    TR_ID: C12834378
    NAME: 'EDIT MY ACCA' button during Partial Cash Out Journey
    DESCRIPTION: 
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Login into App
    PRECONDITIONS: 3. Place single bet and multiple bet with more than 4 selection (e.g. ACCA 5) (selections should have cash out available)
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: 4. Navigate to My Bets page
    PRECONDITIONS: NOTE: Verifications should be done on Cash Out and on Open Bets tabs
    """
    keep_browser_open = True

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_acca_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY ACCA' button and Partial Cash Out bar are shown
        EXPECTED: * 'EDIT MY ACCA' button is shown and enable
        EXPECTED: * Partial Cash Out bar is shown
        """
        pass

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_acca_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY ACCA' button is shown
        EXPECTED: * EDIT MY ACCA' button is shown and enable
        EXPECTED: * Partial Cash Out value is changing
        """
        pass

    def test_003_tap_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_acca_buttons_are_show(self):
        """
        DESCRIPTION: Tap 'Cash Out' button
        DESCRIPTION: Verify that 'Confirm Cash Out' and 'EDIT MY ACCA' buttons are show
        EXPECTED: * 'EDIT MY ACCA' button is shown and enable
        EXPECTED: * 'Confirm Cash Out' button is shown and enabled
        EXPECTED: * 'Confirm Cash Out' button is flashing 3 times
        """
        pass

    def test_004_tap_edit_my_acca_buttonverify_that_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button
        DESCRIPTION: Verify that Partial cash out journey is not shown and edit mode for ACCA is opened
        EXPECTED: * Partial Cash Out journey is closed and not shown
        EXPECTED: * Cash Out and Partial Cash Out button is not shown at all
        EXPECTED: * Edit mode for ACCA is opened
        """
        pass

    def test_005_tap_cancel_editing_buttonverify_that_edit_mode_for_acca_is_closed_and_cash_out_and_partial_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        DESCRIPTION: Verify that edit mode for ACCA is closed and Cash Out and Partial Cash Out button is shown
        EXPECTED: * Edit mode for ACCA is closed
        EXPECTED: * Cash Out and Partial Cash Out button is shown
        """
        pass

    def test_006_run_1_3_step_one_more_time(self):
        """
        DESCRIPTION: Run 1-3 step one more time
        EXPECTED: Results are the same
        """
        pass

    def test_007_tap_confirm_cash_out_buttonverify_that_edit_my_acca_button_is_shown_and_disabled(self):
        """
        DESCRIPTION: Tap 'Confirm Cash Out' button
        DESCRIPTION: Verify that 'EDIT MY ACCA' button is shown and disabled
        EXPECTED: * 'EDIT MY ACCA' button is shown and disabled
        EXPECTED: * Spiner for partial cash out is shown
        EXPECTED: * 'Successful cash out' is shown
        """
        pass

    def test_008_verify_that_successful_cash_out_message_is_shown__and_edit_my_acca_button_is_shown_and_enabled(self):
        """
        DESCRIPTION: Verify that 'Successful cash out' message is shown  and 'EDIT MY ACCA' button is shown and enabled
        EXPECTED: * 'EDIT MY ACCA' button is shown and enabled
        EXPECTED: * On Open Bets tab: 'Show Partial Cash Out History' drop down is shown with cashed out value in the table
        """
        pass
