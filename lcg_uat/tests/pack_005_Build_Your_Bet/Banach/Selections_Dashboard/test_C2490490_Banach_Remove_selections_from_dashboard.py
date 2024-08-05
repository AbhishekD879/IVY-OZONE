import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
import voltron.environments.constants as vec


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.banach
@pytest.mark.high
@pytest.mark.desktop
@vtest
class Test_C2490490_Banach_Remove_selections_from_dashboard(BaseBanachTest):
    """
    TR_ID: C2490490
    NAME: Banach Remove selections from dashboard
    DESCRIPTION: This test case verifies possibility to delete dashboard selections by tapping on Delete button or on selections inside accordions
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: For Odds calculation check Dev tools > Network: price request
    PRECONDITIONS: **Banach selections are added to dashboard**
    PRECONDITIONS: **Dashboard is expanded**
    """
    keep_browser_open = True
    team1, team2 = 'Test Team 1', 'Test Team 2'
    initial_odds = None
    dashboard_markets_list = None
    match_betting_market_and_selection_name = None
    double_chance_market_and_selection_name = None
    correct_score_market_and_selection_name = None
    both_teams_to_score_market_and_selection_name = None
    expected_all_markets_and_selections = []
    blocked_hosts = ["*spark-br.*"]

    def verify_dashboard_after_removing_selection(self) -> None:
        """
        Verifying if:
        - Selection is removed from dashboard
        - Top selection name is updated on dashboard header
        - Selections counter is updated on the dashboard header
        - Odds value updated
        """
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel

        dashboard_summary_markets = dashboard_panel.byb_summary.summary_description.dashboard_market_text
        self._logger.debug('*** Dashboard Markets and selection list: "%s"' % dashboard_summary_markets)
        self.assertTrue(dashboard_summary_markets,
                        msg=f'Dashboard summary markets text is empty "{dashboard_summary_markets}"')
        dashboard_summary_markets = dashboard_summary_markets.split(', ')
        self.assertEqual(dashboard_summary_markets, self.expected_all_markets_and_selections,
                         msg=f'List of markets selections: "{dashboard_summary_markets}" are not the same as expected '
                             f'"{self.expected_all_markets_and_selections}"')

        counter_value = dashboard_panel.byb_summary.summary_counter.value
        self.assertEqual(int(counter_value), self.initial_counter,
                         msg=f'Number of added selections "{counter_value}" is not the same as added "{self.initial_counter}"')

        updated_odds = dashboard_panel.byb_summary.place_bet.value_text
        self.assertNotEqual(updated_odds, self.initial_odds,
                            msg=f'Odds value seems not updated, actual odds: "{updated_odds}", initial odds: "{self.initial_odds}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: At least 4 Banach selections are added to dashboard
        DESCRIPTION: Dashboard is expanded
        """
        self.__class__.eventID = self.create_ob_event_for_mock(team1=self.team1, team2=self.team2)
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting 90 mins selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting_default_switcher = match_betting.grouping_buttons.current
        match_betting_selection_names = match_betting.set_market_selection(selection_name=self.team1)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        self.__class__.match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                                                                 f'{match_betting_default_switcher.lower()} ' \
                                                                 f'{self.team1.upper()}'
        self.__class__.expected_all_markets_and_selections.append(self.match_betting_market_and_selection_name.upper())

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.__class__.initial_counter += 1

        # Double chance selection
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_default_switcher = double_chance_market.grouping_buttons.current
        double_chance_selection_names = double_chance_market.set_market_selection(count=1)
        self.assertTrue(double_chance_selection_names, msg='No one selection added to Dashboard')
        self.__class__.double_chance_market_and_selection_name = f'{self.expected_market_sections.double_chance.title()} ' \
                                                                 f'{double_chance_default_switcher.lower()} ' \
                                                                 f'{double_chance_selection_names[0].upper()}'

        self.__class__.expected_all_markets_and_selections.append(self.double_chance_market_and_selection_name.upper())

        self.__class__.initial_counter += 1

        # Both teams to score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        both_teams_to_score_selection_names = both_teams_to_score_market.set_market_selection(count=1)
        self.assertTrue(both_teams_to_score_selection_names, msg='No one selection added to Dashboard')
        self.__class__.both_teams_to_score_market_and_selection_name = f'{self.expected_market_sections.both_teams_to_score.title()} ' \
                                                                       f'{both_teams_to_score_selection_names[0].upper()}'

        self.__class__.expected_all_markets_and_selections.append(self.both_teams_to_score_market_and_selection_name.upper())

        self.__class__.initial_counter += 1

        # Correct score selection
        correct_score_market = self.get_market(market_name=self.expected_market_sections.correct_score)
        correct_score_default_switcher = correct_score_market.grouping_buttons.current
        team_a_scores = correct_score_market.team_away_scores
        team_h_scores = correct_score_market.team_home_scores

        team_h_scores.select_score_by_text(text='1')
        team_a_scores.select_score_by_text(text='1')
        correct_score_selection = 'DRAW 1-1'
        self._logger.debug(f'*** Correct score selection: "{correct_score_selection}"')

        self.__class__.correct_score_market_and_selection_name = f'{self.expected_market_sections.correct_score.title()} ' \
                                                                 f'{correct_score_default_switcher.lower()} ' \
                                                                 f'{correct_score_selection}'
        correct_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.__class__.initial_counter += 1

        self.__class__.expected_all_markets_and_selections.append(self.correct_score_market_and_selection_name.upper())

        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        is_expanded = dashboard_panel.is_expanded()
        self.assertTrue(is_expanded, msg='Dashboard is not expanded')

        self.__class__.initial_odds = dashboard_panel.byb_summary.place_bet.value_text
        self.assertTrue(self.initial_odds, msg='Can not get odds for given selections')

    def test_001_tap_remove_button_for_the_top_selection_inside_dashboard(self):
        """
        DESCRIPTION: Tap "Remove" button for the top selection inside dashboard
        EXPECTED: - Selection is not highlighted within market accordion
        EXPECTED: - Selection is removed from dashboard
        EXPECTED: - Top selection name is updated on dashboard header
        EXPECTED: - Selections counter is updated on the dashboard header
        EXPECTED: - Odds value updated (from **price** request)
        """
        dashboard_match_betting_outcome = self.get_byb_dashboard_outcome(name=self.match_betting_market_and_selection_name)
        dashboard_match_betting_outcome.remove_button.click()
        self.expected_all_markets_and_selections.remove(self.match_betting_market_and_selection_name.upper())

        self.__class__.initial_counter -= 1

        result = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.assertTrue(result, msg='Number of selections has not decreased')

        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg='Can not get market "{self.expected_market_sections.match_result}"')
        match_betting_outcomes = match_betting.outcomes.items_as_ordered_dict
        self.assertTrue(match_betting_outcomes, msg='No outcomes found in Match Betting section')
        team1_outcome = match_betting_outcomes.get(self.team1)
        self.assertTrue(team1_outcome,
                        msg=f'Outcome "{self.team1}" not found among Match Betting outcomes "{match_betting_outcomes.keys()}"')
        self.assertFalse(team1_outcome.bet_button.is_selected(expected_result=False))

        dashboard_outcomes = self.get_byb_dashboard_outcomes()

        self.assertNotIn(self.match_betting_market_and_selection_name, dashboard_outcomes.keys(),
                         msg=f'{self.match_betting_market_and_selection_name} was not found in list'
                             f' of dashboard outcomes "{dashboard_outcomes.keys()}"')

        self.verify_dashboard_after_removing_selection()

    def test_002_tap_on_the_selection_in_market_accordion(self):
        """
        DESCRIPTION: Tap on the selection that is added to Dashboard in market accordion
        EXPECTED: - Selection is not highlighted within market accordion
        EXPECTED: - Selection is removed from dashboard
        EXPECTED: - Top selection name is updated on dashboard header
        EXPECTED: - Selections counter is updated on the dashboard header
        EXPECTED: - Odds value updated (from **price** request)
        """
        both_teams_to_score = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score, msg=f'Can not get market "{self.expected_market_sections.both_teams_to_score}"')
        both_teams_to_score_outcomes = both_teams_to_score.outcomes.items_as_ordered_dict
        self.assertTrue(both_teams_to_score_outcomes, msg=f'No outcomes found in "{self.expected_market_sections.both_teams_to_score}" section')
        yes_outcome = both_teams_to_score_outcomes.get('Yes')
        self.assertTrue(yes_outcome,
                        msg=f'Outcome "Yes" not found among Both Teams to Score outcomes "{both_teams_to_score_outcomes.keys()}"')
        yes_outcome.bet_button.click()
        self.assertFalse(yes_outcome.bet_button.is_selected(expected_result=False, timeout=1))

        self.expected_all_markets_and_selections.remove(self.both_teams_to_score_market_and_selection_name.upper())

        self.__class__.initial_counter -= 1

        result = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.assertTrue(result, msg='Number of selections has not decreased')

        dashboard_outcomes = self.get_byb_dashboard_outcomes()

        self.assertNotIn(self.both_teams_to_score_market_and_selection_name, dashboard_outcomes.keys(),
                         msg=f'{self.both_teams_to_score_market_and_selection_name} was not found in list'
                             f' of dashboard outcomes "{dashboard_outcomes.keys()}"')

        self.verify_dashboard_after_removing_selection()

    def test_003_remove_more_selections_to_have_1_onlyby_tapping_remove_button_or_tapping_on_selections_in_market_accordions(self):
        """
        DESCRIPTION: Remove more selections to have 1 only
        DESCRIPTION: (by tapping Remove button or tapping on selections in market accordions)
        EXPECTED: - **Please add another selection to place bet** message appears above dashboard header
        """
        correct_score_dashboard_outcome = self.get_byb_dashboard_outcome(
            name=self.correct_score_market_and_selection_name)
        correct_score_dashboard_outcome.remove_button.click()
        self.expected_all_markets_and_selections.remove(self.correct_score_market_and_selection_name.upper())

        self.__class__.initial_counter -= 1
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel

        result = dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.assertTrue(result, msg='Number of selections has not decreased')

        counter_value = dashboard_panel.byb_summary.summary_counter.value
        self.assertEqual(int(counter_value), self.initial_counter,
                         msg=f'Number of added selections "{counter_value}" '
                         f'is not the same as added "{self.initial_counter}"')

        self.assertEqual(dashboard_panel.info_panel.text, vec.yourcall.DASHBOARD_ALERT,
                         msg='Info panel text: "%s" is not the same as expected: "%s"' %
                             (dashboard_panel.info_panel.text,
                              vec.yourcall.DASHBOARD_ALERT))

    def test_004_remove_the_last_selection(self):
        """
        DESCRIPTION: Remove the last selection
        EXPECTED: - Dashboard disappears
        EXPECTED: - Message disappears
        """
        double_chance_dashboard_outcome = self.get_byb_dashboard_outcome(name=self.double_chance_market_and_selection_name)
        double_chance_dashboard_outcome.remove_button.click()
        self.expected_all_markets_and_selections.remove(self.double_chance_market_and_selection_name.upper())

        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')
