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
class Test_C3020281_Verify_that_Edit_My_ACCA_button_is_not_shown_in_case_only_one_selection_remains_open(Common):
    """
    TR_ID: C3020281
    NAME: Verify that 'Edit My ACCA' button is not shown in case only one selection remains open
    DESCRIPTION: This test case verifies that 'EDIT MY ACCA' button is NOT displaying when the bet on an ACCA is placed and only one selection remains open
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add 3 (three) selections to Betslip and place a bet on TREBLE and SINGLES
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_for_treble_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE only
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for TREBLE bet
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_002_click_on_edit_my_betedit_my_acca_buttondelete_one_of_the_selections_and_confirm_changes_or_add_a_result_in_tinavigate_back_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_for_double_only(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Delete one of the selections and confirm changes OR add a result in TI
        DESCRIPTION: Navigate back to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for DOUBLE only
        EXPECTED: - Two selections remained in edited ACCA
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_003_navigate_back_to_my_bets__open_betsverify_that_edit_my_betedit_my_acca_button_is_shown_for_double_only(self):
        """
        DESCRIPTION: Navigate back to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for DOUBLE only
        EXPECTED: - Two selections remained in edited ACCA
        EXPECTED: - Removed selection is shown and marked as 'REMOVED'
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_004_click_on_edit_my_betedit_my_acca_button_one_more_timedelete_one_of_the_selections_and_confirm_changes_or_add_a_result_in_tinavigate_back_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_edited_acca(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button one more time
        DESCRIPTION: Delete one of the selections and confirm changes OR add a result in TI
        DESCRIPTION: Navigate back to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for the edited ACCA
        EXPECTED: - ONE selection remained in edited ACCA
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for SINGLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_005_navigate_back_to_my_bets__open_betsverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_edited_acca(self):
        """
        DESCRIPTION: Navigate back to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for the edited ACCA
        EXPECTED: - ONE selection remained in edited ACCA
        EXPECTED: - Two removed selections are shown and marked as 'REMOVED'
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for SINGLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        pass
