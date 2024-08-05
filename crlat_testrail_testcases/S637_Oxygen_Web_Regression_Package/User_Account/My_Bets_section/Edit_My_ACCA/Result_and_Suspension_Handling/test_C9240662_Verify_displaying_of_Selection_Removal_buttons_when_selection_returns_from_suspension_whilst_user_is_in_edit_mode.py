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
class Test_C9240662_Verify_displaying_of_Selection_Removal_buttons_when_selection_returns_from_suspension_whilst_user_is_in_edit_mode(Common):
    """
    TR_ID: C9240662
    NAME: Verify displaying of Selection Removal buttons when selection returns from suspension whilst user is in edit mode
    DESCRIPTION: This test case verifies that Selection Removal buttons on all selections become clickable in case  selection returns from suspension whilst user is in edit mode
    PRECONDITIONS: Login with User1
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on TREBLE
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
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
        EXPECTED: - Label 'SUSPENDED' **[From OX99]** label 'SUSP' is shown for suspended selection
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' **[From OX99]** 'Cash Out Suspended' button is NOT shown
        """
        pass

    def test_005_navigate_to_ti_and_unsuspend_eventmarketselection_wich_was_suspended_in_step3(self):
        """
        DESCRIPTION: Navigate to TI and unsuspend event/market/selection wich was suspended in step3
        EXPECTED: The selection event/market/selection is active
        """
        pass

    def test_006_navigate_back_to_the_applicationverify_that_selection_removal_buttons_become_clickable_and_the_message_that_section_is_suspended_is_not_shown(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that 'Selection Removal' buttons become clickable and the message that section is suspended is NOT shown
        EXPECTED: The appropriate elements are shown:
        EXPECTED: - Enabled 'Selection removal' buttons for all selection is the bet
        EXPECTED: - Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection"
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' button is shown
        """
        pass

    def test_007_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_selection_removal_buttons_become_clickable_when_selection_returns_from_suspension(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that 'Selection Removal' buttons become clickable when selection returns from suspension
        EXPECTED: - 'Selection removal' buttons become clickable for all selection
        EXPECTED: - Message 'Some of your selections are suspended is NOT shown
        """
        pass
