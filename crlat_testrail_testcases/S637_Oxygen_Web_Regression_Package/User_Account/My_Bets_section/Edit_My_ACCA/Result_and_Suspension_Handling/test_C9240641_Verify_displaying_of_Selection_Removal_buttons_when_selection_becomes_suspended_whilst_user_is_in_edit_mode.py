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
class Test_C9240641_Verify_displaying_of_Selection_Removal_buttons_when_selection_becomes_suspended_whilst_user_is_in_edit_mode(Common):
    """
    TR_ID: C9240641
    NAME: Verify displaying of Selection Removal buttons when selection becomes suspended whilst user is in edit mode
    DESCRIPTION: This test case verifies that Selection Removal buttons on all selections become unclickable in case one of the selection is suspended whilst user is in edit mode
    PRECONDITIONS: Login with User1
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on TREBLE
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: NOTE: The verifications should be done in 'List View' and in 'Card View'
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashoutverify_that_edit_my_acca_button_and_event_details_are_shown_for_treble_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY ACCA' button and event details are shown for TREBLE bets
        EXPECTED: 'EDIT MY ACCA' button is shown for TREBLE bet
        """
        pass

    def test_002_tap_edit_my_acca_button_for_the_first_betverify_that_selection_removal_buttons_are_displayed_adjacent_to_all_selections_in_the_bet(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button for the first bet
        DESCRIPTION: Verify that 'Selection Removal' buttons are displayed adjacent to all selections in the bet
        EXPECTED: The appropriate elements are shown:
        EXPECTED: - Selection removal buttons for all selection is the bet
        EXPECTED: - Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection"
        EXPECTED: - 'CANCEL EDITING' button is shown
        EXPECTED: - 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' button is NOT shown
        """
        pass

    def test_003_navigate_to_ti_and_suspend_one_of_eventmarketselection_from_the_bet(self):
        """
        DESCRIPTION: Navigate to TI and suspend one of event/market/selection from the bet
        EXPECTED: The selection event/market/selection is suspended
        """
        pass

    def test_004_navigate_back_to_the_applicationverify_that_selection_removal_buttons_become_unclickable_and_the_message_that_section_is_suspended_is_shown(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that 'Selection Removal' buttons become unclickable and the message that section is suspended is shown
        EXPECTED: The appropriate elements are shown:
        EXPECTED: - Disabled 'Selection removal' buttons for all selection
        EXPECTED: - Message 'Some of your selections are suspended' is shown instead of message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection"
        EXPECTED: - Label 'SUSPENDED' **[from OX99]** label 'SUSP' is shown for suspended selection
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'SUSP CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' button is NOT shown
        """
        pass

    def test_005_tap_cancel_editing_buttonverify_that_edit_mode_is_closed_and_edit_my_acca_button_disabled(self):
        """
        DESCRIPTION: Tap 'CANCEL EDITING' button
        DESCRIPTION: Verify that edit mode is closed and 'EDIT MY ACCA' button disabled
        EXPECTED: - Edit mode is closed
        EXPECTED: - 'EDIT MY ACCA' button is shown and disabled
        EXPECTED: - Label 'SUSPENDED' **[from OX99]** label 'SUSP' is shown for suspended selection
        EXPECTED: - 'Cash Out' **[from OX99]** 'cash out suspended' button is shown and NOT clickable
        """
        pass

    def test_006_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_selection_removal_buttons_become_unclickable_and_the_message_that_section_is_suspended_is_shown_in_case_one_of_the_selection_in_the_bet_become_suspended(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that 'Selection Removal' buttons become unclickable and the message that section is suspended is shown in case one of the selection in the bet become suspended
        EXPECTED: - 'Selection Removal' buttons become unclickable
        EXPECTED: - Message 'Some of your selections are suspended is shown
        """
        pass
