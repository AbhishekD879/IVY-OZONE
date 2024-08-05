import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C12834316_Edit_My_ACCA_flow(Common):
    """
    TR_ID: C12834316
    NAME: Edit My ACCA flow
    DESCRIPTION: This test case verifies that user can edit acca bet on My Bets>Cash out tab (Coral only) and Open Bets tab
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS:
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Login into App
    PRECONDITIONS: 3. Place single bet and multiple bet with more than 4 selection (e.g. ACCA 5) (selections should have cash out available)
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: Note: this test case should be run on 'Cash out' and on 'Open Bets' tabs
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashoutopen_bets_tab_for_coralopen_bets_tab_for_ladbrokesverify_that_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_button_is_shown_only_for_multiple_bet_from_preconditions(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout/Open Bets tab (for Coral)/Open Bets tab (for Ladbrokes)
        DESCRIPTION: Verify that 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button is shown only for Multiple bet from preconditions
        EXPECTED: * 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbroke button is shown only for Multiple bet
        EXPECTED: * Stake is shown
        EXPECTED: * Est. Returns is shown
        """
        pass

    def test_002_tap_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_buttonverify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: * Selection details
        EXPECTED: * Event Name
        EXPECTED: * Event Time
        EXPECTED: * Scores (For Inplay Events)
        EXPECTED: * Winning / Losing Arrow (For Inplay Events)
        EXPECTED: * Selection removal button
        EXPECTED: * Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection" is shown as per design
        EXPECTED: * 'Cancel Editing' button
        EXPECTED: * 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: * 'Cash Out' button is NOT shown
        """
        pass

    def test_003_tap_selection_removal_button_for_any_selectionverify_that_selection_removal_button_is_no_longer_displayed_adjacent_to_the_removed_selection(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any selection
        DESCRIPTION: Verify that 'Selection Removal' button is no longer displayed adjacent to the removed selection
        EXPECTED: * 'Selection Removal' button is no longer displayed adjacent to the removed selection
        EXPECTED: * 'Selection Removal' buttons remain displayed adjacent to all other open selections
        EXPECTED: * 'UNDO' button displayed adjacent to the removed selection
        EXPECTED: * 'REMOVED' label for the removed selection
        EXPECTED: * Updated potential returns are displayed
        """
        pass

    def test_004_tap_on_cancel_editing_buttonverify_that_cancel_popup_is_not_shown(self):
        """
        DESCRIPTION: Tap on 'Cancel Editing' button
        DESCRIPTION: Verify that 'Cancel' popup is not shown
        EXPECTED: * Cancel message is not shown.
        EXPECTED: * Removed selection is restored.
        EXPECTED: * User is on Openbet /Cashout Tab
        """
        pass

    def test_005_tap_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_button_and_tap_selection_removal_button_for_more_than_one_selectionverify_that_selection_removal_button_is_no_longer_displayed_adjacent_to_the_removed_selection(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button and Tap 'Selection Removal' button for more than one selection
        DESCRIPTION: Verify that 'Selection Removal' button is no longer displayed adjacent to the removed selection
        EXPECTED: * 'Selection Removal' button is no longer displayed adjacent to the removed selections
        EXPECTED: * 'Selection Removal' buttons remain displayed adjacent to all other open selections
        EXPECTED: * 'UNDO' button displayed adjacent to the removed selections
        EXPECTED: * 'REMOVED' label for the removed selections
        """
        pass

    def test_006_click_on_the_selection_undo_button(self):
        """
        DESCRIPTION: Click on the Selection 'Undo' button
        EXPECTED: * The removed selection is re-displayed
        EXPECTED: * The Selection Removal button is re-displayed adjacent to the selection
        EXPECTED: * Updated potential returns are displayed
        """
        pass

    def test_007_click_the_confirm_buttonverify_that_new_bet_is_placed_on_all_open_remaining_selections_at_their_current_price_spot_price_simultaneously(self):
        """
        DESCRIPTION: Click the 'Confirm' button
        DESCRIPTION: Verify that new bet is placed on all open remaining selections at their current price (spot price) simultaneously
        EXPECTED: * New bet is placed on all open remaining selections at their current price (spot price) simultaneously
        EXPECTED: * NO funds are sent or requested from the users account
        EXPECTED: * message is shown confirming that the edit was successful: "ACCA edited successfully" (Green tick message under cash-out buttin)
        """
        pass

    def test_008_verify_that_new_bet_type_is_shownin_case_the_bet_was_acca4_and_you_removed_1_selection___the_new_bet_type_is_treble(self):
        """
        DESCRIPTION: Verify that new bet type is shown
        DESCRIPTION: (in case the bet was ACCA4 and you removed 1 selection - the new bet type is treble)
        EXPECTED: New bet type is shown
        """
        pass

    def test_009_verify_that_removed_bet_is_shown(self):
        """
        DESCRIPTION: Verify that Removed bet is shown
        EXPECTED: * Removed bet is shown on 'Open Bets' tab
        EXPECTED: * Removed bet is NOT shown on 'Cashout' tab (for Coral only)
        """
        pass

    def test_010_tap_edit_my_acca_button_one_more_timetap_selection_removal_buttons_to_leave_just_one_selection_in_the_betverify_that_the_selection_removal_button_is_not_shown_for_last_selection_is_the_bet(self):
        """
        DESCRIPTION: Tap 'Edit My Acca' button one more time
        DESCRIPTION: Tap 'Selection Removal' buttons to leave just one selection in the bet
        DESCRIPTION: Verify that the 'Selection Removal' button is not shown for last selection is the bet
        EXPECTED: 'Selection Removal' button is not shown for last selection is the bet
        """
        pass

    def test_011_confirm_edittingverify_that_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_button_is_not_shown_any_more_for_this_bet(self):
        """
        DESCRIPTION: Confirm editting
        DESCRIPTION: Verify that 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button is not shown any more for this bet
        EXPECTED: * 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button is not shown
        EXPECTED: * 'Single' bet type is shown for the bet
        """
        pass
