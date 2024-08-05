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
class Test_C12835242_Edit_My_ACCA_when_suspention_happened(Common):
    """
    TR_ID: C12835242
    NAME: 'Edit My ACCA' when suspention happened
    DESCRIPTION: 
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login with User1
    PRECONDITIONS: User1 has 2(two)bets with cash out available placed on ACCA4
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__open_betstap_edit_my_acca_button_for_acca4_betverify_that_selection_removal_buttons_are_displayed_adjacent_to_all_selections_in_the_bet_treble_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        DESCRIPTION: Tap 'EDIT MY ACCA' button for 'ACCA4' bet
        DESCRIPTION: Verify that 'Selection Removal' buttons are displayed adjacent to all selections in the bet TREBLE bets
        EXPECTED: The appropriate elements are shown:
        EXPECTED: * Selection removal buttons for all selection is the bet
        EXPECTED: * Message "Editing this bet Changes the value of Cashout and Odds"
        EXPECTED: * 'CANCEL EDITING' button is shown
        EXPECTED: * 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: * 'Cash Out' button is NOT shown
        """
        pass

    def test_002_tap_selection_removal_button_for_one_of_the_selection_in_the_bet(self):
        """
        DESCRIPTION: Tap 'Selection removal' button for one of the selection in the bet
        EXPECTED: * 'UNDO' button is shown instead of 'Selection Removal' button for removed selection
        EXPECTED: * 'REMOVED' label is shown for removed selection
        EXPECTED: * New Stake' and 'New Est. Returns' (Coral) / 'Potential Returns' (Ladbrokes) are shown (values taken from 'Validate Bet' request)
        """
        pass

    def test_003_stay_in_edit_modein_same_time1_suspend_removed_selection2_suspend_one_of_the_selection_which_was_not_removedverify_that_selection_removal_buttons_become_unclickable_and_the_message_that_section_is_suspended_is_shown(self):
        """
        DESCRIPTION: Stay in edit mode
        DESCRIPTION: In same time
        DESCRIPTION: 1. Suspend removed selection
        DESCRIPTION: 2. Suspend one of the selection which was NOT removed
        DESCRIPTION: Verify that 'Selection Removal' buttons become unclickable and the message that section is suspended is shown
        EXPECTED: The appropriate elements are shown:
        EXPECTED: * 'Undo' button is NOT shown for removed selection
        EXPECTED: * 'REMOVED' label is NOT shown for removed selection
        EXPECTED: * Disabled 'Selection removal' buttons for all selection
        EXPECTED: * Message 'Some of your selections are suspended' is shown instead of message "Editing this bet Changes the value of Cashout and Odds"
        EXPECTED: * Label 'SUSP' is shown for suspended selections
        EXPECTED: * 'CANCEL EDITING' button is shown and clickable
        EXPECTED: * 'SUSP CONFIRM' button is shown and is NOT clickable
        EXPECTED: * 'Cash Out' button is NOT shown
        EXPECTED: *  Original Stake is shown
        EXPECTED: * 'Est. Returns' (Coral) / 'Potential Returns' (Ladbrokes) is shown N/A
        EXPECTED: ![](index.php?/attachments/get/18697405)
        EXPECTED: ![](index.php?/attachments/get/18697407)
        """
        pass

    def test_004_stay_in_edit_modein_same_time_unsuspend_selectiions_which_was_suspendedverify_that_selection_removal_buttons_become_enabled(self):
        """
        DESCRIPTION: Stay in edit mode
        DESCRIPTION: In same time unsuspend selectiions which was suspended
        DESCRIPTION: Verify that 'Selection removal' buttons become enabled
        EXPECTED: * Edit mode is shown with enabled 'Selection Removal' buttons for all selections in the bet
        EXPECTED: * 'SUSP' labels are NOT shown
        EXPECTED: * Message 'Some of your selections are suspended' is NOT shown instead of message "Editing this bet Changes the value of Cashout and Odds"
        EXPECTED: * Original Stake is shown
        EXPECTED: * 'Est. Returns'(Coral) / 'Potential Returns' (Ladbrokes) is shown N/A
        EXPECTED: * 'CONFIRM' button is shown and disabled
        EXPECTED: * 'CANCEL EDITING' button is enabled
        """
        pass

    def test_005_tap_selection_removal_button_for_any_selection_and_confirm_editing(self):
        """
        DESCRIPTION: Tap 'Selection removal' button for any selection and Confirm editing
        EXPECTED: Selection is successfully removed
        """
        pass

    def test_006_provide_same_verifications_with_second_acca4_bet_on_cashout_tab(self):
        """
        DESCRIPTION: Provide same verifications with second 'ACCA4' bet on 'Cashout' tab
        EXPECTED: 
        """
        pass
