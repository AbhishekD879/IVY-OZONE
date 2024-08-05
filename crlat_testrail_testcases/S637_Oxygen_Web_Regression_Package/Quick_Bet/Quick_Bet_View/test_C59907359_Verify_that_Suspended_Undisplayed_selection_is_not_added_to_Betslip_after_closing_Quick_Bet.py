import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C59907359_Verify_that_Suspended_Undisplayed_selection_is_not_added_to_Betslip_after_closing_Quick_Bet(Common):
    """
    TR_ID: C59907359
    NAME: Verify that Suspended/Undisplayed selection is not added to Betslip after closing Quick Bet
    DESCRIPTION: BMA-54870 Quickbet - Add selection if customer taps X
    DESCRIPTION: This Test case verifies that, after customer taps 'X' Button on Quick bet, Quick bet is closed and Selection is not added to Betslip, if selection is already suspended or undisplayed
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in/logged out
    PRECONDITIONS: (Test for logged in and logged out user)
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page. Selection is added Quick Bet
        """
        pass

    def test_002_in_open_bet_find_the_event_added_to_quick_bet_and_suspend_eventmarketselection(self):
        """
        DESCRIPTION: In Open Bet, find the event, added to Quick bet, and suspend Event/Market/Selection
        EXPECTED: Event suspension is reflected on Quick Bet.
        EXPECTED: Message 'Your event has been suspended' is shown. Buttons 'Place bet', 'Add to Betslip' are disabled.
        """
        pass

    def test_003_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Selection is NOT added to Betslip
        """
        pass

    def test_004_in_openbet_make_active_eventmarketselection(self):
        """
        DESCRIPTION: In OpenBet make active Event/Market/Selection
        EXPECTED: * Selection is not highlighted
        EXPECTED: * Betslip counter has not changed
        EXPECTED: * Betslip is empty
        """
        pass

    def test_005_add_another_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add another Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page. Selection is added Quick Bet
        """
        pass

    def test_006_in_open_bet_find_the_event_added_to_quick_bet_and_undisplay_eventmarketselection(self):
        """
        DESCRIPTION: In Open Bet, find the event, added to Quick bet, and undisplay Event/Market/Selection
        EXPECTED: Event undisplaying is reflected on Quick Bet.
        EXPECTED: Message 'Your event has been suspended' is shown. Buttons 'Place bet', 'Add to Betslip' are disabled.
        """
        pass

    def test_007_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Selection is NOT added to Betslip
        """
        pass

    def test_008_in_openbet_display_eventmarketselection(self):
        """
        DESCRIPTION: In OpenBet display Event/Market/Selection
        EXPECTED: * Selection is not highlighted
        EXPECTED: * Betslip counter has not changed
        EXPECTED: * Betslip is empty
        """
        pass
