import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.mocked_data
@pytest.mark.desktop
@pytest.mark.banach
@pytest.mark.login
@vtest
class Test_C2490965_Banach_Trigger_selections_dashboard_and_price(BaseBanachTest):
    """
    TR_ID: C2490965
    NAME: Banach. Trigger selections dashboard and price
    DESCRIPTION: This test case verifies triggering Banach selections dashboard and price generation
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Examples of combinable Banach markets:**
    PRECONDITIONS: Match Result or Both teams to score + Double Chance + Anytime goalscorer + Over/Under markets + Correct Score
    PRECONDITIONS: Check price value: Open Dev tools > Network > **price** request
    PRECONDITIONS: **Build Your Bet tab on event details page with Banach markets is loaded**
    PRECONDITIONS: **App local storage is cleared**
    """
    keep_browser_open = True
    team1, team2 = 'Test Team 1', 'Test Team 2'
    both_team_to_score_selection = 'Yes'
    expected_default_place_bet_text = vec.yourcall.PLACE_BET
    summary_block = None
    blocked_hosts = ['*spark-br.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Build Your Bet tab on event details page with Banach markets is loaded
        """
        self.__class__.eventID = self.create_ob_event_for_mock(team1=self.team1, team2=self.team2)
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_001_add_only_one_selection_to_dashboard(self):
        """
        DESCRIPTION: Add only one selection to dashboard
        EXPECTED: - Dashboard appears with slide animation and is expanded (when selection is added for the first time)
        EXPECTED: - **Please add another selection to place the bet** notification is shown above the dashboard
        """
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting,
                                            selection_name=self.team1)
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='Yourcall dashboard is not available')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertEqual(dashboard_panel.info_panel.text, vec.yourcall.DASHBOARD_ALERT,
                         msg='Infopanel text: "%s" is not the same as expected: "%s"' %
                             (dashboard_panel.info_panel.text,
                              vec.yourcall.DASHBOARD_ALERT))
        self.assertTrue(dashboard_panel.is_expanded(), msg='BYB Dashboard is not expanded')

    def test_002_add_one_more_selection_from_combinable_markets_accordions(self):
        """
        DESCRIPTION: Add one more selection from combinable markets accordions
        EXPECTED: - Notification disappears
        EXPECTED: - Odds area appears next to dashboard header
        EXPECTED: - Selections are highlighted within accordions
        """
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.both_teams_to_score,
                                            selection_name=self.both_team_to_score_selection)
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='Yourcall dashboard is not available')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertFalse(dashboard_panel.wait_for_info_panel(expected_result=False, timeout=2))
        self.assertTrue(dashboard_panel.is_expanded(), msg='BYB Dashboard is not expanded')
        self.__class__.summary_block = dashboard_panel.byb_summary
        self.__class__.odds = self.summary_block.place_bet.value
        self.assertTrue(self.odds, msg='Can not get odds for given selections')

        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg='Can not get market "{self.expected_market_sections.match_result}"')
        match_betting_outcomes = match_betting.outcomes.items_as_ordered_dict
        self.assertTrue(match_betting_outcomes, msg='No outcomes found in Match Betting section')
        team1_outcome = match_betting_outcomes.get(self.team1)
        self.assertTrue(team1_outcome, msg=f'Outcome "{self.team1}" not found among '
                                           f'Match Betting outcomes "{match_betting_outcomes.keys()}"')
        self.assertTrue(team1_outcome.bet_button.is_selected())

        both_teams_to_score = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score, msg='Can not get market "{self.expected_market_sections.match_result}"')
        both_teams_to_score_outcomes = both_teams_to_score.outcomes.items_as_ordered_dict
        self.assertTrue(both_teams_to_score_outcomes, msg='No outcomes found in Both Teams to Score section')
        yes_outcome = both_teams_to_score_outcomes.get(self.both_team_to_score_selection)
        self.assertTrue(yes_outcome, msg=f'Outcome "Yes" not found among '
                                         f'Both Teams to Score outcomes "{both_teams_to_score_outcomes.keys()}"')
        self.assertTrue(yes_outcome.bet_button.is_selected())

    def test_003_verify_odds_area_for_fractional_format(self):
        """
        DESCRIPTION: Verify Odds area
        EXPECTED: - Odds value taken from **price** response is displayed TODO VOL-1815 this check cannot be done for now
        EXPECTED: - Odds are displayed in format (decimal/ fractional) defined in Settings
        EXPECTED: - PLACE BET text below odds
        """
        odds = self.summary_block.place_bet.value_text
        self.assertRegexpMatches(odds, self.fractional_pattern,
                                 msg=f'Odds value for current selections combination "{odds}" '
                                     f'is not in correct format "{self.fractional_pattern}"'
                                 )
        self.assertEqual(self.summary_block.place_bet.text, self.expected_default_place_bet_text,
                         msg=f'Place bet button text: "{self.summary_block.place_bet.text}" is not the same '
                             f'as expected: "{self.expected_default_place_bet_text}"')

    def test_004_change_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: Odds format is changed
        """
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')
        self.__class__.expected_pattern = self.decimal_pattern

    def test_005_navigate_to_byb_edp(self):
        """
        DESCRIPTION: Navigate back to EDP of event that has Banach markets and select Build Your Bet tab
        EXPECTED: Build Your Bet tab on event details page with Banach markets is loaded
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_006_verify_odds_area_on_byb_dashboard(self):
        """
        DESCRIPTION: Verify Odds area for decimal odds format
        EXPECTED: Odds format is changed
        EXPECTED: - PLACE BET text below odds
        """
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(timeout=15),
                        msg='Build Your Bet Dashboard panel not displayed')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        summary_block = dashboard_panel.byb_summary

        odds = summary_block.place_bet.value_text
        self.assertRegexpMatches(odds, self.expected_pattern,
                                 msg=f'Odds value for current selections combination "{odds}" '
                                     f'is not in correct format "{self.expected_pattern}"'
                                 )
        self.assertEqual(summary_block.place_bet.text, self.expected_default_place_bet_text,
                         msg=f'Place bet button text: "{summary_block.place_bet.text}" is not the same as expected:'
                             f' "{self.expected_default_place_bet_text}"')

    def test_007_remove_all_selections_from_dashboard(self):
        """
        DESCRIPTION: Remove all selections from Dashboard
        EXPECTED: Dashboard is not displayed anymore on EDP
        """
        self.remove_all_selections_from_dashboard()

    def test_008_add_only_one_selection_to_dashboard_from_player_bets_market(self):
        """
        DESCRIPTION: Add only one selection to dashboard from 'Player bets' market
        EXPECTED: - Odds value taken from **price** response is displayed next to dashboard header TODO VOL-1815 this check cannot be done for now
        EXPECTED: - Odds are displayed in a format (decimal/ fractional) defined in Settings
        EXPECTED: - PLACE BET text below odds
        EXPECTED: - Selections are highlighted within accordions
        """
        self.add_player_bet_selection_to_dashboard(player_index=1,
                                                   statistic_index=1,
                                                   statistic_value_index=1)
        self.test_006_verify_odds_area_on_byb_dashboard()

    def test_009_change_odds_format_back_to_fractional(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Fractional
        EXPECTED: Odds format is changed
        """
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(result, msg='Odds format is not changed to Fractional')
        self.__class__.expected_pattern = self.fractional_pattern

    def test_010_go_back_to_byb_edp_and_verify_odds_format(self):
        """
        DESCRIPTION: Navigate to BYB EDP
        DESCRIPTION: Verify odds format
        """
        self.test_005_navigate_to_byb_edp()
        self.test_006_verify_odds_area_on_byb_dashboard()
