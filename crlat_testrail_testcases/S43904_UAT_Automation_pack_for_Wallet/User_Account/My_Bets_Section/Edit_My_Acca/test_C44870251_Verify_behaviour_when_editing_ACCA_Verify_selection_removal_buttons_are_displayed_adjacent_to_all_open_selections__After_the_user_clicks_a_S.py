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
class Test_C44870251_Verify_behaviour_when_editing_ACCA_Verify_selection_removal_buttons_are_displayed_adjacent_to_all_open_selections__After_the_user_clicks_a_Selection_Removal_button_then_the_selection_removal_button_is_no_longer_displayed__the_selection_removal_bu(Common):
    """
    TR_ID: C44870251
    NAME: "Verify behaviour when editing ACCA -Verify selection removal buttons are displayed adjacent to all open selections - After the user clicks a Selection Removal button then the selection removal button is no longer displayed - the selection removal bu
    DESCRIPTION: "Verify behaviour when editing ACCA
    DESCRIPTION: -Verify selection removal buttons are displayed adjacent to all open selections
    DESCRIPTION: - After the user clicks a Selection Removal button then the selection removal button is no longer displayed
    DESCRIPTION: - the selection removal button for the last open selection should become non-clickable
    DESCRIPTION: - When the user clicks on Edit My Bet, Confirm button is displayed but it is non-clickable
    DESCRIPTION: - When the user clicks on Selection Removal button, confirm button is displayed and is clickable
    DESCRIPTION: -  When user clicks on confirm button successful confirmation message is displayed
    DESCRIPTION: - Tapping on Cancel Edit should cancel the editing and bring user to the Openbet /Cashout Tab
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__open_bets_tabverify_edit_my_bet_button(self):
        """
        DESCRIPTION: Navigate to My Bets > Open bets tab
        DESCRIPTION: Verify 'EDIT MY BET' button
        EXPECTED: EDIT MY BET button is displayed.
        """
        pass

    def test_002_tap_edit_my_bet_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_bet_button(self):
        """
        DESCRIPTION: Tap EDIT My BET button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET' button
        EXPECTED: Edit mode of the ACCA is open
        EXPECTED: 'CANCEL EDITING' button is shown instead of EDIT MY BET button
        """
        pass

    def test_003_verify_selection_removal_buttons_are_displayed_adjacent_to_all_open_selections(self):
        """
        DESCRIPTION: Verify selection removal buttons are displayed adjacent to all open selections
        EXPECTED: Removal buttons should be available for all open selections
        """
        pass

    def test_004_after_the_user_clicks_a_selection_removal_button_and_verify_if_undo_button_is_displayed(self):
        """
        DESCRIPTION: After the user clicks a Selection Removal button and verify if UNDO button is displayed.
        EXPECTED: UNDO button is displayed when the user clicks on the Selection removal button
        """
        pass

    def test_005_verify_that_the_selection_removal_button_for_the_last_open_selection_should_become_non_clickable(self):
        """
        DESCRIPTION: Verify that the selection removal button for the last open selection should become non-clickable
        EXPECTED: The selection removal button for the last open selection should be non-clickable
        """
        pass

    def test_006_when_the_user_clicks_on_selection_removal_button_confirm_button_is_displayed_and_is_clickable(self):
        """
        DESCRIPTION: When the user clicks on Selection Removal button, confirm button is displayed and is clickable
        EXPECTED: The confirm button should be displayed and clickable
        """
        pass

    def test_007_when_user_clicks_on_confirm_button_verify_that_the_successful_confirmation_message_is_displayed(self):
        """
        DESCRIPTION: When user clicks on confirm button, verify that the successful confirmation message is displayed
        EXPECTED: The successful confirmation message should be seen
        """
        pass

    def test_008_tapping_on_cancel_edit_should_cancel_the_editing_and_bring_user_to_the_openbet_cashout_tab(self):
        """
        DESCRIPTION: Tapping on Cancel Edit should cancel the editing and bring user to the Openbet /Cashout Tab
        EXPECTED: The edit should be cancelled and the user is on the Openbet/Cashout tab
        """
        pass
