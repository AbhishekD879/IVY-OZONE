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
class Test_C9346554_TO_BE_EDITED_Verify_the_flow_when_the_game_result_LOSE(Common):
    """
    TR_ID: C9346554
    NAME: [TO BE EDITED] Verify the flow when the game result LOSE
    DESCRIPTION: This test case verifies that the flow for EMA edit mode when game result LOSE
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a bet on TREBLE or more (All selections in the placed bet are active and open)
    PRECONDITIONS: Go To My Bets>Cash OUt / Open Bets
    PRECONDITIONS: Tap 'EDIT MY ACCA' button for placed bet
    PRECONDITIONS: Test case should be run on Cash out tab and on Open Bets tab
    PRECONDITIONS: NOTE: LOSE result should be set to the appropriate selection in the bet
    """
    keep_browser_open = True

    def test_001_go_to_ti_and_set_lose_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event_and_error_message_is_displayed_your_acca_is_no_longer_active(self):
        """
        DESCRIPTION: Go to TI and set 'LOSE' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event and error message is displayed "Your Acca is no longer active"
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: - 'LOST' label (red cross icon) is shown for resulted event
        EXPECTED: - 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: - 'Selection Removal' button is NOT shown for other events
        EXPECTED: - Error message is displayed "Your Acca is no longer active"
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'CONFIRM' button is shown and NOT clickable
        EXPECTED: NOTE: On Cash Out tab the bet will disappear after setting result
        """
        pass
