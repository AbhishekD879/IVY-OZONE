import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29014_Clearing_All_Bets_From_the_Betslip(Common):
    """
    TR_ID: C29014
    NAME: Clearing All Bets From the Betslip
    DESCRIPTION: This test case verifies how all bets can be removed from the BetSlip.
    DESCRIPTION: AUTOTEST [C11802791]
    PRECONDITIONS: User is logged in / logged out
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_add_single_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add single selection to the Betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * Selection is present in the Bet Slip
        EXPECTED: * 'REMOVE ALL' button is displayed within Betslip header on the right from Your Selections section
        """
        pass

    def test_003_tap_remove_all_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button
        EXPECTED: *  'Remove All' pop-up is shown
        """
        pass

    def test_004_verify_view_of_remove_all_pop_up(self):
        """
        DESCRIPTION: Verify view of 'Remove All' pop-up
        EXPECTED: Pop-up contains header title, question text and two buttons: Cancel and Continue
        EXPECTED: **Coral**: pop up name is "REMOVE ALL?"
        EXPECTED: **Ladbrokes**: pop up name is "Remove All"
        """
        pass

    def test_005_press_cancel_button(self):
        """
        DESCRIPTION: Press 'Cancel' button
        EXPECTED: * 'Remove All' pop-up is closed
        EXPECTED: * User stays on Betslip, placed bets are present in Betslip
        """
        pass

    def test_006_tap_remove_all_button_and_press_continue_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button and press Continue button
        EXPECTED: *  Bets is removed from the Bet Slip after confirming
        EXPECTED: *  The Bet Slip counter is reset to 0
        EXPECTED: *  For Mobile: Betslip is automatically closed after selections removal
        EXPECTED: *  For Tablet and Desktop: User sees 'You have no selections in the slip.' message
        EXPECTED: *  For Tablet and Desktop: 'GO BETTING' button is displayed for empty Betslip
        """
        pass

    def test_007_tabletdesktoptap_go_betting_button_in_betslip_widget(self):
        """
        DESCRIPTION: Tablet/Desktop:
        DESCRIPTION: Tap 'GO BETTING' button in Betslip widget
        EXPECTED: - Homepage is opened in the main view
        """
        pass

    def test_008_tabletdesktoptap_go_betting_button_in_betslip_widget_again_when_user_is_already_navigated_to_the_homepage(self):
        """
        DESCRIPTION: Tablet/Desktop:
        DESCRIPTION: Tap 'GO BETTING' button in Betslip widget again when user is already navigated to the Homepage
        EXPECTED: Homepage continues to be displayed in the main view without any additional redirection
        """
        pass

    def test_009_select_several_selections_from_the_different_events(self):
        """
        DESCRIPTION: Select several selections from the different events
        EXPECTED: 
        """
        pass

    def test_010_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: *   Selections are present in the Bet Slip
        EXPECTED: * 'REMOVE ALL' button is displayed within Betslip header on the right from Your Selections section
        """
        pass

    def test_011_tap_remove_all_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button
        EXPECTED: * 'Remove All' pop-up is shown
        """
        pass

    def test_012_verify_view_of_remove_all_pop_up(self):
        """
        DESCRIPTION: Verify view of 'Remove All' pop-up
        EXPECTED: Pop-up contains header title, question text and two buttons: 'Cancel' and 'Continue'
        """
        pass

    def test_013_press_cancel_button(self):
        """
        DESCRIPTION: Press 'Cancel' button
        EXPECTED: * 'Remove All' pop-up is closed
        EXPECTED: * User stays on Betslip, placed bets are present in Betslip
        """
        pass

    def test_014_tap_remove_all_button_and_press_continue_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button and press Continue button
        EXPECTED: *  All Bets are removed from the Bet Slip after confirming (Singles, Multiples)
        EXPECTED: *  The Bet Slip counter is reset to 0
        EXPECTED: *  For Mobile: Betslip is automatically closed after selections removal
        EXPECTED: *  For Tablet and Desktop: User sees 'Your betslip is empty.' message
        EXPECTED: *  For Tablet and Desktop: 'GO BETTING' button is displayed for empty Betlsip
        """
        pass
