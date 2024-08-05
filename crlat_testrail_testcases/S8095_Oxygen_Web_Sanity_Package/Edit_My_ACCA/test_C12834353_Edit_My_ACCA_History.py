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
class Test_C12834353_Edit_My_ACCA_History(Common):
    """
    TR_ID: C12834353
    NAME: Edit My ACCA History
    DESCRIPTION: This test case verifies that 'Edit my ACCA' history is shown for edited bet
    DESCRIPTION: AUTOTEST [C13035462]
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login
    PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA7)
    PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 4. Remove few selections from the bet and save changes
    PRECONDITIONS: 5. Tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 6. Remove few selections from the bet and save changes
    PRECONDITIONS: Note: all data in Step1 and Step2 is based on received data from BPP in Network -> accountHistory?detailLevel=DETAILED&fromDate=<DateFrom>%2000%3A00%3A00&toDate=<DateTo> Request
    """
    keep_browser_open = True

    def test_001_navigate_to_my_betsopen_bets_tab(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets tab
        EXPECTED: 
        """
        pass

    def test_002_tap_show_edit_history_buttonverify_that_edit_history_listing_overlay_for_the_edited_acca_is_shown_with_all_appropriate_elements(self):
        """
        DESCRIPTION: Tap 'SHOW EDIT HISTORY' button
        DESCRIPTION: Verify that Edit History Listing Overlay for the edited ACCA is shown with all appropriate elements
        EXPECTED: Edit History Listing Overlay is shown with appropriate elements:
        EXPECTED: * "Edit Acca History" title
        EXPECTED: * 'Close' ('X') button
        EXPECTED: * Bet type for all bets
        EXPECTED: * Original Bet box
        EXPECTED: * All Edited Bet boxes
        EXPECTED: * All edited accas are displayed collapsed by default
        EXPECTED: * Date and Time when the bet was placed is displayed
        EXPECTED: NOTE: Edited ACCA should be shown as per Time Order as they were Edited
        """
        pass

    def test_003_tap_on_original_betverify_that_detailed_information_for_original_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Original Bet'
        DESCRIPTION: Verify that detailed information for original ACCA is shown
        EXPECTED: The Original ACCA is shown with appropriate elements:
        EXPECTED: * Bet Type
        EXPECTED: * Date and Time of bet placement is displayed
        EXPECTED: * Selections name
        EXPECTED: * Markets name
        EXPECTED: * Events name
        EXPECTED: * Events Date and Time
        EXPECTED: * Scores result (if available)
        EXPECTED: * Selections Price
        EXPECTED: * Returns status
        EXPECTED: * Total stake which was used at the time of bet placement
        EXPECTED: * Receipt ID is displayed
        EXPECTED: Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        pass

    def test_004_tap_on_edited_betverify_that_detailed_information_for_edited_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Edited Bet'
        DESCRIPTION: Verify that detailed information for edited ACCA is shown
        EXPECTED: The Edited ACCA is shown with appropriate elements:
        EXPECTED: * Bet Type
        EXPECTED: * Date and Time of bet placement is displayed
        EXPECTED: * Selections name
        EXPECTED: * Markets name
        EXPECTED: * Events name
        EXPECTED: * Events Date and Time
        EXPECTED: * Scores result (if available)
        EXPECTED: * Selections Price
        EXPECTED: * Returns status
        EXPECTED: * Total stake which was used at the time of bet placement
        EXPECTED: * Receipt ID is displayed
        EXPECTED: * Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: * Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        pass

    def test_005_tap_close_x_buttonverify_that_edit_history_listing_overlay_is_closed(self):
        """
        DESCRIPTION: Tap 'Close' ('X') button
        DESCRIPTION: Verify that Edit History Listing Overlay is closed
        EXPECTED: * Edit History Listing Overlay is closed
        """
        pass

    def test_006_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets(self):
        """
        DESCRIPTION: Make a placed bet (edited bet) SETTLED (add and settle the result for each event in the edited bet)
        DESCRIPTION: Verify that the new bet is resulted and shown on By Bets>(Bet History)Settled Bets
        EXPECTED: * Edited Bet is resulted
        EXPECTED: * Edited Bet is shown on By Bets>(Bet History)Settled Bets
        """
        pass

    def test_007_go_to_by_betsbet_historysettled_betran_2_6_steps(self):
        """
        DESCRIPTION: Go to By Bets>(Bet History)Settled Bet
        DESCRIPTION: Ran 2-6 steps
        EXPECTED: Results are the same
        """
        pass
