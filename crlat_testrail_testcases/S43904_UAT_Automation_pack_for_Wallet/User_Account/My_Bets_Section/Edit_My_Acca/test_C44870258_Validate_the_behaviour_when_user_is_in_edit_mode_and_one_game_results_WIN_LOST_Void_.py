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
class Test_C44870258_Validate_the_behaviour_when_user_is_in_edit_mode_and_one_game_results_WIN_LOST_Void_(Common):
    """
    TR_ID: C44870258
    NAME: Validate the behaviour when user is in edit mode and one game results (WIN/LOST/Void) )
    DESCRIPTION: 
    PRECONDITIONS: Login with User
    PRECONDITIONS: User must have accumulator bets
    PRECONDITIONS: Navigate to My Bets > open bets
    """
    keep_browser_open = True

    def test_001_user_is_in_edit_modego_to_ti_and_set_win_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: User is in EDIT MODE
        DESCRIPTION: Go to TI and set 'WIN' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: WIN' label (green tick icon) is shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: 'Selection Removal' button is shown and clickable for other events
        EXPECTED: 'CANCEL EDITING' button is shown and clickable
        EXPECTED: 'CONFIRM' button is shown and NOT clickable
        EXPECTED: Est. Returns are updated
        """
        pass

    def test_002_tap_selection_removal_button_for_any_other_selection_in_the_betverify_that_confirm_button_is_clickable_and_undo_button_is_shown_for_removed_selection(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any other selection in the bet
        DESCRIPTION: Verify that 'CONFIRM' button is clickable and 'UNDO' button is shown for removed selection
        EXPECTED: 'UNDO' button is shown for removed selection
        EXPECTED: 'CONFIRM' button is shown and clickable
        """
        pass

    def test_003_go_to_ti_and_set_lose_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event_and_error_message_is_displayed_your_acca_is_no_longer_active(self):
        """
        DESCRIPTION: Go to TI and set 'LOSE' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event and error message is displayed "Your Acca is no longer active
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: 'LOST' label (red cross icon) is shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for other events
        EXPECTED: Error message is displayed "Your Acca is no longer active"
        EXPECTED: 'CANCEL EDITING' button is shown and clickable
        EXPECTED: 'CONFIRM' button is shown and NOT clickable
        EXPECTED: NOTE: On Cash Out tab the bet will disappear after setting result
        """
        pass

    def test_004_in_the_same_time_suspend_any_eventmarketselection_from_the_bet_in_tiverify_that_edit_mode_is_opened(self):
        """
        DESCRIPTION: In the same time suspend any event/market/selection from the bet in TI
        DESCRIPTION: Verify that edit mode is opened
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: 'SUSPENDED' label is displayed
        EXPECTED: Disabled 'Selection Removal' buttons for all selections
        EXPECTED: 'SUSP CONFIRM' button is disabled
        EXPECTED: 'CANCEL EDITING' is still displayed.
        """
        pass

    def test_005_go_to_ti_and_set_void_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: Go to TI and set 'VOID' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: 'VOID' label is shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown and NOT clickable for other events
        EXPECTED: 'CANCEL EDITING' button is shown and clickable
        EXPECTED: 'CONFIRM' button is shown and NOT clickable
        EXPECTED: Est. Returns are updated
        """
        pass

    def test_006_verify_that_confirm_button_is_disabled(self):
        """
        DESCRIPTION: Verify that 'CONFIRM' button is disabled
        EXPECTED: CONFIRM button is disabled
        """
        pass
