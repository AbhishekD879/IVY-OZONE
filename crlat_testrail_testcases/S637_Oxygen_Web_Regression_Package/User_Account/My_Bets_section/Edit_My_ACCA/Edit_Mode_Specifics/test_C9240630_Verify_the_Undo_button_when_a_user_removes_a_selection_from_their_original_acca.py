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
class Test_C9240630_Verify_the_Undo_button_when_a_user_removes_a_selection_from_their_original_acca(Common):
    """
    TR_ID: C9240630
    NAME: Verify the 'Undo' button when a user removes a selection from their original acca
    DESCRIPTION: This test case verifies displaying of the Selection 'Undo' button when a user removes a selection from their original acca
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Verify that 'Edit My Bet/Edit My ACCA' button is available on both Cashout and My Bets (Open Bets)
    PRECONDITIONS: Tap on 'Edit My Bet/Edit My ACCA' button: need to verify on both  Cashout and My Bets (Open Bets)
    PRECONDITIONS: NOTE: 'Edit My ACCA/BET' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_tap_on_edit_my_betedit_my_acca_button_on_cashout_tab(self):
        """
        DESCRIPTION: Tap on 'Edit My Bet/Edit My ACCA' button on Cashout tab
        EXPECTED: The Selection Removal sign "X" appears next to all selections of ACCA
        """
        pass

    def test_002_tap_on_a_selection_removal_button_xto_remove_the_selection_from_the_original_acca_on_cashout(self):
        """
        DESCRIPTION: Tap on a Selection Removal button ('X')to remove the selection from the original Acca on Cashout
        EXPECTED: The selection is removed from ACCA and the "Undo" button is displayed next to it
        """
        pass

    def test_003_verify_the_name_of_the_removed_selection(self):
        """
        DESCRIPTION: Verify the name of the removed selection
        EXPECTED: The removed selection is marked as "Removed" next to selection name
        """
        pass

    def test_004_tap_on_the_undo_button(self):
        """
        DESCRIPTION: Tap on the 'UNDO' button
        EXPECTED: The selection is added back to the ACCA and the Selection Removal sign "X" appears next to it
        """
        pass

    def test_005_repeat_steps_2_4_on_my_bets_open_bets(self):
        """
        DESCRIPTION: Repeat steps 2-4 on My Bets (Open Bets)
        EXPECTED: The "UNDO" button works accordingly
        """
        pass
