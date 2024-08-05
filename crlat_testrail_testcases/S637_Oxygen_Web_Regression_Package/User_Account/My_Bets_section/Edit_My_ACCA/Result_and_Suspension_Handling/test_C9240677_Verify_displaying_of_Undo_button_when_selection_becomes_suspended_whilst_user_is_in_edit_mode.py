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
class Test_C9240677_Verify_displaying_of_Undo_button_when_selection_becomes_suspended_whilst_user_is_in_edit_mode(Common):
    """
    TR_ID: C9240677
    NAME: Verify displaying of 'Undo' button when selection becomes suspended whilst user is in edit mode
    DESCRIPTION: This test case verifies that 'Undo' button is not shown in case the selection is suspended
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Navigate to My Bets > Cashout
    PRECONDITIONS: 3. Tap 'EDIT MY ACCA' button
    PRECONDITIONS: NOTE: The verifications should be done in 'List View' and in 'Card View'
    """
    keep_browser_open = True

    def test_001_tap_selection_removal_buttons_for_few_selections_in_the_betverify_that_undo_buttons_are_shown_for_removed_selections_and_updated_stake_and_est_returns_are_shown_for_the_bet(self):
        """
        DESCRIPTION: Tap 'Selection Removal' buttons for few selections in the bet
        DESCRIPTION: Verify that 'Undo' buttons are shown for removed selections and updated Stake and Est. returns are shown for the bet
        EXPECTED: - 'UNDO' buttons are shown for removed selections
        EXPECTED: - Updated Stake is shown
        EXPECTED: - Updated Est. Return is shown
        """
        pass

    def test_002_navigate_to_ti_and_suspend_one_of_eventmarketselection_from_the_bet_which_was_removed(self):
        """
        DESCRIPTION: Navigate to TI and suspend one of event/market/selection from the bet which was removed
        EXPECTED: The selection event/market/selection is suspended
        """
        pass

    def test_003_navigate_back_to_the_applicationverify_that_undo_button_is_not_shown_and_susp_confirm_button_becomes_disabled(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that 'Undo' button is NOT shown and 'SUSP CONFIRM' button becomes disabled
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - 'SUSPENDED' label and disabled 'Selection Removal' button for suspended event/market/selection
        EXPECTED: - Disabled 'Selection Removal' buttons for all other selections
        EXPECTED: - Stake and Est. Returns are updated back to initial
        EXPECTED: - SUSP is displayed in the 'CONFIRM' button
        EXPECTED: - 'SUSP CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass

    def test_004_tap_cancel_editing_buttonverify_that_edit_mode_is_closed_and_edit_my_acca_button_is_disabled(self):
        """
        DESCRIPTION: Tap 'CANCEL EDITING' button
        DESCRIPTION: Verify that edit mode is closed and 'EDIT MY ACCA' button is disabled
        EXPECTED: - Edit mode is closed
        EXPECTED: - 'EDIT MY ACCA' button is shown and disabled
        EXPECTED: - Label 'SUSPENDED' is shown for suspended event/market/selection
        """
        pass

    def test_005_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_undo_button_is_not_shown_for_suspended_eventmarketselection_the_suspended_label_is_shown_instead_of_it_and_confirm_button_becomes_disabled(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that 'Undo' button is not shown for suspended event/market/selection, the "SUSPENDED' label is shown instead of it and 'CONFIRM' button becomes disabled
        EXPECTED: - 'SUSPENDED' label is shown
        EXPECTED: - Disabled 'Selection Removal' buttons for all selections
        EXPECTED: - Initial Stake and Est. Returns are shown
        EXPECTED: - 'SUSP CONFIRM' button is shown and disabled
        EXPECTED: - 'CANCEL EDITING' is shown and enabled
        """
        pass
