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
class Test_C113828_To_update_Verify_Settled_Bets_tab__Regular_filter_tablet_desktop(Common):
    """
    TR_ID: C113828
    NAME: [To update]  Verify Settled Bets tab - "Regular" filter (tablet & desktop)
    DESCRIPTION: This test case verifies  Bet History tab
    PRECONDITIONS: 1. User should be logged in to view their Settled Bets.
    PRECONDITIONS: 2. User should have a few Settled: won/lose/void/cashed out bets
    PRECONDITIONS: 3. User should have bets that were reviewed by Overask functionality (rejected, offered and so on)
    """
    keep_browser_open = True

    def test_001_tap_on_right_menu_icon___settled_bets_bet_history_or_right_menu_icon___my_account___settled_bets_bet_historyortap_settled_bets_on_bet_slip_widget(self):
        """
        DESCRIPTION: Tap on Right menu icon -> 'Settled Bets' ('Bet History') or Right menu icon -> 'My Account' -> 'Settled Bets' ('Bet History')
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Settled Bets' on 'Bet Slip' widget
        EXPECTED: 1. 'Settled Bets' tab is opened within 'Bet Slip' widget (last on the right, after 'Bet Slip', 'Cash Out' and 'Open Bets')
        EXPECTED: 2. Four sort filters are present :
        EXPECTED: *   Sports (selected by default)
        EXPECTED: *   Player Bets
        EXPECTED: *   Lotto
        EXPECTED: *   Pools
        EXPECTED: 3. "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: Note: The date pickers are not shown for 'Player Bets' sort filter
        EXPECTED: 4. Pending/win/lose/cancelled/cashed out bet sections are present
        EXPECTED: 5. "Settled Bets" accordion (collapsed by default)
        EXPECTED: 6. Previously opened page remains opened
        """
        pass

    def test_002_verify_time_panel(self):
        """
        DESCRIPTION: Verify time panel
        EXPECTED: **For** **98** **Release**:
        EXPECTED: *  Time panel displays date of when bets were placed
        EXPECTED: *  All dates are shown chronologically, most recent first
        EXPECTED: *  Date is shown in next format: DD/MM/YYYY (e.g 19/05/2016) on the left side of the panel
        EXPECTED: * Bet Receipt number is shown on the right side of the panel
        EXPECTED: * Time panel is NOT available for Open bets
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Time panel displays date of when bets were placed
        EXPECTED: * All dates are shown chronologically, most recent first
        EXPECTED: * Date is shown in HH:MM, DD MM format (e.g 10:22 - 14 July) at the bottom, on the right side of the panel
        EXPECTED: * Bet Receipt number is shown on the left side to date
        EXPECTED: * Time panel is NOT available for Open bets
        EXPECTED: ![](index.php?/attachments/get/99256864)
        """
        pass

    def test_003_verify_multiples_bets(self):
        """
        DESCRIPTION: Verify Multiples bets
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * Bet details of all bets, which are included in a multiple, are shown one under another
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake and Estimated Returns are shown at the bottom of the section
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet details of all bets, which are included in a multiple, are shown one under another
        EXPECTED: * Stake and Total Returns are shown under bet details
        EXPECTED: * Date of bet placement and bet receipt ID are shown at the bottom (in card footer)
        """
        pass

    def test_004_verify_final_scores_after_event_settlement(self):
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
        EXPECTED: Final scores should be shown only after event settlement
        """
        pass

    def test_005_verify_case_of_extra_time_andor_penalty_shootout(self):
        """
        DESCRIPTION: Verify case of Extra Time and/or Penalty Shootout
        EXPECTED: Only Final Extra Time or Final Penalty Shoot Out Score with Indication of Extra Time or Penalty Shoot Out are shown
        """
        pass

    def test_006_go_to_the_homepage(self):
        """
        DESCRIPTION: Go to the homepage
        EXPECTED: Oxygen homepage is loaded
        """
        pass

    def test_007_enter_direct_url_for_settled_bets_page_into_the_address_bar(self):
        """
        DESCRIPTION: Enter direct URL for Settled Bets page into the address bar
        EXPECTED: Settled Bets pageis opened
        """
        pass

    def test_008_verify_settled_bets_page_ui(self):
        """
        DESCRIPTION: Verify "Settled Bets" page UI
        EXPECTED: 1. Page header is "MY BETS" with a "back" button next to it
        EXPECTED: 2. 3 tabs are on the page: "CASH OUT", "OPEN BETS", "SETTLED BETS" (last one is default)
        EXPECTED: 3. Four sort filters are present :
        EXPECTED: *   Sports (selected by default)
        EXPECTED: *   Player Bets
        EXPECTED: *   Lotto
        EXPECTED: *   Pools
        EXPECTED: 4. "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: Note: The date pickers are not shown for 'Player Bets' sort filter
        EXPECTED: 5. Pending/win/lose/cancelled/cashed out bet sections are present (all collapsed by default)
        """
        pass

    def test_009_load_oxygen_application_on_desktoptap_on_right_menu_icon___my_account___settled_bets_bet_historyortap_settled_bets_on_bet_slip_widget(self):
        """
        DESCRIPTION: Load Oxygen application on desktop
        DESCRIPTION: Tap on Right menu icon -> 'My Account' -> 'Settled Bets' ('Bet History')
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Settled Bets' on 'Bet Slip' widget
        EXPECTED: Expected result is the same as for step #2
        """
        pass

    def test_010_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps #3-8
        EXPECTED: 
        """
        pass
