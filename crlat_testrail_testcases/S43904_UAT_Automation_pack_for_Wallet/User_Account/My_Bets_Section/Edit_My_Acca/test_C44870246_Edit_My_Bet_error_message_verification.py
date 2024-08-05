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
class Test_C44870246_Edit_My_Bet_error_message_verification(Common):
    """
    TR_ID: C44870246
    NAME: Edit My Bet error message verification
    DESCRIPTION: 
    PRECONDITIONS: Login with User
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

    def test_002_tap_confirm_buttonin_the_same_time_suspend_any_eventmarketselection_from_the_bet_in_tiverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message(self):
        """
        DESCRIPTION: Tap 'CONFIRM' button
        DESCRIPTION: In the same time suspend any event/market/selection from the bet in TI
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: Error Message: "text from CMS"
        EXPECTED: 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: Disabled 'Selection Removal' buttons for all selections
        EXPECTED: New Stake and New Est. Returns
        EXPECTED: 'SUSP CONFIRM' button is disabled
        EXPECTED: 'CANCEL EDITING' is enabled
        """
        pass

    def test_003_verify_the_pop_up_msg(self):
        """
        DESCRIPTION: Verify the pop up msg
        EXPECTED: Leave the EMB page  before confirming EMB, pop up msg should be displayed.
        EXPECTED: Note: Do you want to cancel editing msg should be displayed.
        """
        pass
