import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C9618067_Verify_displaying_Edit_History_Listing_Overlay_of_Settled_Bet(Common):
    """
    TR_ID: C9618067
    NAME: Verify displaying Edit History Listing Overlay of Settled Bet
    DESCRIPTION: This test case verifies the view of Edit History Listing Overlay of Settled Bet
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA7)
    PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 4. Remove few selections from the bet and save changes
    PRECONDITIONS: 5. Tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 6. Remove few selections from the bet and save changes
    PRECONDITIONS: *NOTE:* The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: Ladbrokes has 'EDIT MY ACCA' button
    PRECONDITIONS: Coral has 'EDIT MY BET' button
    """
    keep_browser_open = True

    def test_001_go_to_my_betsopen_betstap_show_edit_history_buttonverify_that_edit_history_listing_overlay_for_the_edited_acca_is_shown_with_all_appropriate_elements(self):
        """
        DESCRIPTION: Go to My Bets>Open Bets
        DESCRIPTION: Tap 'SHOW EDIT HISTORY' button
        DESCRIPTION: Verify that Edit History Listing Overlay for the edited ACCA is shown with all appropriate elements
        EXPECTED: Edit History Listing Overlay is shown with appropriate elements:
        EXPECTED: - "Edit Acca History" title
        EXPECTED: - 'Close' ('X') button
        EXPECTED: - Bet type for all bets
        EXPECTED: - Original Bet box
        EXPECTED: - All Edited Bet boxes
        EXPECTED: - Date and Time when the bet was placed is displayed
        EXPECTED: NOTE: Edited ACCA should be shown as per Time Order as they were Edited
        """
        pass

    def test_002_tap_close_x_buttonverify_that_edit_history_listing_overlay_is_closed(self):
        """
        DESCRIPTION: Tap 'Close' ('X') button
        DESCRIPTION: Verify that Edit History Listing Overlay is closed
        EXPECTED: - Edit History Listing Overlay is closed
        """
        pass

    def test_003_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets(self):
        """
        DESCRIPTION: Make a placed bet (edited bet) SETTLED (add and settle the result for each event in the edited bet)
        DESCRIPTION: Verify that the new bet is resulted and shown on By Bets>(Bet History)Settled Bets
        EXPECTED: - Edited Bet is resulted
        EXPECTED: - Edited Bet is shown on By Bets>(Bet History)Settled Bets
        """
        pass

    def test_004_go_to_by_betsbet_historysettled_bettap_show_edit_history_buttonverify_that_edit_history_listing_overlay_for_the_edited_acca_is_shown_with_all_appropriate_elements(self):
        """
        DESCRIPTION: Go to By Bets>(Bet History)Settled Bet
        DESCRIPTION: Tap 'SHOW EDIT HISTORY' button
        DESCRIPTION: Verify that Edit History Listing Overlay for the edited ACCA is shown with all appropriate elements
        EXPECTED: Edit History Listing Overlay is shown with appropriate elements:
        EXPECTED: - "Edit Acca History" title
        EXPECTED: - 'Close' ('X') button
        EXPECTED: - Bet type for all bets
        EXPECTED: - Original Bet box
        EXPECTED: - All Edited Bet boxes
        EXPECTED: - Date and Time when the bet was placed is displayed
        EXPECTED: NOTE: Edited ACCA should be shown as per Time Order as they were Edited
        """
        pass

    def test_005_tap_close_x_buttonverify_that_edit_history_listing_overlay_is_closed(self):
        """
        DESCRIPTION: Tap 'Close' ('X') button
        DESCRIPTION: Verify that Edit History Listing Overlay is closed
        EXPECTED: - Edit History Listing Overlay is closed
        EXPECTED: - The Settled Bet (Bet History) page is opened
        """
        pass
