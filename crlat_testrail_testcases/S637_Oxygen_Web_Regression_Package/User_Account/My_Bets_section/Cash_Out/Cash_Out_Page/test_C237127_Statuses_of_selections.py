import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C237127_Statuses_of_selections(Common):
    """
    TR_ID: C237127
    NAME: Statuses of selections
    DESCRIPTION: This test case verifies displaying status of each selection on the Cash Out page
    DESCRIPTION: AUTOTEST [C665128]
    DESCRIPTION: AUTOTEST [C1684533]
    DESCRIPTION: AUTOTEST [C1684520]
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed single and multiple bets on events with Cash Out offer available
    PRECONDITIONS: * All events with placed bets are active (not suspended or resulted)
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where
    PRECONDITIONS: X.XX - current OpenBet version;
    PRECONDITIONS: XXX - event ID
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Cash out' tab is opened
        EXPECTED: * All bets are shown **without** any status badge (previously "Open")
        """
        pass

    def test_002_in_ob_backoffice_set_win_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Win** result for selection of event with placed **Single** bet
        EXPECTED: * Bet is shown with status badge of "Won" (in green color) for a few seconds and after it bet disappears from the page
        """
        pass

    def test_003_in_ob_backoffice_set_lose_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Lose** result for selection of event with placed **Single** bet
        EXPECTED: **OX99** * Bet is shown with status badge of "Lost" (in red color) for a few seconds and after it bet disappears from the page
        EXPECTED: OX98 * Bet is shown with status badge of "Lost" (in grey color) for a few seconds and after it bet disappears from the page
        """
        pass

    def test_004_in_ob_backoffice_set_void_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Void** result for selection of event with placed **Single** bet
        EXPECTED: **OX99** * Bet is shown with status badge of "Void" (black text) for a few seconds and after it bet disappears from the page
        EXPECTED: **OX98** * Bet is shown with status badge of "Void" (in yellow color) for a few seconds and after it bet disappears from the page
        """
        pass

    def test_005_repeat_steps_2_4_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **Multiple** bets
        EXPECTED: * Results are the same for the appropriate leg in multiple bet
        """
        pass

    def test_006_refresh_my_bets_page(self):
        """
        DESCRIPTION: Refresh 'My Bets' page'
        EXPECTED: * All bets and legs are shown with relevant statuses, where applied
        EXPECTED: Note: Some bets can be removed from frontend as already settled
        """
        pass
