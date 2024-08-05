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
class Test_C9602560_Verify_that_the_error_message_is_shown_when_some_error_happened_after_user_taps_Confirm_button(Common):
    """
    TR_ID: C9602560
    NAME: Verify that the error message is shown when some error happened after user taps 'Confirm' button
    DESCRIPTION: This test case verifies that error is shown when some error happened after user taps 'Confirm' button
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: Generate Error text in CMS: CMS System Config Data>EMA
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Navigate to My Bets > Cashout
    PRECONDITIONS: Tap 'EDIT MY ACCA' button
    PRECONDITIONS: Remove any selection
    PRECONDITIONS: Uncheck 'Cash Out' in TI for any event fro the bet (to generate Validbet / reqBetBuild or reqBetPlace error)
    """
    keep_browser_open = True

    def test_001_tap_confirm_buttonverify_that_edit_mode_is_remains_opened_with_an_error_message_and_confirm_button_is_clickable(self):
        """
        DESCRIPTION: Tap 'CONFIRM' button
        DESCRIPTION: Verify that edit mode is remains opened with an error message and 'Confirm' button is clickable
        EXPECTED: - Edit mode is remains opened
        EXPECTED: - Error message 'text from CMS' is shown
        EXPECTED: - 'CONFIRM' button is clickable
        EXPECTED: - 'CANCEL EDITING' button is clickable
        """
        pass

    def test_002_provide_same_verification_on_my_bets__open_bets_tabverify_that_edit_mode_is_remains_opened_with_an_error_message_and_confirm_button_is_clickable(self):
        """
        DESCRIPTION: Provide same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that edit mode is remains opened with an error message and 'Confirm' button is clickable
        EXPECTED: - Edit mode is remains opened
        EXPECTED: - Error message 'text from CMS' is shown
        EXPECTED: - 'CONFIRM' button is clickable
        EXPECTED: - 'CANCEL EDITING' button is clickable
        """
        pass
