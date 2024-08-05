import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.failure_exception import TestFailure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C1933493_Banach_Cannot_combine_error(BaseBanachTest):
    """
    TR_ID: C1933493
    NAME: Banach. Cannot combine error
    DESCRIPTION: Test case verifies error when user adds selections which cannot be combined to dashboard
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Examples of not valid selections combinations:
    PRECONDITIONS: - BOTH TEAMS TO SCORE IN BOTH HALFS - Yes + BOTH TEAMS TO SCORE - No
    PRECONDITIONS: - BOTH TEAMS TO SCORE IN BOTH HALFS - No + BOTH TEAM TO SCORE IN FIRST HALF - Yes
    PRECONDITIONS: - DOUBLE CHANCE 90 MINS - [Home team] or Draw + MATCH BETTING SECOND HALF - [Away team]
    PRECONDITIONS: - TOTAL GOALS 90 MINS - Over 0.5 Goals + [HOME TEAM] TOTAL GOALS - Under 0.5 + [AWAY TEAM] TOTAL GOALS - Under 0.5
    PRECONDITIONS: To see the error message from the provider check Dev tools > Network - "price" request
    PRECONDITIONS: **Build Your Bet tab on event details page is loaded**
    """
    cannot_combine_error = 'Cannot combine: {selection_name_both_teams_to_score} in BOTH TEAMS TO SCORE and ' \
                           '{selection_name_both_teams_to_score_in_both_halves} in BOTH TEAMS TO SCORE IN BOTH HALVES'
    selection_to_delete = 'Both Teams To Score'
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Login and navigate to EDP using derived event_id
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'{self.expected_market_tabs.build_your_bet} tab is not active')

    def test_001_add_to_dashboard_selections_from_invalid_combinations_choose_which_is_available(self):
        """
        DESCRIPTION: Add to dashboard selections from invalid combinations (choose which is available)
        EXPECTED: - Error message from the provider is shown - it comes in **price** request "responseMessage" parameter
        EXPECTED: - "Place bet" button is hidden from Dashboard
        """
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting, selection_index=2)
        self.__class__.initial_counter += 1
        both_teams_to_score_selection = self.add_byb_selection_to_dashboard(
            market_name=self.expected_market_sections.both_teams_to_score, selection_index=0)[1]
        self.__class__.initial_counter += 1
        both_teams_to_score_in_both_halves_selection = self.add_byb_selection_to_dashboard(
            market_name=self.expected_market_sections.both_teams_to_score_in_both_halves, selection_index=1)[0]
        self.__class__.initial_counter += 1
        self.__class__.cannot_combine_error = self.cannot_combine_error.format(
            selection_name_both_teams_to_score=both_teams_to_score_selection.upper(),
            selection_name_both_teams_to_score_in_both_halves=both_teams_to_score_in_both_halves_selection.upper())
        error_message_text = self.site.sport_event_details.tab_content.dashboard_panel.info_panel.text
        self.assertTrue(error_message_text, msg='Error message from provider is not shown')
        try:
            self.assertEqual(error_message_text, self.cannot_combine_error,
                             msg=f'Error message "{error_message_text}" is not the same '
                                 f'as expected "{self.cannot_combine_error}"')
        except TestFailure:
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.assertFalse(
            self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.has_place_bet_button(
                expected_result=False), msg='"Place bet" button is not hidden from Dashboard')

    def test_002_remove_some_selections_to_have_valid_combination(self):
        """
        DESCRIPTION: Remove some selections to have valid combination
        EXPECTED: * Error message disappears
        EXPECTED: * Odds area is shown with a price
        """
        outcomes = self.site.sport_event_details.tab_content.dashboard_panel.outcomes_section.items_as_ordered_dict
        outcome = next(
            (outcome for outcome_name, outcome in outcomes.items() if self.selection_to_delete in outcome_name), None)
        self.assertTrue(outcome, f'{outcome} is not available at Dashboard')
        outcome.remove_button.click()

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            initial_counter=self.initial_counter)
        self.assertFalse(
            self.site.sport_event_details.tab_content.dashboard_panel.wait_for_info_panel(
                expected_result=False, timeout=2),
            msg='Error message from provider is not hidden from Dashboard')
        self.assertTrue(self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.has_place_bet_button(),
                        msg='"Place bet" button is not shown at Dashboard')
