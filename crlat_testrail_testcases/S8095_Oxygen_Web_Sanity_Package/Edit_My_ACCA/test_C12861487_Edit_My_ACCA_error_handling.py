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
class Test_C12861487_Edit_My_ACCA_error_handling(Common):
    """
    TR_ID: C12861487
    NAME: 'Edit My ACCA' error handling
    DESCRIPTION: 
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Generate Error text in CMS: CMS System Config Data>EMA
    PRECONDITIONS: 1. User1 has 2(bets) with cash out available placed on Single line Accumulator (e.g. ACCA4) (All selections in the placed bet are active and open)
    PRECONDITIONS: 2. Login with User1
    PRECONDITIONS: 3. Navigate to My Bets > Open Bets tab
    PRECONDITIONS: 4. Tap 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def test_001_remove_few_selections_from_the_bet(self):
        """
        DESCRIPTION: Remove few selections from the bet
        EXPECTED: * 'UNDO' button is shown for removed selections
        EXPECTED: * 'CONFIRM' button is shown and enabled
        EXPECTED: * Stake and Est. Returns are updated
        """
        pass

    def test_002_tap_confirm_buttonin_the_same_time_suspend_any_eventmarketselection_from_the_edited_betverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message_and_removed_selections_are_remembered(self):
        """
        DESCRIPTION: Tap 'CONFIRM' button
        DESCRIPTION: In the same time suspend any event/market/selection from the edited bet
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message and removed selections are remembered
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: * Error Message: "text from CMS"
        EXPECTED: * 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: * Disabled 'Selection Removal' buttons for all other selections
        EXPECTED: * Original Stake and Est. Returns
        EXPECTED: * 'SUSP CONFIRM' button is disabled
        EXPECTED: * 'CANCEL EDITING' is enabled
        EXPECTED: ![](index.php?/attachments/get/18729339)
        EXPECTED: ![](index.php?/attachments/get/18729341)
        """
        pass

    def test_003_close_message_and_tap_cancel_editing_button(self):
        """
        DESCRIPTION: Close message and Tap 'Cancel Editing' button
        EXPECTED: * Error Message is closed
        EXPECTED: * Edit mode is closed
        """
        pass

    def test_004_navigate_to_ti___unsuspend_selection_which_was_suspended(self):
        """
        DESCRIPTION: Navigate to TI -> Unsuspend selection which was suspended
        EXPECTED: 
        """
        pass

    def test_005_tap_edit_my_acca_button(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_ti_and_uncheck_cash_out_for_any_event_in_the_editing_bet_to_generate_validbet__reqbetbuild_or_reqbetplace_error(self):
        """
        DESCRIPTION: Navigate to TI and uncheck 'Cash out' for any event in the editing bet (to generate Validbet / reqBetBuild or reqBetPlace error)
        EXPECTED: 
        """
        pass

    def test_007_tap_selection_removal_button_for_any_selectionverify_that_an_error_message_is_shown_and_selection_is_not_removed(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any selection
        DESCRIPTION: Verify that an error message is shown and selection is not removed
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: * Error message "text fro CMS" is shown
        EXPECTED: * Selection is not removed
        EXPECTED: * 'CONFIRM' button is disabled
        EXPECTED: * 'CANCEL EDITING' button is enabled
        """
        pass

    def test_008_tap_cancel_editing_button(self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        EXPECTED: Edit mode is closed
        """
        pass

    def test_009_in_ti_turn_on_cash_out_for_selection_where_is_was_unchecked(self):
        """
        DESCRIPTION: In TI Turn on cash out for selection where is was unchecked
        EXPECTED: 
        """
        pass

    def test_010_tap_edit_my_acca_button_and_remove_any_selection(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button and remove any selection
        EXPECTED: * 'UNDO' button is shown for removed selection
        EXPECTED: * 'Removed' label is shown for removed selection
        """
        pass

    def test_011_uncheck_cash_out_in_ti_for_any_event_in_the_editing_bet_to_generate_validbet__reqbetbuild_or_reqbetplace_error(self):
        """
        DESCRIPTION: Uncheck 'Cash out' in TI for any event in the editing bet (to generate Validbet / reqBetBuild or reqBetPlace error)
        EXPECTED: 
        """
        pass

    def test_012_tap_confirm_buttonverify_that_edit_mode_is_remains_opened_with_an_error_message_and_confirm_button_is_clickable(self):
        """
        DESCRIPTION: Tap 'CONFIRM' button
        DESCRIPTION: Verify that edit mode is remains opened with an error message and 'Confirm' button is clickable
        EXPECTED: * Edit mode is remains opened
        EXPECTED: * Error message 'text from CMS' is shown
        EXPECTED: * 'CONFIRM' button is clickable
        EXPECTED: * 'CANCEL EDITING' button is clickable
        """
        pass

    def test_013_provide_same_verification_on_my_bets__cashout_tab(self):
        """
        DESCRIPTION: Provide same verification on My Bets > Cashout tab
        EXPECTED: Results are the same
        """
        pass
