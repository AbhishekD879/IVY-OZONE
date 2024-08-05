import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.user_journey_in_play_betting
@pytest.mark.event_details
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C820529_Verify_newly_created_markets_selections_on_Sport_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C820529
    NAME: Verify newly created markets/selections on Sport Event Details Page
    DESCRIPTION: This test case verifies automatically displaying newly created markets/selections on In-Play/Pre-Match <Sport> Event Details Page
    PRECONDITIONS: - Live and Pre Match events are available
    PRECONDITIONS: - To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    over_under_total_goals_market = 'over_under_total_goals'

    def test_001_create_test_event(self):
        """
        DESCRIPTION: Create test event
        """
        cms = self.get_initial_data_system_configuration()
        ss_live_markets_config = cms.get('SiteServerLiveMarkets')
        if not ss_live_markets_config:
            ss_live_markets_config = self.cms_config.get_system_configuration_item('SiteServerLiveMarkets')
        if not ss_live_markets_config:
            raise CmsClientException(f'"SiteServerLiveMarkets" config not found in CMS')
        ss_live_markets_config_enabled = ss_live_markets_config.get('enabled')
        if not ss_live_markets_config_enabled:
            raise CmsClientException(f'"SiteServerLiveMarkets" config not enabled in CMS')
        ss_live_markets_config_categories = ss_live_markets_config.get('sportCategoriesIds')
        if ss_live_markets_config_categories is None:
            raise CmsClientException(f'"SiteServerLiveMarkets" config not contains "sportCategoriesIds" section in CMS')
        if ss_live_markets_config_categories != '':
            category_id = self.ob_config.football_config.category_id
            if str(category_id) not in ss_live_markets_config_categories:
                raise CmsClientException(f'Category id "{category_id}" not present in "{ss_live_markets_config_categories}"')

        start_time = self.get_date_time_formatted_string(seconds=10)
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time)
        self.__class__.eventID = event.event_id
        self.__class__.team1 = event.team1
        self.__class__.team2 = event.team2

    def test_002_go_to_in_play_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: Go to In-Play event Details page of <Sport> event
        EXPECTED: Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_in_ti_tool_create_new_market(self):
        """
        DESCRIPTION: In TI tool: Create new market. Add selection(s) to the newly created market
        """
        [self.ob_config.add_custom_markets_with_selections(event_id=self.eventID,
                                                           markets=[(self.over_under_total_goals_market, {'cashout': True, 'over_under': over_under})],
                                                           class_id=self.ob_config.football_config.autotest_class.class_id,
                                                           category_id=self.ob_config.football_config.category_id,
                                                           type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                                                           team1=self.team1,
                                                           team2=self.team2) for over_under in ['1.5', '2.5']]

        self.ob_config.add_custom_markets_with_selections(event_id=self.eventID,
                                                          markets=[('handicap', {'cashout': True})],
                                                          class_id=self.ob_config.football_config.autotest_class.class_id,
                                                          category_id=self.ob_config.football_config.category_id,
                                                          type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                                                          team1=self.team1,
                                                          team2=self.team2)

    def test_004_in_application_verify_opened_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: In application: Verify opened Event Details page of <Sport> event
        EXPECTED: Newly created market with selections automatically appear on the page
        EXPECTED: All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: If new market belongs to a new collection, the collection automatically appears along with the market
        """
        over_under_market_appears = self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(
            item_name=self.expected_market_sections.over_under_total_goals)
        self.assertTrue(over_under_market_appears,
                        msg='Market %s does not appear' % self.expected_market_sections.over_under_total_goals)

        handicap_market_appears = self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(
            item_name=self.expected_market_sections.handicap_results)
        self.assertTrue(handicap_market_appears,
                        msg='Market %s does not appear' % self.expected_market_sections.handicap_results)

        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        market = markets_list.get(self.expected_market_sections.over_under_total_goals)
        self.assertTrue(market, msg='*** Can not find OVER/UNDER TOTAL GOALS section')
        market.expand()
        self.assertTrue(market.is_expanded(), msg='The section OVER/UNDER TOTAL GOALS is not expanded')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are shown for OVER/UNDER TOTAL GOALS market')
        for outcome_name, outcome in outcomes.items():
            result = wait_for_result(lambda: len(outcome.items_as_ordered_dict) == 2,
                                     timeout=5,
                                     name='Bet buttons to appear')
            self.assertTrue(result, msg='Not all buttons are shown for %s' % outcome_name)

        market = markets_list.get(self.expected_market_sections.handicap_results)
        self.assertTrue(market, msg='*** Can not find HANDICAP RESULTS section')
        market.expand()
        self.assertTrue(market.is_expanded(), msg='The section HANDICAP RESULTS is not expanded')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are shown for HANDICAP RESULTS market')
        for outcome_name, outcome in outcomes.items():
            result = wait_for_result(lambda: len(outcome.items_as_ordered_dict) == 3,
                                     timeout=5,
                                     name='Bet buttons to appear')
            self.assertTrue(result, msg='Not all bet buttons are shown for %s' % outcome_name)

    def test_005_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Already created market is displayed with selection(s) in corresponding collection
        """
        tab_appears = self.site.sport_event_details.markets_tabs_list.wait_item_appears(item_name=self.expected_market_tabs.autotest_collection)
        self.assertTrue(tab_appears, msg='Tab %s does not appear' % self.expected_market_tabs.autotest_collection)
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.autotest_collection)

        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.autotest_collection,
                         msg='Autotest Collection is not active tab after click, active tab is %s' % current_tab)
        self.test_004_in_application_verify_opened_event_details_page_of_sport_event()

    def test_006_in_ti_tool_add_another_selection_to_the_market_from_step_4_in_application_verify_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: In TI tool: Add another selection to the market (from step 4) > In application: Verify Event Details page of <Sport> event
        EXPECTED: Newly created selection automatically appears on the page for a corresponding market
        """
        over_under_values = ['3.5', '4.5']
        [self.ob_config.add_custom_markets_with_selections(event_id=self.eventID,
                                                           markets=[(self.over_under_total_goals_market, {'cashout': True, 'over_under': over_under})],
                                                           class_id=self.ob_config.football_config.autotest_class.class_id,
                                                           category_id=self.ob_config.football_config.category_id,
                                                           type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                                                           team1=self.team1,
                                                           team2=self.team2) for over_under in over_under_values]
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        market = markets_list.get(self.expected_market_sections.over_under_total_goals)
        self.assertTrue(market, msg='*** Can not find OVER/UNDER TOTAL GOALS section')
        market.expand()
        self.assertTrue(market.is_expanded(), msg='The section OVER/UNDER TOTAL GOALS is not expanded')
        for over_under in over_under_values:
            market_results = wait_for_result(lambda: over_under in market.outcomes.items_as_ordered_dict,
                                             timeout=3,
                                             name='Market to appear')
            self.assertTrue(market_results, msg='Market %s does not appear' % over_under)
            outcomes = market.outcomes.items_as_ordered_dict
            self.assertIn(over_under, outcomes, msg='OVER/UNDER value "%s" not found in %s' % (over_under, outcomes.keys()))
            buttons_result = wait_for_result(lambda: len(outcomes[over_under].items_as_ordered_dict) == 2,
                                             timeout=3,
                                             name='Bet buttons to appear')
            self.assertTrue(buttons_result, msg='Not all buttons are shown for %s OVER/UNDER value' % over_under)

    # fixme: disabled as corresponding issue BMA-26449 is not fixed for two years
    # def test_007_in_ti_tool_add_combined_market(self):
    #     """
    #     DESCRIPTION: In TI tool: Add combined market
    #     DESCRIPTION: In TI tool: Add selection(s) to one market within combined markets group
    #     """
    #     self.ob_config.add_custom_markets_with_selections(event_id=self.eventID,
    #                                                       markets=[('scorecast', {'cashout': True})],
    #                                                       class_id=self.ob_config.football_config.autotest_class.class_id,
    #                                                       category_id=self.ob_config.football_config.category_id,
    #                                                       type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
    #                                                       team1=self.team1,
    #                                                       team2=self.team2)
    #
    # def test_008_in_application_verify_opened_event_details_page_of_sport_event(self):
    #     """
    #     DESCRIPTION: In application: Verify opened Event Details page of <Sport> event
    #     EXPECTED: Newly created combined market automatically appear on the page
    #     EXPECTED: Added selection(s) is/are displayed for a corresponding market within combined markets group
    #     EXPECTED: No selections are shown for other markets within combined markets group
    #     EXPECTED: All other markets are displayed in their actual state (expanded or collapsed)
    #     EXPECTED: For In-Play <Sport> event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appear
    #     EXPECTED: If new market belongs to a new collection, the collection automatically appears along with the market
    #     """
    #     market_appears = self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(item_name=self.expected_market_sections.scorecast)
    #     self.assertTrue(market_appears, msg='Market %s does not appear' % self.expected_market_sections.scorecast)
    #
    #     markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
    #     self.assertTrue(markets, msg='No markets are shown')
    #     scorecast = markets.get(self.expected_market_sections.scorecast)
    #     self.assertTrue(scorecast, msg='SCORECAST section is not found')
    #     self.assertFalse(scorecast.is_expanded(), msg='Scorecast is not collapsed by default')
    #     scorecast.expand()
    #     is_market_section_expanded = scorecast.is_expanded()
    #     self._logger.info('*** Market section is expanded?: %s' % is_market_section_expanded)
    #     self.assertTrue(is_market_section_expanded, msg='The section %s is not expanded' % scorecast.name)
    #
    #     scorecast.first_scorer_tab.click()
    #     self.assertTrue(scorecast.first_scorer_tab.is_selected(), msg=f'First scorer tab is not selected')
    #
    #     scorecast.last_scorer_tab.click()
    #     self.assertTrue(scorecast.last_scorer_tab.is_selected(), msg=f'Last scorer tab is not selected')
    #     scorecast.first_goalscorer_team_button.click()
    #
    #     first_goalscorer_team_selected = scorecast.first_goalscorer_team_button.is_selected()
    #     self.assertTrue(first_goalscorer_team_selected, msg='First goal scorer team button is not selected')
    #
    #     scorecast.last_goalscorer_team_button.click()
    #
    #     last_goalscorer_team_selected = scorecast.last_goalscorer_team_button.is_selected()
    #     self.assertTrue(last_goalscorer_team_selected, msg='Last goal scorer team button is not selected')
    #
    #     selected_player = scorecast.player_scorers_list.selected_item
    #     self._logger.info('*** Selected player name is: %s' % selected_player)
    #     scorecast.player_scorers_list.select_player_by_index(index=2)
    #
    #     correct_score_teams = scorecast.correct_score_teams.items_as_ordered_dict
    #     for score_team_name, score_team in correct_score_teams:
    #         self._logger.info('*** Correct score team is: %s' % score_team_name)
    #         score_team.click()
    #         button_is_selected = score_team.is_selected()
    #         self.assertTrue(button_is_selected, msg='Score team: "%s" button is not selected' % score_team_name)
    #     scorecast.home_team_results_dropdown.select_value('1')
    #     scorecast.away_team_results_dropdown.select_value('1')
    #     scorecast.player_scorers_list.select_player_by_index(index=2)
    #
    #     self.assertTrue(scorecast.add_to_betslip.is_enabled(), msg='Odds button is not active')
    #
    # def test_009_navigate_through_available_collections(self):
    #     """
    #     DESCRIPTION: Navigate through available collections
    #     EXPECTED: Newly created combined market is displayed with selection(s) in corresponding collections
    #     """
    #     self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.all_markets)
    #
    #     current_tab = self.site.sport_event_details.markets_tabs_list.current
    #     self.assertEqual(current_tab, self.expected_market_tabs.all_markets,
    #                      msg='Autotest Collection is not active tab after click, active tab is %s' % current_tab)
    #     self.test_008_in_application_verify_opened_event_details_page_of_sport_event()

    # fixme: disabled as corresponding story BMA-26771 won't be implemented
    # def test_010_in_ti_tool_add_yourcall_market(self):
    #     """
    #     DESCRIPTION: In TI tool: Add yourcall market
    #     DESCRIPTION: In TI tool: Add selection(s) to one market within combined markets group
    #     """
    #     selections, markets = self.ob_config.add_custom_markets_with_selections(
    #         event_id=self.eventID,
    #         markets=[('your_call', )],
    #         class_id=self.ob_config.football_config.autotest_class.class_id,
    #         category_id=self.ob_config.football_config.category_id,
    #         type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
    #         team1=self.team1,
    #         team2=self.team2)
    #
    #     self.__class__.selection_ids = selections['your_call']
    #
    # def test_011_verify_event_details_page_of_sport_event(self):
    #     """
    #     DESCRIPTION: Verify Event Details page of <Sport> event
    #     """
    #     markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
    #     your_call_market = markets.get(self.expected_market_sections.yourcall_specials_football)
    #     self.assertTrue(your_call_market, msg='"#YourCall Specials" section is not found')
    #     your_call_market.expand()
    #     actual_your_call_markets = your_call_market.items_as_ordered_dict
    #     self.assertTrue(actual_your_call_markets, msg='No one market found in "#YourCall Specials" section')
    #     your_call_markets = [market.upper() for market in self.ob_config.backend.ti.football.your_call_markets]
    #     self.assertListEqual(list(actual_your_call_markets.keys()), your_call_markets,
    #                          msg='Lists are not equal: "%s" with "%s"' %
    #                              (list(actual_your_call_markets.keys()), your_call_markets))
    #     for your_call_market_name, your_call_market in actual_your_call_markets.items():
    #         self.assertTrue(your_call_market.is_expanded(),
    #                         msg='"#YourCall Specials" market: "%s" not expanded by default' % your_call_market_name)
    #         your_call_market.collapse()
    #         self.assertFalse(your_call_market.is_expanded(),
    #                          msg='"#YourCall Specials" market: "%s" was not collapsed' % your_call_market_name)
    #         your_call_market.expand()
    #         self.assertTrue(your_call_market.is_expanded(),
    #                         msg='"#YourCall Specials" market: "%s" was not expanded' % your_call_market_name)
    #         market_selections = your_call_market.items_as_ordered_dict
    #
    #         self.assertTrue(market_selections, msg='Market: "%s" not contains any selections' % your_call_market_name)
    #         expected_selections = list(reversed(self.selection_ids[your_call_market_name.title()].keys()))[:5]
    #         self.assertEqual(list(market_selections.keys()), expected_selections,
    #                          msg='Market: "%s" selections list: \n[%s] \ndoes not match with expected: \n[%s]'
    #                              % (your_call_market_name,
    #                                 ',\n'.join(list(market_selections.keys())),
    #                                 ',\n'.join(expected_selections)))
    #
    # def test_012_navigate_through_available_collections(self):
    #     """
    #     DESCRIPTION: Navigate through available collections
    #     EXPECTED: Newly created combined market is displayed with selection(s) in corresponding collections
    #     """
    #     tab_appears = self.site.sport_event_details.markets_tabs_list.wait_item_appears(item_name=self.expected_market_tabs.yourcall)
    #     self.assertTrue(tab_appears, msg='Tab %s does not appear' % self.expected_market_tabs.build_your_bet)
    #     self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.build_your_bet)
    #
    #     current_tab = self.site.sport_event_details.markets_tabs_list.current
    #     self.assertEqual(current_tab, self.expected_market_tabs.yourcall,
    #                      msg='Autotest Collection is not active tab after click, active tab is %s' % current_tab)
    #     self.test_011_verify_event_details_page_of_sport_event()
