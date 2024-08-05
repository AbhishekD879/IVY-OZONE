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
class Test_C3020310_Verify_that_Edit_My_ACCA_Edit_My_Bet_button_is_greyed_outdisabled_in_case_any_ACCA_selection_is_suspended(Common):
    """
    TR_ID: C3020310
    NAME: Verify that 'Edit My ACCA/Edit My Bet' button is greyed out(disabled) in case any ACCA selection is suspended
    DESCRIPTION: This test case verifies that the 'EDIT MY ACCA/Bet' button is greyed out(disabled)  and the button is NOT clickable.
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add 3 (three) selections to Betslip and place a bet on TREBLE and SINGLES
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashout_and_open_betsverify_that_edit_my_betedit_my_acca_button_is_shown_for_treble_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout and Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE only
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for TREBLE bet
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_002_suspended_one_of_the_selections_of_the_treble_in_backoffice(self):
        """
        DESCRIPTION: Suspended one of the selections of the TREBLE in Backoffice
        EXPECTED: Selection is suspended
        """
        pass

    def test_003_navigate_to_my_bets__cashout(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        EXPECTED: The cashout page is displayed
        """
        pass

    def test_004_verify_that_the_edit_my_accabet_button_is_greyed_out_disabled_and_the_button_is_not_clickable(self):
        """
        DESCRIPTION: Verify that the 'EDIT MY ACCA/Bet' button is greyed out (disabled) and the button is NOT clickable
        EXPECTED: - Grey (disabled) 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is NOT clickable
        EXPECTED: - Suspended selection is greyed out and has 'SUSP' label
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        pass

    def test_005_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        EXPECTED: The Open bets tab is displayed
        """
        pass

    def test_006_verify_that_the_edit_my_betedit_my_acca_button_is_greyed_out_disabled_and_the_button_is_not_clickable(self):
        """
        DESCRIPTION: Verify that the 'EDIT MY BET/EDIT MY ACCA' button is greyed out (disabled) and the button is NOT clickable
        EXPECTED: - Grey (disabled) 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE
        EXPECTED: - 'EDIT MY ACCA/Bet' button is NOT clickable
        EXPECTED: - Suspended selection is greyed out and has 'SUSP' label
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        pass
