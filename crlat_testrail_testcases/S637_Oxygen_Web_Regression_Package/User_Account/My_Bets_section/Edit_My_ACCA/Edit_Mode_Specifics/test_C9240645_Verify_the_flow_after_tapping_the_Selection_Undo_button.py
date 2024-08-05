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
class Test_C9240645_Verify_the_flow_after_tapping_the_Selection_Undo_button(Common):
    """
    TR_ID: C9240645
    NAME: Verify the flow after tapping the Selection 'Undo' button
    DESCRIPTION: This test case verifies the flow after tapping the Selection 'Undo' button
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    DESCRIPTION: AUTOTEST [C12808056]
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place a Multiple bet
    PRECONDITIONS: Navigate to the Bet History from the Right/User menu
    PRECONDITIONS: Verify that 'Edit My Bet/Edit My ACCA' button is available on both Cashout and My Bets (Open Bets)
    PRECONDITIONS: Tap on 'Edit My Bet/Edit My ACCA' button
    PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which are placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4, etc)
    """
    keep_browser_open = True

    def test_001_tap_on_a_selection_removal_button_x(self):
        """
        DESCRIPTION: Tap on a Selection Removal button ('X')
        EXPECTED: The selection is removed from the original Acca
        EXPECTED: The 'Undo' button is displayed next to the removed selection
        """
        pass

    def test_002_click_on_the_selection_undo_button(self):
        """
        DESCRIPTION: Click on the Selection 'Undo' button
        EXPECTED: The removed selection is re-displayed
        """
        pass

    def test_003_verify_that_the_selection_removal_button_is_re_displayed_adjacent_to_the_selection(self):
        """
        DESCRIPTION: Verify that the Selection Removal button is re-displayed adjacent to the selection
        EXPECTED: The Selection Removal button is re-displayed adjacent to the selection
        """
        pass

    def test_004_verify_that_the_updated_potential_returns_are_displayed(self):
        """
        DESCRIPTION: Verify that the updated potential returns are displayed
        EXPECTED: The potential returns are updating accordingly
        """
        pass
