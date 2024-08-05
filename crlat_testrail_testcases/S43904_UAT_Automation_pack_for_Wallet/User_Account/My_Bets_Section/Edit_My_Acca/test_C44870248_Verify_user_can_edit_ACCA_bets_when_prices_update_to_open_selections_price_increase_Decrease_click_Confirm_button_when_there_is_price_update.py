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
class Test_C44870248_Verify_user_can_edit_ACCA_bets_when_prices_update_to_open_selections_price_increase_Decrease_click_Confirm_button_when_there_is_price_update__Check_that_the_new_potential_returns_on_my_acca_page_and_my_bets_Verify_Edit_My_Acca_button_no_longe(Common):
    """
    TR_ID: C44870248
    NAME: "Verify user can edit ACCA bets when prices update to open selections (price increase/Decrease , click Confirm button when there is price update) - Check that the new potential returns on my acca page and my bets.  Verify Edit My Acca button no longe
    DESCRIPTION: "Verify user can edit ACCA bets when prices update to open selections (price increase/Decrease , click Confirm button when there is price update)
    DESCRIPTION: - Check that the new potential returns on my acca page and my bets.
    DESCRIPTION: Verify Edit My Acca button no longer displayed as only one selection remains open
    DESCRIPTION: Verify Display of the Edit My Acca button when any selection is suspended"
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_user_can_edit_acca_bets_when_prices_update_to_open_selections_price_increasedecrease_click_confirm_button_when_there_is_price_update(self):
        """
        DESCRIPTION: Verify user can edit ACCA bets when prices update to open selections (price increase/Decrease, click Confirm button when there is price update)
        EXPECTED: Users should still be able to edit ACCA bets when prices update to open selections (price increase/Decrease, click Confirm button when there is price update)
        """
        pass

    def test_002_after_you_have_edited_an_acca_check_that_the_correct_new_potential_returns_are_shown_for_that_acca_in_my_bets_open_bets(self):
        """
        DESCRIPTION: After you have edited an ACCA, check that the correct New Potential Returns are shown for that ACCA in My Bets->Open Bets
        EXPECTED: You should see correct New Potential Returns for your ACCA in My Bets->Open Bets
        """
        pass

    def test_003_when_all_but_one_selection_in_an_acca_has_not_resulted_in_a_win_verify_that_the_edit_my_acca_button_is_not_seen(self):
        """
        DESCRIPTION: When all but one selection in an ACCA has not resulted in a win, verify that the Edit My ACCA button is not seen
        EXPECTED: When all but one selection in an ACCA has not resulted in a win, the Edit My ACCA button should not be seen
        """
        pass
