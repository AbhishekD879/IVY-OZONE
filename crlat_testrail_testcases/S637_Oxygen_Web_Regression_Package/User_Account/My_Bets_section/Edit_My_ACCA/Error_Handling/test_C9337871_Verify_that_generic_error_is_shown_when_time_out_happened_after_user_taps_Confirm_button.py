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
class Test_C9337871_Verify_that_generic_error_is_shown_when_time_out_happened_after_user_taps_Confirm_button(Common):
    """
    TR_ID: C9337871
    NAME: Verify that generic error is shown when time out happened after user taps 'Confirm' button
    DESCRIPTION: This test case verifies that generic error to try again is shown when time out happened after user taps 'Confirm' button
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: Generate Error text in CMS: CMS System Config Data>EMA
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Navigate to My Bets > Cashout
    PRECONDITIONS: Tap 'EDIT MY ACCA' button
    PRECONDITIONS: Ask dev to generate time-out from any application during validation  or block place bet request
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

    def test_002_tap_confirm_buttonin_the_same_time_generate_time_out_during_validationverify_that_spinner_is_shown_and_edit_mode_is_opened_with_an_error_message_to_try_again(self):
        """
        DESCRIPTION: Tap 'CONFIRM' button
        DESCRIPTION: In the same time generate time-out during validation
        DESCRIPTION: Verify that spinner is shown and edit mode is opened with an error message 'to try again'
        EXPECTED: - Error Message: "text from CMS" is shown
        EXPECTED: - Removed selection with 'UNDO' button is shown
        EXPECTED: - 'CONFIRM ' button is shown and enabled
        EXPECTED: - New Stake and New Potential Returns are shown
        EXPECTED: - 'CANCEL EDITING' button is shown and enabled
        """
        pass

    def test_003_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_spinner_is_shown_and_edit_mode_is_opened_with_an_error_message_to_try_again(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that spinner is shown and edit mode is opened with an error message 'to try again'
        EXPECTED: - Error Message: "text from CMS" is shown
        EXPECTED: - Removed selection with 'UNDO' button is shown
        EXPECTED: - 'CONFIRM ' button is shown and enabled
        EXPECTED: - New Stake and New Potential Returns are shown
        EXPECTED: - 'CANCEL EDITING' button is shown and enabled
        """
        pass
