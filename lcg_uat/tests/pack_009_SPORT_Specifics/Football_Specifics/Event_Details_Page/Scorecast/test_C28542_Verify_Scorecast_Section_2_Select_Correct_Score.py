import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.event_details
@pytest.mark.sports
@vtest
class Test_C28542_Verify_Scorecast_Section_2_Select_Correct_Score(BaseSportTest):
    """
    TR_ID: C28542
    NAME: Verify Scorecast Section 2 (Select Correct Score)
    DESCRIPTION: This test case verifies the functionality of Scorecast market section within Football event details page.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: create event and add scorecast market
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event.event_id
        self.__class__.team1 = event.team1
        self.__class__.team2 = event.team2

    def test_001_open_football_event_details_page(self):
        """
        DESCRIPTION: Open Football Event Detail Page
        EXPECTED: Football Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails')

    def test_002_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: Scorecast market section is present and shown after 'Correct Score' market
        """
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets are shown')
        markets_list = list(self.markets.keys())

        self.assertTrue(markets_list.index(self.expected_market_sections.correct_score) + 1 ==
                        markets_list.index(self.expected_market_sections.scorecast),
                        msg='Scorecast market is not shown after Correct Score market')

    def test_003_verify_section_2_select_result(self):
        """
        DESCRIPTION: Verify section 2 (Select Result)
        EXPECTED: Section 2 consists of:
        EXPECTED: - 'Correct Score' drop down
        EXPECTED: - Lowest available goals number for each team is selected by default (0, 0)
        EXPECTED: - 'Odds calculation' button is displayed as greyed out with 'N/A' inscription if selected combination of outcomes is not valid
        EXPECTED: - 'Odds calculation' button is displayed with appropriate price button when goals are selected in both dropdowns
        """
        self.__class__.scorecast = self.markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(self.scorecast, msg=f'{self.expected_market_sections.scorecast} section is not found')

        self.assertTrue(self.scorecast.home_team_results_dropdown.is_displayed(), msg='Home team result drop-down is not present')
        self.assertTrue(self.scorecast.away_team_results_dropdown.is_displayed(), msg='Away team result drop-down is not present')

        self.assertEqual(self.scorecast.home_team_results_dropdown.selected_item, '0',
                         msg='Default value for home team result drop-down is not "0"')
        self.assertEqual(self.scorecast.away_team_results_dropdown.selected_item, '0',
                         msg='Default value for away team result drop-down is not "0"')

        self.assertFalse(self.scorecast.add_to_betslip.is_enabled(expected_result=False),
                         msg='Add to betslip button is not disabled in case of invalid result selection')
        self.assertEqual(self.scorecast.add_to_betslip.name, 'N/A',
                         msg=f'Add to betslip button price "{self.scorecast.add_to_betslip.name}" '
                             f'is not the same as expected "N/A" in case of invalid result selection')

        self.scorecast.home_team_results_dropdown.select_value('2')
        self.scorecast.away_team_results_dropdown.select_value('1')

        # To make add to betslip button enabled
        last_market = self.markets.get(list(self.markets.keys())[-1])
        last_market.expand() if self.device_type == 'mobile' else last_market.collapse()

        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(timeout=3),
                        msg='Add to betslip button is not enabled in case of valid result selection')
        self.assertNotEqual(self.scorecast.add_to_betslip.name, 'N/A',
                            msg=f'Add to betslip button price "{self.scorecast.add_to_betslip.name}" '
                                f'is "N/A" in case of valid result selection')

    def test_004_verify_correct_score_drop_downs(self):
        """
        DESCRIPTION: Verify 'Correct Score' drop downs
        EXPECTED: Each drop down contain goal numbers (e.g. 0,1,2,3,4,5,6,7,8,9...)
        EXPECTED: Goal numbers are displayed numerically from lowest score to highest
        EXPECTED: The min/max goal numbers in drop-down is taken from SS
        EXPECTED: Combinations of goals are received from OB in attributes that are present on the outcome level in format: **outcomeMeaningScores="X,Y," **
        """
        home_goals_list = []
        away_goals_list = []
        response = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)
        for node in response[0]['event']['children']:
            if node['market']['templateMarketName'] == '|Correct Score|':
                for outcome_node in node['market']['children']:
                    home_goals_list.append(outcome_node['outcome']['outcomeMeaningScores'][0])
                    away_goals_list.append(outcome_node['outcome']['outcomeMeaningScores'][2])

        home_goals_set = set(home_goals_list)
        away_goals_set = set(away_goals_list)

        self.assertEqual(self.scorecast.home_team_results_dropdown.available_options, sorted(home_goals_set),
                         msg=f'Home team results drop-down does not contain the same list of options. '
                             f'Actual: {self.scorecast.home_team_results_dropdown.available_options}. '
                             f'Expected: {sorted(home_goals_set)}.')
        self.assertEqual(self.scorecast.away_team_results_dropdown.available_options, sorted(away_goals_set),
                         msg=f'Away team results drop-down does not contain the same list of options. '
                             f'Actual: {self.scorecast.home_team_results_dropdown.available_options}. '
                             f'Expected: {sorted(home_goals_set)}.')
