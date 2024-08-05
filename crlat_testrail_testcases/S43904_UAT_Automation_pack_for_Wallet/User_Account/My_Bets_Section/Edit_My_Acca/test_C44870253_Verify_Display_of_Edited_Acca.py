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
class Test_C44870253_Verify_Display_of_Edited_Acca(Common):
    """
    TR_ID: C44870253
    NAME: Verify Display of Edited Acca
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__open_bets_tabverify_edit_my_bet_button(self):
        """
        DESCRIPTION: Navigate to My Bets > Open bets tab
        DESCRIPTION: Verify 'EDIT MY BET' button
        EXPECTED: EDIT MY BET button is displayed.
        """
        pass

    def test_002_tap_edit_my_bet_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_bet_button(self):
        """
        DESCRIPTION: Tap EDIT My BET button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET' button
        EXPECTED: Edit mode of the ACCA is open
        EXPECTED: 'CANCEL EDITING' button is shown instead of EDIT MY BET button
        """
        pass

    def test_003_select_the_selections_from_acca(self):
        """
        DESCRIPTION: select the selections from ACCA
        EXPECTED: cash out' button change as 'CONFIRM' and text display on the top of 'Confirm' button.
        EXPECTED: Undo button should be displayed when user select the selections.
        """
        pass

    def test_004_tap_on_confirm_button(self):
        """
        DESCRIPTION: Tap on confirm button
        EXPECTED: confirm button changed to timer.
        EXPECTED: user has successfully edited their acca.
        """
        pass

    def test_005_navigate_to_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to settled bets tab
        EXPECTED: settled bets are displayed.
        """
        pass

    def test_006_verify_user_sees_view_of_an_edited_acca_in_settled_bet(self):
        """
        DESCRIPTION: "Verify user sees View of an edited acca in Settled bet"
        EXPECTED: Edited acca displayed when Acca has been edited.
        """
        pass

    def test_007_verify_user_sees_show_edit_history_listing_overlay_and_edited_acca_displayed(self):
        """
        DESCRIPTION: Verify user sees Show Edit History Listing Overlay and edited Acca displayed.
        EXPECTED: should be shown as per Time Order as they were Edited with below details
        EXPECTED: - Bet Type
        EXPECTED: - Original Bet / Edited Bet
        EXPECTED: - Date and Time when the bet was placed is displayed
        EXPECTED: Verify Original Bet / Edited Bet (Edit History Listing Page ),User should be able to see the bet as per below
        EXPECTED: - the selection name is displayed
        EXPECTED: - the market names are displayed
        EXPECTED: - the event name is displayed
        EXPECTED: - Event Date and Time is displayed
        EXPECTED: - Selection Price is displayed when bet was placed
        EXPECTED: - the returns status is displayed
        EXPECTED: - the total stake which was used at the time of bet placement
        EXPECTED: - Receipt ID is displayed
        EXPECTED: - Date and Time of bet placement is displayed
        EXPECTED: - Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: - AND a message <Cashout Value> was used to Edit your bet should be
        """
        pass
