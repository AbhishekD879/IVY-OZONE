import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2  # Need to update for QA2 envs once envs are fine
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28487_Verify_Correct_Score_selections_display(Common):
    """
    TR_ID: C28487meaningMinor
    NAME: Verify 'Correct Score' selections display
    DESCRIPTION: This test case verifies 'Correct Score' selections displaying.
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Please check the Selections Order for 'Correct Score' Market in the table using the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Generic+Sport+Template+-+Selections+Display+Rules
    PRECONDITIONS: 3) A valid market "Correct Score" must have** dispSortName="CS"**
    """
    keep_browser_open = True
    def outcome_values(self, outcomes='', flag=False):
        y = 0 if flag is False else 1
        outcome_value = []
        for outcome in range(len(outcomes)):
            outcome_value.append(outcomes[outcome].text.split('\n'))
        return outcome_value[y]

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        if tests.settings.backend_env == 'prod':
            event = \
                self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.outcomes = next(((market['market']['children']) for market in event['event']['children']
                                            if 'Correct Score' in market['market']['templateMarketName'] and
                                            market['market'].get('children')), None)
            if self.outcomes is None:
                raise SiteServeException('There are no available outcomes')

            self._logger.info(f'*** Football event with event id "{self.eventID}"')
        else:
            pass

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>'  icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        # Covered in Step# 3

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_004_go_to_correct_score_market_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' Market section
        EXPECTED: It is possible to collapse/expand Market section by tapping the section's header
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')
        if self.brand == 'bma':
            if self.device_type == 'desktop':
                market_name = self.expected_market_sections.correct_score.title()
            else:
                market_name = self.expected_market_sections.correct_score
        else:
            market_name = 'Correct score'
        self.assertIn(market_name, markets_list, msg=f'"{market_name}" section is not present')

        self.__class__.correct_score = markets_list.get(market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{market_name}" section is not found in "{markets_list.keys()}"')
        self.correct_score.collapse()
        self.assertFalse(self.correct_score.is_expanded(expected_result=False),
                         msg=f'"{market_name}" section is not collapsed')

        self.correct_score.expand()
        self.assertTrue(self.correct_score.is_expanded(),
                        msg=f'"{market_name}" section is not expanded')

    def test_005_checkoutcomemeaningscores_attributes_of_selections_in_eventidsimplefilter_response_eventchildrencorrect_score_marketchildrenoutcome_hierarchy(
            self):
        """
        DESCRIPTION: Check **outcomeMeaningScores **attributes of selections in '<EventID>?simpleFilter' response (Event/Children/Correct Score market/Children/Outcome hierarchy)
        EXPECTED: **outcomeMeaningScores **attributes of selections are present on the outcome level in format:
        EXPECTED: **outcomeMeaningScores="X,Y,"**
        EXPECTED: where X - score belongs to Home team, Y - to Away team
        """
        pattern = r'^\d+\,\d+\,+$'
        for i in self.outcomes:
            score = i['outcome']['outcomeMeaningScores']
            self.assertTrue(score, msg=f'"outcomeMeaningScores" attribute is not available for selection "{i["outcome"]}"')
            self.assertRegexpMatches(score, pattern,
                                     msg=f'Score "{score}" not matching pattern: "{pattern}"')

    def test_006_check_number_of_columns_and_grouping_for_correct_score_market(self):
        """
        DESCRIPTION: Check number of columns and grouping for 'Correct Score' Market
        EXPECTED: *   **2 columns** if there are NO **outcomeMeaningScores **attributes where X=Y
        EXPECTED: Team/Player 1
        EXPECTED: ‘outcomeMeaningScores=( X>Y )’ is a Home Win
        EXPECTED: Team/Player 2
        EXPECTED: ‘outcomeMeaningScores=( X<Y )’ - is an Away Win
        EXPECTED: *   **3 columns **if there are **outcomeMeaningScores **attributes where X=Y
        EXPECTED: Team/Player 1
        EXPECTED: ‘outcomeMeaningScores=( X>Y )’ is a Home Win
        EXPECTED: Draw
        EXPECTED: ‘outcomeMeaningScores=( X=Y )’ is a Draw
        EXPECTED: Team/Player 2
        EXPECTED: ‘outcomeMeaningScores=( X<Y )’ - is an Away Win
        """
        self.assertTrue(self.correct_score.team_home_scores, msg='Home team result drop-down is not present')
        self.assertTrue(self.correct_score.team_away_scores, msg='Away team result drop-down is not present')

        self.assertEquals(self.correct_score.team_home_scores.selected_item, '0',
                          msg='Default value for home team result drop-down is not "0"')
        self.assertEquals(self.correct_score.team_away_scores.selected_item, '0',
                          msg='Default value for away team result drop-down is not "0"')

        self.correct_score.show_all_button.click()
        self.assertTrue(self.correct_score.has_show_less_button(), msg='"SHOW LESS" button is not present')

        self.__class__.home_outcomes = self.correct_score.outcome_table.home_outcomes
        self.__class__.home_outcome_values = self.outcome_values(self.home_outcomes)


        self.assertEquals(self.home_outcome_values, sorted(self.home_outcome_values),
                          msg='Outcomes for home team results are not sorted by team score')

        self.__class__.draw_outcomes = self.correct_score.outcome_table.draw_outcomes
        self.__class__.draw_outcome_values = self.outcome_values(self.draw_outcomes)
        self.assertEquals(self.draw_outcome_values, sorted(self.draw_outcome_values),
                          msg='Outcomes for draw results are not sorted by team score')

        self.__class__.away_outcomes = self.correct_score.outcome_table.away_outcomes
        self.__class__.away_outcome_values = self.outcome_values(self.away_outcomes)
        self.assertEquals(self.away_outcome_values, sorted(self.away_outcome_values),
                          msg='Outcomes of away team results are not sorted by team score')

    def test_007_check_format_of_selections_names(self):
        """
        DESCRIPTION: Check format of **selections names **
        EXPECTED: Format of selections names is:
        EXPECTED: **'<Score1>-<Score2>'**
        """
        if self.brand=='ladbrokes':
            pattern = r'^[0-9]+\-{1}[0-9]+[0-9]/[0-9]$'
        else:
            pattern=r'^[[0-9]+[0-9]/[0-9]|[0-9]/[0-9]$'
        # home_outcomes = self.correct_score.outcome_table.home_outcomes
        # draw_outcomes = self.correct_score.outcome_table.draw_outcomes
        # away_outcomes = self.correct_score.outcome_table.away_outcomes

        for outcome in self.home_outcome_values:
            self.assertRegexpMatches(outcome.strip(), pattern,
                                     msg=f'Outcome "{outcome}" not matching pattern: "{pattern}"')

        for outcome in self.draw_outcome_values:
            self.assertRegexpMatches(outcome.strip(), pattern,
                                     msg=f'Outcome "{outcome}" not matching pattern: "{pattern}"')

        for outcome in self.away_outcome_values:
            self.assertRegexpMatches(outcome.strip(), pattern,
                                     msg=f'Outcome "{outcome}" not matching pattern: "{pattern}"')

    def test_008_check_selections_order_in_each_column(self):
        """
        DESCRIPTION: Check **selections order** in each column
        EXPECTED: Selections in each column are ordered by the **outcomeMeaningScores **value in ascending order (e.g. 1-0, 2-0, 2-1)
        """
        # Covered in Step# 6

    def test_009_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify Price/Odds buttons
        EXPECTED: Price/Odds buttons are displayed below each selection name
        """
        #home_outcomes = self.correct_score.outcome_table.home_outcomes
        #home_prices = self.correct_score.outcome_table.home_outcomes.outcomes_prices
        home_outcomes_odds = self.outcome_values(self.home_outcomes, flag=True)
        for item in range(len(home_outcomes_odds)):
            self.assertTrue(home_outcomes_odds[item], msg=f'For home outcome "{item}", price/odds "{home_outcomes_odds[item]}" is not available')

        # draw_outcomes = self.correct_score.outcome_table.draw_outcomes.items_names
        # draw_prices = self.correct_score.outcome_table.draw_outcomes.outcomes_prices
        draw_outcomes_odds = self.outcome_values(self.draw_outcomes, flag=True)
        for item in range(len(draw_outcomes_odds)):
            self.assertTrue(draw_outcomes_odds[item], msg=f'For draw outcome "{item}", price/odds "{draw_outcomes_odds[item]}" is not available')

        # away_outcomes = self.correct_score.outcome_table.away_outcomes.items_names
        # away_prices = self.correct_score.outcome_table.away_outcomes.outcomes_prices
        away_outcomes_odds = self.outcome_values(self.away_outcomes, flag=True)
        for item in range(len(away_outcomes_odds)):
            self.assertTrue(away_outcomes_odds[item], msg=f'For away outcome "{item}", price/odds "{away_outcomes_odds[item]}" is not available')
