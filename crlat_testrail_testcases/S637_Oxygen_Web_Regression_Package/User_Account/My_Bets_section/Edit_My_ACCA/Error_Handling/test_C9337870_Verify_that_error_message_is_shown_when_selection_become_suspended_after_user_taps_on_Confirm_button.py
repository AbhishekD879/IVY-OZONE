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
class Test_C9337870_Verify_that_error_message_is_shown_when_selection_become_suspended_after_user_taps_on_Confirm_button(Common):
    """
    TR_ID: C9337870
    NAME: Verify that error message is shown when selection become suspended after user taps on 'Confirm' button
    DESCRIPTION: This test case verifies that error message is shown when selection become suspended after user taps on 'Confirm' button
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: Generate Error text in CMS: CMS System Config Data>EMA
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Navigate to My Bets > Cashout
    PRECONDITIONS: 3. Tap 'EDIT MY ACCA/Bet' button
    """
    keep_browser_open = True

    def test_001_remove_few_selections_from_the_bet(self):
        """
        DESCRIPTION: Remove few selections from the bet
        EXPECTED: - 'UNDO' button is shown for removed selections
        EXPECTED: - 'CONFIRM' button is shown and enabled
        EXPECTED: - Stake and Est. Returns are updated
        """
        pass

    def test_002_tap_confirm_buttonin_the_same_time_suspend_any_eventmarketselection_from_the_bet_in_tiverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message(self):
        """
        DESCRIPTION: Tap 'CONFIRM' button
        DESCRIPTION: In the same time suspend any event/market/selection from the bet in TI
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - Error Message: "text from CMS"
        EXPECTED: - 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: - Disabled 'Selection Removal' buttons for all selections
        EXPECTED: - New Stake and New Est. Returns
        EXPECTED: - 'SUSP CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass

    def test_003_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message_and_removed_selections_are_remembered(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message and removed selections are remembered
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - Error Message: "text from CMS"
        EXPECTED: - 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: - Disabled 'Selection Removal' buttons for all other selections
        EXPECTED: - Original Stake and Est. Returns
        EXPECTED: - 'SUSP CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass
