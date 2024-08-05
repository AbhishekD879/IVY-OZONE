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
class Test_C12834354_Flow_with_game_results_WIN_LOSE_VOID(Common):
    """
    TR_ID: C12834354
    NAME: Flow with game results WIN, LOSE, VOID
    DESCRIPTION: 
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Place a bet on three TREBLE bets (All selections in the placed bet are active and open)
    PRECONDITIONS: 3. Go To My Bets>Open Bets
    PRECONDITIONS: 4. Tap 'EDIT MY ACCA' button for one of the placed bet
    PRECONDITIONS: Test case should be run on Cash out tab and on Open Bets tab
    """
    keep_browser_open = True

    def test_001_go_to_ti_and_set_win_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: Go to TI and set 'WIN' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: * WIN green tick icon is shown for resulted event
        EXPECTED: * 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: * 'Selection Removal' button is shown and clickable for other events
        EXPECTED: * 'CANCEL EDITING' button is shown and clickable
        EXPECTED: * 'CONFIRM' button is shown and NOT clickable
        EXPECTED: *  Est. Returns/Pot. Returns (Coral/Ladbrokes) is shown N/A
        EXPECTED: ![](index.php?/attachments/get/18577359)
        EXPECTED: ![](index.php?/attachments/get/18577358)
        """
        pass

    def test_002_tap_selection_removal_button_to_remove_selection_from_the_betverify_that_new_stake_and_potential_returns_are_shown(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button to remove selection from the bet
        DESCRIPTION: Verify that New Stake and Potential returns are shown
        EXPECTED: New Stake and Est. Returns/Pot. Returns (Coral/Ladbrokes) are shown
        """
        pass

    def test_003_confirm_changesverify_that_the_bet_successfully_edited(self):
        """
        DESCRIPTION: CONFIRM changes
        DESCRIPTION: Verify that the bet successfully edited
        EXPECTED: New edited   bet is shown with appropriate elements"
        EXPECTED: * Bet type is 'SINGLE'
        EXPECTED: On 'Open Bets' tab:
        EXPECTED: * WIN green tick icon is shown for resulted event
        EXPECTED: * 'REMOVED' label is shown for removed bet
        """
        pass

    def test_004_tap_edit_my_acca_button_for_other_placed_in_preconditions_treble_bet(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button for other placed in preconditions TREBLE bet
        EXPECTED: 
        """
        pass

    def test_005_go_to_ti_and_set_void_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: Go to TI and set 'VOID' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: * 'VOID' label is shown for resulted event
        EXPECTED: * 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: * 'Selection Removal' button is shown and clickable for other events
        EXPECTED: * 'CANCEL EDITING' button is shown and clickable
        EXPECTED: * 'CONFIRM' button is shown and NOT clickable
        EXPECTED: * Est. Returns/Pot. Returns (Coral/Ladbrokes) is shown N/A
        EXPECTED: ![](index.php?/attachments/get/18577360)
        EXPECTED: ![](index.php?/attachments/get/18577357)
        """
        pass

    def test_006_tap_selection_removal_button_to_remove_selection_from_the_betverify_that_new_stake_and_potential_returns_are_shown(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button to remove selection from the bet
        DESCRIPTION: Verify that New Stake and Potential returns are shown
        EXPECTED: New Stake and Est. Returns/Pot. Returns (Coral/Ladbrokes) are shown
        """
        pass

    def test_007_confirm_changesverify_that_the_bet_successfully_edited(self):
        """
        DESCRIPTION: CONFIRM changes
        DESCRIPTION: Verify that the bet successfully edited
        EXPECTED: New edited   bet is shown with appropriate elements"
        EXPECTED: * Bet type is 'SINGLE'
        EXPECTED: On 'Open Bets' tab:
        EXPECTED: * 'VOID' label is shown for resulted event
        EXPECTED: * 'REMOVED' label is shown for removed bet
        """
        pass

    def test_008_tap_edit_my_acca_button_for_other_placed_in_preconditions_treble_bet(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button for other placed in preconditions TREBLE bet
        EXPECTED: 
        """
        pass

    def test_009_go_to_ti_and_set_lose_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event_and_error_message_is_displayed_your_acca_is_no_longer_active(self):
        """
        DESCRIPTION: Go to TI and set 'LOSE' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event and error message is displayed "Your Acca is no longer active"
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: * 'LOST' red cross icon is shown for resulted event
        EXPECTED: * 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: * 'Selection Removal' button is NOT shown for other events
        EXPECTED: * Error message is displayed "Your Acca is no longer active"
        EXPECTED: * 'CANCEL EDITING' button is shown and clickable
        EXPECTED: * 'CONFIRM' button is shown and NOT clickable
        EXPECTED: * Est. Returns/Pot. Returns (Coral/Ladbrokes) is shown N/A
        EXPECTED: NOTE: On Cash Out tab the bet will disappear after setting result
        EXPECTED: ![](index.php?/attachments/get/18577362)
        EXPECTED: ![](index.php?/attachments/get/18577363)
        """
        pass
