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
class Test_C9240678_Verify_displaying_of_Undo_and_Selection_Removal_buttons_when_selection_returns_from_suspension_whilst_user_is_in_edit_mode(Common):
    """
    TR_ID: C9240678
    NAME: Verify displaying of Undo and Selection Removal buttons when selection returns from suspension whilst user is in edit mode
    DESCRIPTION: This test case verifies that initial edit mode is shown with enabled 'Selection removal' buttons when selection returns from suspension whilst user is in edit mode
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Navigate to My Bets > Cashout
    PRECONDITIONS: 3. Tap 'EDIT MY ACCA' button
    PRECONDITIONS: 4. Tap 'Selection Removal' button for any selection
    PRECONDITIONS: 5. Go to TI and Suspend event/market/selection which was removed in the previous step
    PRECONDITIONS: NOTE: The verifications should be done in 'List View' and in 'Card View'
    """
    keep_browser_open = True

    def test_001_navigate_back_to_the_applicationverify_that_disabled_selection_removal_buttons_and_susp_confirm_button_are_shown(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that disabled 'Selection Removal' buttons and 'SUSP CONFIRM' button are shown
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - 'SUSPENDED' label and disabled 'Selection Removal' button for suspended event/market/selection
        EXPECTED: - Disabled 'Selection Removal' buttons for all other selections
        EXPECTED: - Original Stake and Est. Returns are shown
        EXPECTED: - 'SUSP CONFIRM' button is shown and disabled
        EXPECTED: - 'CANCEL EDITING' is shown and enabled
        """
        pass

    def test_002_navigate_to_ti_and_unsuspend_eventmarketselection_which_was_suspended_in_preconditions(self):
        """
        DESCRIPTION: Navigate to TI and unsuspend event/market/selection which was suspended in preconditions
        EXPECTED: The selection event/market/selection is active
        """
        pass

    def test_003_navigate_back_to_the_applicationverify_that_initial_edit_mode_is_shown_with_enabled_selection_removal_buttons(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that initial edit mode is shown with enabled 'Selection removal' buttons
        EXPECTED: - Edit mode is shown with enabled 'Selection Removal' buttons for all selections in the bet
        EXPECTED: - Original Stake and Est. Returns are shown
        EXPECTED: - 'CONFIRM' button is shown and disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass

    def test_004_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_initial_edit_mode_is_shown_with_enabled_selection_removal_buttons_after__selection_returns_from_suspension(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that initial edit mode is shown with enabled 'Selection removal' buttons after  selection returns from suspension
        EXPECTED: - Edit mode is shown with enabled 'Selection Removal' buttons for all selections in the bet
        EXPECTED: - 'CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass
