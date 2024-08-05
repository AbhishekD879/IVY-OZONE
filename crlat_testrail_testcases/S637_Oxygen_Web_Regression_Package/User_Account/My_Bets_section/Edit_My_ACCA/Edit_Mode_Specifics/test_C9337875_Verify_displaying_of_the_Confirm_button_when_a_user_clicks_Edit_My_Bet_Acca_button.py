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
class Test_C9337875_Verify_displaying_of_the_Confirm_button_when_a_user_clicks_Edit_My_Bet_Acca_button(Common):
    """
    TR_ID: C9337875
    NAME: Verify displaying of the Confirm button when a user clicks Edit My Bet/Acca button
    DESCRIPTION: This test case verifies displaying of the Confirm button when a user clicks Edit My Acca button
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_tap_on_on_single_line_accumulator_edit_my_betacca_button(self):
        """
        DESCRIPTION: Tap on on Single line accumulator 'Edit My Bet/Acca' button
        EXPECTED: User is navigated to My Bet/Acca Edit mode
        """
        pass

    def test_002_verify_that_confirm_button_is_displayed_and_non_click_able(self):
        """
        DESCRIPTION: Verify that 'Confirm' button is displayed and non-click-able
        EXPECTED: 'Confirm' button is displayed and non-click-able
        """
        pass

    def test_003_verify_that_cancel_editing_button_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify that 'Cancel Editing' button is displayed and clickable
        EXPECTED: 'Cancel Editing' button is displayed and clickable.
        """
        pass

    def test_004_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(self):
        """
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        EXPECTED: The selection is removed from their original Acca
        """
        pass

    def test_005_verify_that_the_confirm_button_is_displayed_and_click_able(self):
        """
        DESCRIPTION: Verify that the Confirm button is displayed and click-able
        EXPECTED: The 'Confirm' button is displayed and click-able
        """
        pass
