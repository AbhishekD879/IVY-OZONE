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
class Test_C9346556_Verify_Cancel_Pop_up_in_My_Bet_Acca_edit_mode(Common):
    """
    TR_ID: C9346556
    NAME: Verify 'Cancel' Pop up in 'My Bet/Acca' edit mode
    DESCRIPTION: This test case verifies 'Cancel' message in 'My  Bet/Acca' edit mode
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Bet/Acca' button -> verify that user is in 'My Bet/Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(self):
        """
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        EXPECTED: The selection is removed from their original Acca
        """
        pass

    def test_002_tap_on_cancel_editing_button_and_verify_that_cancel_message_is_not_shown(self):
        """
        DESCRIPTION: Tap on 'Cancel Editing' button and verify that 'Cancel' message is not shown
        EXPECTED: * Cancel message is not shown.
        EXPECTED: * Removed selection is restored.
        EXPECTED: * User is on Openbet /Cashout Tab
        """
        pass

    def test_003_tap_on_edit_my_betacca_buttontap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_accatry_to_navigate_away_from_the_page_click_back_button_bottom_menu_item_my_bets_tabs_etc(self):
        """
        DESCRIPTION: Tap on 'Edit My Bet/Acca' button
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        DESCRIPTION: Try to navigate away from the page (click Back button, bottom menu item, My Bets tabs, etc)
        EXPECTED: Cancel message is shown
        """
        pass

    def test_004_verify_content_of_popup_message(self):
        """
        DESCRIPTION: Verify content of Popup message
        EXPECTED: - Text:
        EXPECTED: 'Do you want to cancel editing?
        EXPECTED: Moving away from this page will cancel changes already made to this bet! Are you sure you want to cancel?'
        EXPECTED: - 'Cancel Edit' button
        EXPECTED: - 'Continue Editing' button
        """
        pass

    def test_005_tap_on_cancel_edit_button_and_verify_that_editing_is_canceled_and_user_is_on_openbet_cashout_tab(self):
        """
        DESCRIPTION: Tap on 'Cancel Edit' button and verify that editing is canceled and user is on Openbet /Cashout Tab
        EXPECTED: Editing is canceled and user is on Openbet /Cashout Tab
        """
        pass

    def test_006_tap_on_continue_editing_button_and_verify_that_popup_is_closed_and_user_continue_editing(self):
        """
        DESCRIPTION: Tap on 'Continue Editing' button and verify that popup is closed and user continue editing
        EXPECTED: 'Continue Editing' should close the pop up and continue editing
        """
        pass
