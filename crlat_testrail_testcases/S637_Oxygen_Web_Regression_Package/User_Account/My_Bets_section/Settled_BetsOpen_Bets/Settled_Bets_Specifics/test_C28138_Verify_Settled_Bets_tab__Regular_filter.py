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
class Test_C28138_Verify_Settled_Bets_tab__Regular_filter(Common):
    """
    TR_ID: C28138
    NAME: Verify Settled Bets tab - "Regular" filter
    DESCRIPTION: This test case verifies 'Bet History' tab on 'My Bets' and on 'Account History' pages
    PRECONDITIONS: 1. User should be logged in to view their settled bets.
    PRECONDITIONS: 2. User should have a few Settled: won/lose/void/cashed out bets
    PRECONDITIONS: 3. User should have "Settled Bets" page opened.
    PRECONDITIONS: 4. User should have bets that were reviewed by Overask functionality (rejected, offered and so on)
    """
    keep_browser_open = True

    def test_001_navigate_to_the_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to the Settled Bets tab on 'My Bets' page
        EXPECTED: Settled Bets tab on 'My Bets' page is opened
        """
        pass

    def test_002_verify_page_ui_of_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Verify page UI of "Settled Bets" tab on 'My Bets' page
        EXPECTED: 1. Page header is "MY BETS"
        EXPECTED: 2. "Back" button is in the header
        EXPECTED: 3. Filters are present:
        EXPECTED: * Sports (selected by default)
        EXPECTED: * Lotto
        EXPECTED: * Pools
        EXPECTED: 4. "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: 5. "Settled Bets" accordion (collapsed by default)
        EXPECTED: 6. Pending/win/lose/cancelled/cashed out bets are present
        """
        pass

    def test_003_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User is directed to the last visited page before entering "My Bets" page
        """
        pass

    def test_004_verify_time_panel(self):
        """
        DESCRIPTION: Verify time panel
        EXPECTED: **For** **98** **Release**:
        EXPECTED: *   Time panel displays date of when bets were placed
        EXPECTED: *   All dates are shown chronologically, most recent first
        EXPECTED: *   Date is shown in next format: DD/MM/YYYY (e.g 19/05/2016) on the left side of the panel
        EXPECTED: * Bet Receipt number is shown on the right side of the panel
        EXPECTED: * Time panel is NOT available for Open bets
        EXPECTED: **For** **99** **Release**:
        EXPECTED: *   Time panel displays date of when bets were placed
        EXPECTED: *   All dates are shown chronologically, most recent first
        EXPECTED: *   Date is shown in HH:MM, DD MM format (e.g 10:22 - 14 July) at the bottom, on the right side of the panel
        EXPECTED: * Bet Receipt number is shown on the left side to date
        EXPECTED: * Time panel is NOT available for Open bets
        """
        pass

    def test_005_verify_multiples_bets(self):
        """
        DESCRIPTION: Verify Multiples bets
        EXPECTED: **For** **98** **Release**:
        EXPECTED: Bet details of all bets, which are included in a multiple, are shown one under another
        EXPECTED: Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: Stake and Total Returns are shown at the bottom of the section
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet details of all bets, which are included in a multiple, are shown one under another
        EXPECTED: * Stake and Total Returns are shown under bet details
        EXPECTED: * Date of bet placement and bet receipt ID are shown at the bottom (in card footer)
        """
        pass

    def test_006_verify_final_scores_after_event_settlement(self):
        """
        DESCRIPTION: Verify final scores after event settlement
        EXPECTED: Final scores should be available for the following sports:
        EXPECTED: * Football
        EXPECTED: * Basketball
        EXPECTED: * Tennis
        EXPECTED: * Badminton
        EXPECTED: * Handball
        EXPECTED: * Volleyball
        EXPECTED: * Beach Volleyball
        EXPECTED: Final scores should be shown only **after** event settlement
        """
        pass

    def test_007_verify_case_of_extra_time_andor_penalty_shootout(self):
        """
        DESCRIPTION: Verify case of Extra Time and/or Penalty Shootout
        EXPECTED: Only Final Extra Time or Final Penalty Shoot Out Score with Indication of Extra Time or Penalty Shoot Out are shown
        """
        pass

    def test_008_navigate_to_settled_bets_page_from_right_hand_menu(self):
        """
        DESCRIPTION: Navigate to "Settled Bets" page from right hand menu
        EXPECTED: "Settled Bets" page is opened
        """
        pass

    def test_009_repeat_steps_1_9(self):
        """
        DESCRIPTION: Repeat steps #1-9
        EXPECTED: 
        """
        pass

    def test_010_navigate_to_the_transaction_history_page_from_right_hand_menu(self):
        """
        DESCRIPTION: Navigate to the 'Transaction History' page from right hand menu
        EXPECTED: * 'Account History' page is opened
        EXPECTED: * 'Transaction History' page is opened by default
        """
        pass

    def test_011_tap_the_settled_bets_tab(self):
        """
        DESCRIPTION: Tap the 'Settled Bets' tab
        EXPECTED: 'Settled Bets' tab is opened
        """
        pass

    def test_012_verify_page_ui_of_settled_bets_tab_on_account_history_page(self):
        """
        DESCRIPTION: Verify page UI of "Settled Bets" tab on 'Account History' page
        EXPECTED: 1. Page header is "ACCOUNT HISTORY"
        EXPECTED: 2. "Back" button is in the header
        EXPECTED: 3. Filters are present:
        EXPECTED: * Sports (selected by default)
        EXPECTED: * Lotto
        EXPECTED: * Pools
        EXPECTED: 4. "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: 5. Pending/win/lose/cancelled/cashed out bet sections are present (all collapsed by default)
        """
        pass

    def test_013_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps 3-9
        EXPECTED: 
        """
        pass
