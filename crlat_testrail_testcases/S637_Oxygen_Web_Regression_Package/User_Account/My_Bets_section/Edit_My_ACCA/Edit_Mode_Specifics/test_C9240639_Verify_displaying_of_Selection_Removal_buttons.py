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
class Test_C9240639_Verify_displaying_of_Selection_Removal_buttons(Common):
    """
    TR_ID: C9240639
    NAME: Verify displaying of Selection Removal buttons
    DESCRIPTION: This test case verifies that Selection Removal buttons after user taps on 'EDIT MY ACCA'/BET' button and user has two or more open selections
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Login with User1
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on TREBLE
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cashoutverify_that_edit_my_bet_coraledit_my_acca_ladbrokes_button_and_event_details_are_shown_for_treble_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET' (Coral)/'EDIT MY ACCA' (Ladbrokes) button and event details are shown for TREBLE bets
        EXPECTED: The appropriate elements are shown for TREBLE bet:
        EXPECTED: - 'EDIT MY BET' (Coral)/'EDIT MY ACCA' (Ladbrokes) button is shown
        EXPECTED: - Selections details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        """
        pass

    def test_002_tap_edit_my_betacca_button_for_the_first_betverify_that_selection_removal_buttons_are_displayed_adjacent_to_all_selections_in_the_bet(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET/ACCA' button for the first bet
        DESCRIPTION: Verify that 'Selection Removal' buttons are displayed adjacent to all selections in the bet
        EXPECTED: The appropriate elements are shown for each selection in the TREBLE bet:
        EXPECTED: - Selection details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        EXPECTED: - Selection removal button
        EXPECTED: - Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection" is shown as ped design
        EXPECTED: - 'CONFIRM' button is shown and  is NOT be clickable
        EXPECTED: - 'Cash Out' button is NOT shown
        """
        pass

    def test_003_tap_the_selection_removal_x_button_for_any_selection(self):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        """
        pass

    def test_004_tap_the_selection_removal_x_button_for_any_selection_one_more_time(self):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection one more time
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        EXPECTED: - 'Selection Removal' button is non-clickable on the last open selection
        """
        pass

    def test_005_navigate_to_my_bets__open_betsverify_that_edit_my_betacca_button_and_event_details_are_shown_for_treble_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/ACCA' button and event details are shown for TREBLE bets
        EXPECTED: The appropriate elements are shown for TREBLE bet:
        EXPECTED: - 'EDIT MY BET/ACCA' button is shown
        EXPECTED: - Selections details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        """
        pass

    def test_006_tap_edit_my_betacca_button_for_the_first_betverify_that_selection_removal_buttons_are_displayed_next_to_all_selections_in_the_bet(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET/ACCA' button for the first bet
        DESCRIPTION: Verify that 'Selection Removal' buttons are displayed next to all selections in the bet
        EXPECTED: The appropriate elements are shown for each selection in the TREBLE bet:
        EXPECTED: - Selection details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        EXPECTED: - Selection removal button
        EXPECTED: - Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection"
        EXPECTED: - 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' button is NOT shown
        """
        pass

    def test_007_tap_the_selection_removal_x_button_for_any_selection(self):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        """
        pass

    def test_008_tap_the_selection_removal_x_button_for_any_selection_one_more_time(self):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection one more time
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        EXPECTED: - 'Selection Removal' button is non-clickable on the last open selection
        """
        pass
