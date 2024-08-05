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
class Test_C44870245_Verify_edited_ACCA_displayed_in_the_openbet(Common):
    """
    TR_ID: C44870245
    NAME: Verify edited ACCA displayed in the openbet.
    DESCRIPTION: 
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
        EXPECTED: cash out' button change as 'CONFIRM'  and text display on the top of 'Confirm' button.
        """
        pass

    def test_003_select_the_selections_from_acca(self):
        """
        DESCRIPTION: select the selections from ACCA
        EXPECTED: Undo button should be displayed when user select the selections.
        """
        pass

    def test_004_tap_on_confirm_button(self):
        """
        DESCRIPTION: Tap on confirm button
        EXPECTED: user has successfully edited their acca.
        """
        pass

    def test_005_verify_the_my_betsopen_bets_area_after_remove_the_selections(self):
        """
        DESCRIPTION: verify the my bets(open bets) area after remove the selections
        EXPECTED: The new bet type name is displayed.
        EXPECTED: The selection(s) which were removed have a Removed token displayed
        EXPECTED: Removed selections should appear below Open selections
        EXPECTED: The changed stake is displayed.
        EXPECTED: odds are displayed for any selections
        EXPECTED: The new potential returns are displayed
        """
        pass
