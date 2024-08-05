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
class Test_C44870249_After_editing_an_acca_if_user_clicks_on_confirm_when_a_selection_suspended_included_in_acca(Common):
    """
    TR_ID: C44870249
    NAME: "After editing an acca if user clicks on confirm when a selection suspended  included in acca
    DESCRIPTION: 
    PRECONDITIONS: Login with User and place a 4fold or 5fold acca bet
    PRECONDITIONS: Navigate to My Bets > open bets
    PRECONDITIONS: Tap EDIT MY BET button
    """
    keep_browser_open = True

    def test_001_remove_few_selections_from_the_bet(self):
        """
        DESCRIPTION: Remove few selections from the bet
        EXPECTED: 'UNDO' button is shown for removed selections
        EXPECTED: 'CONFIRM' button is shown and enabled
        EXPECTED: Stake and Est. Returns are updated
        """
        pass

    def test_002_suspend_any_eventmarketselectionin_acca_from_the_bet_in_tiverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message(self):
        """
        DESCRIPTION: Suspend any event/market/selection(in acca) from the bet in TI
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: Disabled 'Selection Removal' buttons for all selections
        EXPECTED: 'CANCEL EDITING'is enabled and able to click that
        EXPECTED: New stake and New estimated results are displayed
        """
        pass

    def test_003_verify_grey_suspended(self):
        """
        DESCRIPTION: Verify grey suspended
        EXPECTED: Edit My Acca button is not click-able when any selection is suspended
        """
        pass
