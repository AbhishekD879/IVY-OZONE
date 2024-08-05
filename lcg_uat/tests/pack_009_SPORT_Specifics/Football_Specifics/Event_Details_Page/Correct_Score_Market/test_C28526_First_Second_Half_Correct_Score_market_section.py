import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # can not create event in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28526_First_Second_Half_Correct_Score_market_section(BaseSportTest):
    """
    TR_ID: C28526
    NAME: First/Second Half Correct Score market section
    DESCRIPTION: This test case verifies First/Second Half Correct Score market sections.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Half Correct Score"
    PRECONDITIONS: *   PROD: name="1st Half Correct Score"
    PRECONDITIONS: **Jira ticket: **BMA-3861
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(markets=[('first_half_correct_score', {'cashout': True})])
        self.__class__.event1 = self.ob_config.add_autotest_premier_league_football_event(markets=[('second_half_correct_score', {'cashout': True})])
        self.__class__.eventID = self.event.event_id
        self.__class__.eventID1 = self.event1.event_id
        self.__class__.event_name = '%s v %s' % (self.event.team1, self.event.team2)

        correct_score_prices = self.ob_config.event.correct_score_prices

        home_score_prices = correct_score_prices[0]
        sorted_home_score_prices = OrderedDict(sorted(home_score_prices[1].items()))
        self.__class__.home_prices = list(sorted_home_score_prices.values())

        away_score_prices = correct_score_prices[1]
        sorted_away_score_prices = OrderedDict(sorted(away_score_prices[1].items()))
        self.__class__.away_prices = list(sorted_away_score_prices.values())

        draw_score_prices = correct_score_prices[2]
        sorted_draw_score_prices = OrderedDict(sorted(draw_score_prices[1].items()))
        self.__class__.draw_prices = list(sorted_draw_score_prices.values())

        expected_goals = []
        for result in correct_score_prices:
            for score in list(result[1].keys()):
                expected_goals.append(score[0])
        self.__class__.expected_goals_quantity = sorted(list(set(expected_goals)))

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_event_details_page_of_football_event(self, status=True):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        if status:
            self.navigate_to_edp(event_id=self.eventID)
        else:
            self.navigate_to_edp(event_id=self.eventID1)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)
        if self.brand == 'bma':
            all_markets_tab = vec.siteserve.EXPECTED_MARKET_TABS.all_markets
            self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=all_markets_tab)

    def test_003_go_to_first_halfcorrect_score_market_section(self, market_name=None):
        """
        DESCRIPTION: Go to 'First Half Correct Score' market section
        EXPECTED: *   Section is present on Event Details Page (e.g. All Markets tab)
        EXPECTED: *   It is possible to collapse/expand section
        """
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')
        if market_name is None:
            market_name = self.expected_market_sections.first_half_correct_score
        else:
            market_name = market_name
        self.assertIn(market_name, self.markets_list, msg=f'"{market_name}" section is not present')

        self.__class__.correct_score = self.markets_list.get(market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{market_name}" section is not found in "{self.markets_list.keys()}"')
        self.correct_score.collapse()
        self.assertFalse(self.correct_score.is_expanded(expected_result=False),
                         msg=f'"{market_name}" section is not collapsed')

        self.correct_score.expand()
        self.assertTrue(self.correct_score.is_expanded(),
                        msg=f'"{market_name}" section is not expanded')

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If Correct Score has **cashoutAvail="Y"** then label Cash out should be displayed next to market section name
        """
        self.assertTrue(self.correct_score.market_section_header.has_cash_out_mark(),
                        msg=f'Market "{self.correct_score}" has no cashout label')

    def test_005_expand_first_halfcorrect_score_market_section(self):
        """
        DESCRIPTION: Expand 'First Half Correct Score' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Two pickers (<Home Team> <Away Team>)
        EXPECTED: *   **'Add to Betslip'** button with associated price
        EXPECTED: *   **'Show All' **option with all Correct Score outcomes
        EXPECTED: *   Lowest available goals number for each team is selected by default
        """
        self.assertTrue(self.correct_score.team_home_scores, msg='Home team result drop-down is not present')
        self.assertTrue(self.correct_score.team_away_scores, msg='Away team result drop-down is not present')

        self.assertEquals(self.correct_score.team_home_scores.selected_item, '0',
                          msg='Default value for home team result drop-down is not "0"')
        self.assertEquals(self.correct_score.team_away_scores.selected_item, '0',
                          msg='Default value for away team result drop-down is not "0"')

        self.assertEquals(self.correct_score.combined_outcome_button.name, self.draw_prices[0],
                          msg=f'Outcome price "{self.correct_score.combined_outcome_button.name}" '
                              f'is not the same as expected "{self.draw_prices[0]}" in case of invalid result selection')

        self.assertTrue(self.correct_score.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_006_verify_home_team___away_team_pickers(self):
        """
        DESCRIPTION: Verify <Home Team> - <Away Team> pickers
        EXPECTED: *   Each drop down contain goal numbers (e.g. 0,1,2,3,4,5,6,7,8,9...)
        EXPECTED: *   The min/max goal numbers in drop-down is taken from SS
        """
        for goals_quantity in self.expected_goals_quantity:
            self.assertIn(goals_quantity, self.correct_score.team_home_scores.available_options,
                          msg=f'Expected goals quantity: {goals_quantity}, is not found in dropdown of home team')

        for goals_quantity in self.expected_goals_quantity:
            self.assertIn(goals_quantity, self.correct_score.team_away_scores.available_options,
                          msg=f'Expected goals quantity: {goals_quantity}, is not found in dropdown of away team')

    def test_007_clicktap_show_all_option(self):
        """
        DESCRIPTION: Click/Tap 'Show All' option
        EXPECTED: *   All Correct Score outcomes are present
        EXPECTED: *   Outcomes are ordered in three columns (<Home Team> <Draw> <Away Team>)
        EXPECTED: *   Button name is changed to 'Show less'
        """
        self.correct_score.show_all_button.click()
        self.assertTrue(self.correct_score.has_show_less_button(), msg='"SHOW LESS" button is not present')
        home_actual_prices = self.correct_score.outcome_table.home_outcomes.outcomes_prices
        self.assertEquals(self.home_prices, home_actual_prices,
                          msg=f'Expected prices for home team: "{self.home_prices}"'
                              f' are not equal to actual: "{home_actual_prices}"')

        draw_actual_prices = self.correct_score.outcome_table.draw_outcomes.outcomes_prices
        self.assertEquals(self.draw_prices, draw_actual_prices,
                          msg=f'Expected prices for home team: "{self.draw_prices}"'
                              f' are not equal to actual: "{draw_actual_prices}"')

        away_actual_prices = self.correct_score.outcome_table.away_outcomes.outcomes_prices
        self.assertEquals(self.away_prices, away_actual_prices,
                          msg=f'Expected prices for home team: "{self.away_prices}"'
                              f' are not equal to actual: "{away_actual_prices}"')

    def test_008_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   selection of 'Home Team' are shown on the left side
        EXPECTED: *   selection of 'Draw' are shown in the middle
        EXPECTED: *   selection of 'Away Team are shownon the right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        # Verification was done in previous step, where Home / Draw / Away
        # expected and actual selections lists are compared

    def test_009_verify_any_other_selections_displaying(self):
        """
        DESCRIPTION: Verify Any other selections displaying
        EXPECTED: *   selection of 'Home Any other' are shown on the bottom left side
        EXPECTED: *   selection of 'Draw Any other' are shown in the middle bottom
        EXPECTED: *   selection of 'Away Any other' are shown on the bottom right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        # Covered in above steps

    def test_010_verify_selections_sortening(self):
        """
        DESCRIPTION: Verify selections sortening
        EXPECTED: Selection are sorted by Team score (**outcomeMeaningScores** attribute) from lowest to highest
        """
        home_outcomes = self.correct_score.outcome_table.home_outcomes.items_names
        self.assertEquals(home_outcomes, sorted(home_outcomes),
                          msg='Outcomes for home team results are not sorted by team score')

        draw_outcomes = self.correct_score.outcome_table.draw_outcomes.items_names
        self.assertEquals(draw_outcomes, sorted(draw_outcomes),
                          msg='Outcomes for draw results are not sorted by team score')

        home_outcomes = self.correct_score.outcome_table.home_outcomes.items_names
        self.assertEquals(home_outcomes, sorted(home_outcomes),
                          msg='Outcomes of away team results are not sorted by team score')

    def test_011_clicktap_show_less_button(self):
        """
        DESCRIPTION: Click/Tap 'Show Less' button
        EXPECTED: *   Section with Correct Score outcomes is collapsed
        EXPECTED: *   Button name is changed to 'Show All'
        """
        self.correct_score.show_less_button.click()
        self.assertFalse(self.correct_score.outcome_table.is_displayed(expected_result=False, timeout=2),
                         msg='Outcome table remains displayed')
        self.assertTrue(self.correct_score.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_012_verify_first_halfcorrect_score_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'First Half Correct Score' section in case of data absence
        EXPECTED: 'First Half Correct Score' section is not shown if:
        EXPECTED: *   all markets of that section are absent
        EXPECTED: *   all outcomes of that section are absent
        """
        selection_ids = list(self.event.selection_ids['first_half_correct_score'].values())
        for inedex in range(0, len(selection_ids)):
            self.ob_config.change_selection_state(selection_id=selection_ids[inedex], displayed=False, active=False)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        first_half_market_name = self.expected_market_sections.first_half_correct_score
        self.assertNotIn(first_half_market_name, markets_list, msg=f'"{first_half_market_name}" section is not present')

    def test_013_repeat_3_11_steps_for_second_half_correct_score_market_section(self):
        """
        DESCRIPTION: Repeat 3-11 steps for 'Second Half Correct Score' market section
        EXPECTED:
        """
        self.test_002_go_to_event_details_page_of_football_event(status=False)
        market_name = self.expected_market_sections.second_half_correct_score
        self.test_003_go_to_first_halfcorrect_score_market_section(market_name=market_name)
        self.test_004_verify_cash_out_label_next_to_market_section_name()
        self.test_005_expand_first_halfcorrect_score_market_section()
        self.test_006_verify_home_team___away_team_pickers()
        self.test_007_clicktap_show_all_option()
        self.test_008_verify_selections_displaying_for_markets()
        self.test_009_verify_any_other_selections_displaying()
        self.test_010_verify_selections_sortening()
        self.test_011_clicktap_show_less_button()
