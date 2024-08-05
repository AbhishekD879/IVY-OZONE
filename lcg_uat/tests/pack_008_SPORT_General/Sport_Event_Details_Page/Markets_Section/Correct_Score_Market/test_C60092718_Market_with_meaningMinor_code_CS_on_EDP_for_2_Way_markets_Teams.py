import pytest
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Intercation with OB for scores creation and other stuff
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60092718_Market_with_meaningMinor_code_CS_on_EDP_for_2_Way_markets_Teams(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C60092718
    NAME: Market with  meaningMinor code 'CS' on EDP for 2-Way markets (Teams).
    DESCRIPTION: This test case verifies Correct Score market section on EDP.
    DESCRIPTION: Correct score: add option to allow 'H/D/A Any Other' score selection
    DESCRIPTION: Markets including meaningMinor code 'CS'such as:
    DESCRIPTION: First half correct score
    DESCRIPTION: Second half correct score
    DESCRIPTION: Sports(ex) :
    DESCRIPTION: VolleyBall
    DESCRIPTION: BasketBall
    DESCRIPTION: BaseBall
    DESCRIPTION: Ice hockey
    DESCRIPTION: List of Correct score markets such as (Market sort "correct score" and Display sort "CS") :
    DESCRIPTION: Correct score
    DESCRIPTION: Set Betting
    DESCRIPTION: Set X correct score
    DESCRIPTION: Current Game correct score
    DESCRIPTION: Next game correct score
    DESCRIPTION: Current set correct score
    DESCRIPTION: Next set correct score
    DESCRIPTION: Current set score after X games
    DESCRIPTION: Next set score after X games
    DESCRIPTION: Tie break correct score
    DESCRIPTION: Match tie correct score
    DESCRIPTION: Match tie break correct score
    DESCRIPTION: Match correct score
    DESCRIPTION: Game X correct score
    DESCRIPTION: X innings correct score
    DESCRIPTION: Xth innings correct score
    DESCRIPTION: Series correct score
    DESCRIPTION: Correct match score
    DESCRIPTION: xth set correct score
    DESCRIPTION: Best of X correct score
    DESCRIPTION: Map X correct round score
    DESCRIPTION: Extra time correct score
    DESCRIPTION: First half correct score
    DESCRIPTION: Second half correct score
    DESCRIPTION: Extra time half time correct score
    DESCRIPTION: Any Time correct score
    DESCRIPTION: Correct score betting
    DESCRIPTION: Frame X-X correct score
    DESCRIPTION: X set correct score
    DESCRIPTION: Set X correct score
    DESCRIPTION: Period X correct score
    DESCRIPTION: X Period correct score
    DESCRIPTION: Correct score X mins
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('correct_score',
                                                                                    {'cashout': True})])
        self.__class__.eventID = event.event_id
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)

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

    def test_001_navigate_to_sport_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Navigate to <Sport> Event Details page of Football event
        EXPECTED: <Sport> Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)

        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_002_go_to_correct_score_market_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' market section
        EXPECTED: *   Section is present on Event Details Page
        EXPECTED: *   It is possible to collapse/expand section
        """
        self.__class__.market_name = self.expected_market_sections.correct_score
        self.assertIn(self.market_name, self.markets_list, msg=f'"{self.market_name}" section is not present')

        self.__class__.correct_score = self.markets_list.get(self.market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{self.market_name}" section is not found in "{self.markets_list.keys()}"')
        self.correct_score.collapse()
        self.assertFalse(self.correct_score.is_expanded(expected_result=False),
                         msg=f'"{self.market_name}" section is not collapsed')

        self.correct_score.expand()
        self.assertTrue(self.correct_score.is_expanded(),
                        msg=f'"{self.market_name}" section is not expanded')

    def test_003_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If Correct Score has **cashoutAvail="Y"** on Market level then label Cash out is displayed
        """
        self.assertTrue(self.correct_score.market_section_header.has_cash_out_mark(),
                        msg=f'Market "{self.correct_score}" has no cashout label')

    def test_004_expand_correct_score_market_section(self):
        """
        DESCRIPTION: Expand 'Correct Score' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Two pickers (<Home Team> <Away Team>)
        EXPECTED: *   **Price/Odds** button with associated price
        EXPECTED: *   **'Show All' **option with all Correct Score outcomes
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

    def test_005_verify_home_team___away_team_pickers(self):
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

    def test_006_clicktap_on_show_all_option(self):
        """
        DESCRIPTION: Click/Tap on 'Show All' option
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

    def test_007_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   selection of 'Home Team' are shown on the left side
        EXPECTED: *   selection of 'Draw' are shown in the middle
        EXPECTED: *   selection of 'Away Team' are shown on the right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        # Verification was done in previous step, where Home / Draw / Away
        # expected and actual selections lists are compared

    def test_008_verify_any_other_selections_displaying(self):
        """
        DESCRIPTION: Verify Any other selections displaying
        EXPECTED: *   selection of 'Home Any other' are shown on the bottom left side
        EXPECTED: *   selection of 'Away Any other' are shown on the bottom right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        # Verification was done in previous step, where Home / Draw / Away
        # expected and actual selections lists are compared

    def test_009_verify_selections_sortening(self):
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

        away_outcomes = self.correct_score.outcome_table.away_outcomes.items_names
        self.assertEquals(away_outcomes, sorted(away_outcomes),
                          msg='Outcomes of away team results are not sorted by team score')

    def test_010_clicktap_on_show_less_button(self):
        """
        DESCRIPTION: Click/Tap on 'Show Less' button
        EXPECTED: *   Section with Correct Score outcomes is collapsed
        EXPECTED: *   Button name is changed to 'Show All'
        """
        self.correct_score.show_less_button.click()
        self.assertFalse(self.correct_score.outcome_table.is_displayed(expected_result=False, timeout=2),
                         msg='Outcome table remains displayed')
        self.assertTrue(self.correct_score.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_011_add_any_hda___any_other_selection_to_betslip(self):
        """
        DESCRIPTION: Add any H/D/A - Any other selection to Betslip.
        EXPECTED: Selection should be added successfully
        """
        self.correct_score.show_all_button.click()
        self.assertTrue(self.correct_score.has_show_less_button(), msg='"SHOW LESS" button is not present')

        home_outcome = self.correct_score.outcome_table.home_outcomes.items[0]
        home_outcome.bet_button.click()

        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(home_outcome.bet_button.is_selected(timeout=2),
                        msg=f'Bet button "{home_outcome.bet_button}" is not active after selection')

    def test_012_click_on_place_betverify_bet_receiptverify_settled_bets_after_it_is_settled(self):
        """
        DESCRIPTION: Click on Place Bet
        DESCRIPTION: Verify Bet receipt
        DESCRIPTION: Verify settled bets after it is settled.
        EXPECTED: Bet should be placed and Bet receipt is displayed.
        EXPECTED: The selection must be settled ad name should be displayed as expected.
        """
        self.navigate_to_page('Home')
        self.site.wait_content_state('Homepage')
        self.site.login()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
