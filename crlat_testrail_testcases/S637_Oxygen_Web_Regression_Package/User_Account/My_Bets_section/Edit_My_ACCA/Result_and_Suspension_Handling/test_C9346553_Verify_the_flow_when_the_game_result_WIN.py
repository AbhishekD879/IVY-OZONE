import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C9346553_Verify_the_flow_when_the_game_result_WIN(Common):
    """
    TR_ID: C9346553
    NAME: Verify the flow when the game result WIN
    DESCRIPTION: This test case verifies that the flow for EMA edit mode when game result WIN
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a bet on TREBLE or more (All selections in the placed bet are active and open)
    PRECONDITIONS: Go To My Bets>Cash OUt / Open Bets
    PRECONDITIONS: Tap 'EDIT MY ACCA/Bet' button for placed bet
    PRECONDITIONS: Test case should be run on Cash out tab and on Open Bets tab
    PRECONDITIONS: NOTE: WIN result should be set to the appropriate selection in the bet
    """
    keep_browser_open = True

    def test_001_go_to_ti_and_set_win_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: Go to TI and set 'WIN' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: - 'WIN' label (green tick icon) is shown for resulted event
        EXPECTED: - 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: - 'Selection Removal' button is shown and clickable for other events
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'CONFIRM' button is shown and NOT clickable
        EXPECTED: - Est. Returns are updated
        """
        pass

    def test_002_tap_selection_removal_button_for_any_other_selection_in_the_betverify_that_confirm_button_is_clickable_and_undo_button_is_shown_for_removed_selection(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any other selection in the bet
        DESCRIPTION: Verify that 'CONFIRM' button is clickable and 'UNDO' button is shown for removed selection
        EXPECTED: - 'UNDO' button is shown for removed selection
        EXPECTED: - 'CONFIRM' button is shown and clickable
        """
        pass
