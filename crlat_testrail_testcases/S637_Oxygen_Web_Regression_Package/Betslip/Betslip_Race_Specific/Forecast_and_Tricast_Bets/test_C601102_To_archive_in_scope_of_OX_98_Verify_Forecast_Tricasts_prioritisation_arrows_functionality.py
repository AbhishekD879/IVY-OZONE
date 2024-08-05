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
class Test_C601102_To_archive_in_scope_of_OX_98_Verify_Forecast_Tricasts_prioritisation_arrows_functionality(Common):
    """
    TR_ID: C601102
    NAME: [To archive in scope of OX 98] Verify Forecast/Tricasts prioritisation arrows functionality
    DESCRIPTION: Thie test case verifies possibility to re-order Horse Racing selections in the Betslip using Forecast/Tricasts prioritisation arrows
    PRECONDITIONS: 1. Oxygen application is loaded
    PRECONDITIONS: 2. Two and more Horse Racing selections from the same event and the same market are added to the Betslip
    PRECONDITIONS: 3. Betslip is opened and Forecast/Tricast section is available
    """
    keep_browser_open = True

    def test_001_tap_plus_for__forecaststricasts_section_and_verify_re_order_selections_text_link_displaying_in_expanded_view(self):
        """
        DESCRIPTION: Tap '+' for  'Forecasts/Tricasts' section and verify 'Re-order selections' text link displaying in expanded view
        EXPECTED: - Selections with all appropriate parameters (order number, runner number, and selection name) are displayed in the order as they were added to the Betslip
        EXPECTED: - 'Re-order selections' text link is displayed above the selections list
        """
        pass

    def test_002_tap_re_order_selections_text_link_and_verify_forecaststricasts_section_content(self):
        """
        DESCRIPTION: Tap 'Re-order selections' text link and verify 'Forecasts/Tricasts' section content
        EXPECTED: - 'Re-order selections' text link is changed to 'Done' text link
        EXPECTED: - Unselected checkbox is displayed for each selection in the list
        EXPECTED: - 'Up' and 'Down' arrows are displayed below the selections list and are disabled
        """
        pass

    def test_003_verify_up_and_down_arrows_disabling_depending_on_chosen_selection_position(self):
        """
        DESCRIPTION: Verify 'Up' and 'Down' arrows disabling depending on chosen selection position
        EXPECTED: - 'Down' arrow becomes disabled if the first (the highest) selection is selected using checkbox
        EXPECTED: - 'Up' arrow becomes disabled if the last (the lowest) selection is selected using checkbox
        EXPECTED: - Both arrows are enabled for all other selections from the list
        """
        pass

    def test_004_verify_possibility_to_select_two_and_more_selections_at_once_using_checboxes(self):
        """
        DESCRIPTION: Verify possibility to select two and more selections at once using checboxes
        EXPECTED: - It is impossible to select 2 or more selections at once (Radio button UI element functionality is used)
        """
        pass

    def test_005_do_not_change_selections_ordering_and_tap_done_text_link(self):
        """
        DESCRIPTION: Do NOT change selections ordering and tap 'Done' text link
        EXPECTED: - Selections position is not changed
        EXPECTED: - Reorder Selections area is hidden
        EXPECTED: - 'Done' text link is changed to 'Re-order selections' text link
        """
        pass

    def test_006_tap_re_order_selections_text_link(self):
        """
        DESCRIPTION: Tap 'Re-order selections' text link
        EXPECTED: 
        """
        pass

    def test_007_choose_any_selection_from_the_list_except_of_the_first_one_using_checkbox_and_tap_up_arrowverify_selection_position_in_the_list(self):
        """
        DESCRIPTION: Choose any selection from the list (except of the first one) using checkbox and tap 'Up' arrow.
        DESCRIPTION: Verify selection position in the list.
        EXPECTED: - Selection swaps position to the selection above
        """
        pass

    def test_008_choose_any_selection_from_the_list_except_of_the_last_one_using_checkbox_and_tap_down_arrowverify_selection_position_in_the_list(self):
        """
        DESCRIPTION: Choose any selection from the list (except of the last one) using checkbox and tap 'Down' arrow.
        DESCRIPTION: Verify selection position in the list.
        EXPECTED: - Selection swaps position to the selection beneath
        """
        pass

    def test_009_do_not_tap_done_text_link_and_verify_selections_ordering_on_bet_receipt_page_and_in_buildbet_response(self):
        """
        DESCRIPTION: Do not tap 'Done' text link and verify selections ordering on Bet receipt page and in 'BuildBet' response
        EXPECTED: - Selections IDs ordering in 'BuildBet' response  is appropriate to initial Selections positions in the list and do not include positions changes for selections
        """
        pass

    def test_010_do_not_tap_done_button_and_place_a_bet_for_forecaststricasts_stakeverify_selections_ordering_on_bet_receipt_page(self):
        """
        DESCRIPTION: Do not tap 'Done' button and place a bet for Forecasts/Tricasts stake.
        DESCRIPTION: Verify selections ordering on Bet receipt page.
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Ordering of selections on Bet Receipt page is appropriate to initial Selections positions in the list and do not include positions changes for selections
        """
        pass

    def test_011_add_two_and_more_horse_racing_selections_from_the_same_event_and_the_same_market_to_the_betslip(self):
        """
        DESCRIPTION: Add two and more Horse Racing selections from the same event and the same market to the Betslip
        EXPECTED: Forecasts/Tricasts section is available
        """
        pass

    def test_012_change_position_for_few_selections_in_forecaststricasts_sectiontap_done_text_link(self):
        """
        DESCRIPTION: Change position for few selections in Forecasts/Tricasts section.
        DESCRIPTION: Tap 'Done' text link
        EXPECTED: - Betlsip is reloaded
        EXPECTED: - Selections in Forecasts/tricasts setion are re-ordered appropriately
        EXPECTED: - Selections in Singles section are re-ordered appropriately
        """
        pass

    def test_013_verify_selections_ordering_in_buildbet_response(self):
        """
        DESCRIPTION: Verify selections ordering in 'BuildBet' response
        EXPECTED: - Selections IDs ordering in 'BuildBet' response  is appropriate to re-ordered Selections positions
        """
        pass

    def test_014_place_bet_for_forecaststricasts_stakeverify_selections_ordering_on_bet_receipt_page(self):
        """
        DESCRIPTION: Place bet for Forecasts/Tricasts stake.
        DESCRIPTION: Verify selections ordering on Bet receipt page.
        EXPECTED: - Ordering of selections on Bet Receipt page is appropriate to re-ordered Selections positions
        """
        pass

    def test_015_go_to_my_betsbet_historyverify_selections_ordering_for_placed_bet(self):
        """
        DESCRIPTION: Go to My Bets/Bet History.
        DESCRIPTION: Verify selections ordering for placed bet
        EXPECTED: - Ordering of selections on My Bets/Bet History page is appropriate to re-ordered Selections positions
        """
        pass
