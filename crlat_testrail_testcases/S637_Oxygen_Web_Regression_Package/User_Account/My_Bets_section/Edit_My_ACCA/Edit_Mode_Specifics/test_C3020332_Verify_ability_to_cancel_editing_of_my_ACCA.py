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
class Test_C3020332_Verify_ability_to_cancel_editing_of_my_ACCA(Common):
    """
    TR_ID: C3020332
    NAME: Verify ability to cancel editing of my ACCA
    DESCRIPTION: This test case verifies that edit my ACCA can be canceled
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a bet on DOUBLE
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashout_tabverify_that_edit_my_bet_coraledit_my_acca_ladbrokes_buttonis_shown_for_double_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout tab
        DESCRIPTION: Verify that 'EDIT MY BET' (Coral)/EDIT MY ACCA' (Ladbrokes) button
        DESCRIPTION: is shown for DOUBLE only
        EXPECTED: 'EDIT MY BET' (Coral)/EDIT MY ACCA' (Ladbrokes) button is shown only for DOUBLE bet
        """
        pass

    def test_002_tap_edit_my_betacca_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_betacca_button(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET/ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        EXPECTED: - Edit mode of the ACCA is open
        EXPECTED: - CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        """
        pass

    def test_003_tap_cancel_editing_buttonverify_that_user_returned_back_to_the_not_edit_mode(self):
        """
        DESCRIPTION: Tap 'CANCEL EDITING' button
        DESCRIPTION: Verify that user returned back to the not edit mode
        EXPECTED: - Cashout page is opened
        EXPECTED: - Edit mode of the ACCA is closed
        EXPECTED: - 'EDIT MY BET/ACCA' button is shown
        """
        pass

    def test_004_navigate_to_my_bets__open_bets_tabverify_that_edit_my_betacca_button_is_shown_for_double_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets tab
        DESCRIPTION: Verify that 'EDIT MY BET/ACCA' button is shown for DOUBLE only
        EXPECTED: 'EDIT MY BET/ACCA' button is shown only for DOUBLE bet
        """
        pass

    def test_005_tap_edit_my_betacca_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_betacca_button(self):
        """
        DESCRIPTION: Tap ''EDIT MY BET/ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        EXPECTED: - Edit mode of the ACCA is open
        EXPECTED: - 'CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        """
        pass

    def test_006_tap_cancel_editing_buttonverify_that_user_returned_back_to_the_not_edit_mode(self):
        """
        DESCRIPTION: Tap 'CANCEL EDITING' button
        DESCRIPTION: Verify that user returned back to the not edit mode
        EXPECTED: - Cashout page is opened
        EXPECTED: - Edit mode of the ACCA is closed
        EXPECTED: - ''EDIT MY BET/ACCA' button is shown
        """
        pass
