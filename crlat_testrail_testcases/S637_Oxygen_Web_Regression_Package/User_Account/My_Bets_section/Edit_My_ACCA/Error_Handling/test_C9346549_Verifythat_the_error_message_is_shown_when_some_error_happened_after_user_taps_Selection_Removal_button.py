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
class Test_C9346549_Verifythat_the_error_message_is_shown_when_some_error_happened_after_user_taps_Selection_Removal_button(Common):
    """
    TR_ID: C9346549
    NAME: Verifythat the error message is shown when some error happened after user taps 'Selection Removal' button
    DESCRIPTION: This test case verifies that error is shown when some error happened after user taps 'Selection Removal' button
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: Generate Error text in CMS: CMS System Config Data>EMA
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Navigate to My Bets > Cashout
    PRECONDITIONS: Tap 'EDIT MY ACCA' button
    PRECONDITIONS: Uncheck 'Cash out' in TI for any event in the bet (to generate Validbet / reqBetBuild or reqBetPlace error)
    """
    keep_browser_open = True

    def test_001_tap_selection_removal_button_for_any_selectionverify_that_an_error_message_is_shown_and_selection_is_not_removed(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any selection
        DESCRIPTION: Verify that an error message is shown and selection is not removed
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - Error message "text from CMS" is shown
        EXPECTED: - Selection is not removed
        EXPECTED: - 'CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' button is enabled
        """
        pass

    def test_002_provide_same_verification_on_my_bets__open_bets_tabverify_that_an_error_message_is_shown_and_selection_is_not_removed(self):
        """
        DESCRIPTION: Provide same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that an error message is shown and selection is not removed
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - Error message "text from CMS" is shown
        EXPECTED: - Selection is not removed
        EXPECTED: - 'CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' button is enabled
        """
        pass
