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
class Test_C237130_Statuses_of_selections(Common):
    """
    TR_ID: C237130
    NAME: Statuses of selections
    DESCRIPTION: This test case verifies displaying status of each selection on 'My Bets' tab on the Event Details page
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Single with cashout [C14790094] [C14835378]
    DESCRIPTION: Single without cashout [C14742505] [C14790091]
    DESCRIPTION: Multiple with/without cashout [C14835381] [C14835382]
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed single and multiple bets on events with and without Cash Out offer available
    PRECONDITIONS: * All events with placed bets are active (not suspended or resulted)
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where
    PRECONDITIONS: X.XX - current OpenBet version;
    PRECONDITIONS: XXX - event ID
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Single bet is shown **without** any status badge
        """
        pass

    def test_002_in_ob_backoffice_set_win_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Win** result for selection of event with placed **Single** bet
        EXPECTED: **For** **Release** **99**
        EXPECTED: * Bet is shown with a "Won" status (green tick from the left side)
        EXPECTED: **For** **Release** **98**
        EXPECTED: * Bet is shown with status badge of "Won" (in green color)
        """
        pass

    def test_003_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Bet is shown without any status badge
        """
        pass

    def test_004_in_ob_backoffice_set_lose_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Lose** result for selection of event with placed **Single** bet
        EXPECTED: **For** **Release** **99**
        EXPECTED: * Bet is shown with "Lost" status (red cross from the left side)
        EXPECTED: **For** **Release** **98**
        EXPECTED: * Bet is shown with status badge of "Lost" (in grey color)
        """
        pass

    def test_005_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Bet is shown without any status badge
        """
        pass

    def test_006_in_ob_backoffice_set_void_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Void** result for selection of event with placed **Single** bet
        EXPECTED: **For** **Release** **99**
        EXPECTED: * Bet is shown with "Void" status (text in black color from the left side)
        EXPECTED: **For** **Release** **98**
        EXPECTED: * Bet is shown with status badge of "Void" (in yellow color)
        """
        pass

    def test_007_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Bet is shown without any status badge
        """
        pass

    def test_008_repeat_steps_1_7_for_single_bets_without_available_cash_out(self):
        """
        DESCRIPTION: Repeat steps #1-7 for **Single** bets without available Cash Out
        EXPECTED: Results are the same
        """
        pass

    def test_009_repeat_steps_1_7_for_multiple_bets_with_and_without_available_cash_out(self):
        """
        DESCRIPTION: Repeat steps #1-7 for **Multiple** bets with and without available Cash Out
        EXPECTED: * Results are the same for appropriate leg in multiple bet
        """
        pass

    def test_010_refresh_my_bets_page(self):
        """
        DESCRIPTION: Refresh 'My Bets' page'
        EXPECTED: * All bets and legs are shown with relevant statuses
        EXPECTED: Note: Some bets can be removed from frontend as already settled
        """
        pass
