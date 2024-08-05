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
class Test_C2351458_To_edit_according_to_BMA_48153_add_case_for_Desktop_Verify_displaying_numeric_keyboard_for_one_selection(Common):
    """
    TR_ID: C2351458
    NAME: [To edit according to BMA-48153; add case for Desktop] Verify displaying numeric keyboard for one selection
    DESCRIPTION: TO EDIT: Also should be added a case for Desktop
    DESCRIPTION: This test case verifies displaying numeric keyboard for one selection in Betslip
    DESCRIPTION: Applies for Mobile only
    DESCRIPTION: AUTOTEST: [C9698026]
    DESCRIPTION: Note: On OX100 Key pad should not open by default  BMA-45311
    PRECONDITIONS: - Oxygen application is loaded on Mobile device
    PRECONDITIONS: - One selection is added to the Betslip
    PRECONDITIONS: - Betslip is opened
    """
    keep_browser_open = True

    def test_001_verify_stake_box(self):
        """
        DESCRIPTION: Verify 'Stake' box
        EXPECTED: - 'Stake' box is highlighted
        EXPECTED: - '<currency symbol>' is shown within 'Stake' box by default
        EXPECTED: From OX 100:
        EXPECTED: -'Stake' box is not focused, Stake text is displayed in 'Stake' box
        """
        pass

    def test_002_verify_availability_of_numeric_keyboard(self):
        """
        DESCRIPTION: Verify availability of numeric keyboard
        EXPECTED: Numeric keyboard is available
        EXPECTED: From OX 100:
        EXPECTED: - Numeric keyboard is NOT available above 'BET NOW'/'LOG IN & BET' button
        """
        pass

    def test_003_tap_somewhere_outside_stake_box_or_tap_return_button_on_keyboardvalid_for_ox98_only(self):
        """
        DESCRIPTION: Tap somewhere outside 'Stake' box OR tap 'Return' button on keyboard
        DESCRIPTION: (valid for OX98 only)
        EXPECTED: - 'Stake' box is NOT focused
        EXPECTED: - '<currency symbol> 0.00' is shown within 'Stake' box (After OX99 'Stake' is shown within 'Stake' box
        EXPECTED: - Numeric keyboard is NOT shown
        """
        pass

    def test_004_add_one_more_selection_to_betslip(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        EXPECTED: - Added selection is displayed on Bet Slip
        EXPECTED: - Numeric keyboard is NOT shown
        """
        pass

    def test_005_remove_one_selection_or_close_betslip_and_unselect_selected_odds_button(self):
        """
        DESCRIPTION: Remove one selection OR close Betslip and unselect selected 'Odds' button
        EXPECTED: - Betslip content is reloaded
        EXPECTED: - One selection is displayed on Bet Slip
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: From OX 100:
        EXPECTED: - Numeric keyboard is NOT available above 'BET NOW'/'LOG IN & BET' button
        """
        pass
