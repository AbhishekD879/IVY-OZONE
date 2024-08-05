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
class Test_C3020263_Verify_that_Edit_My_ACCA_button_is_displaying(Common):
    """
    TR_ID: C3020263
    NAME: Verify that 'Edit My ACCA' button is displaying
    DESCRIPTION: This test case verifies that ''Edit My Bet/Edit My ACCA' button is displaying when the bet on an ACCA is placed and two or more selections are open and all of selections are active
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add 2 (two) selections to Betslip and Place a bet for DOUBLE and SINGLES (Bet1)
    PRECONDITIONS: Add 3 (three) selections to Betslip and place a bet on TREBLE, DOUBLE, TRIXIE and SINGLES (Bet2)
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_only_for_double_from_bet1_and_treble_from_bet2(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2)
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2) bets
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_002_click_on_edit_my_betedit_my_acca_buttonverify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: - Edit mode of the Acca is shown
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button changes to the 'CANCEL EDITING' button
        """
        pass

    def test_003_navigate_to_my_bets__open_betsverify_that_edit_my_betedit_my_acca_button_is_shown_only_for_double_from_bet1_and_treble_from_bet2(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2)
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2) bets
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns (**Coral**)/ Potential Returns(**Ladbrokes**) is shown
        """
        pass

    def test_004_click_on_edit_my_betedit_my_acca_buttonverify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: - Edit mode of the Acca is shown
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button changes to the 'CANCEL EDITING' button
        """
        pass
