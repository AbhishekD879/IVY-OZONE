import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.event_details
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.markets
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C849464_Verify_automatically_displaying_undisplayed_markets_selections_on_Sport_event_details_page(BaseSportTest):
    """
    TR_ID: C849464
    NAME: Verify automatically displaying undisplayed markets/selections on Sport event details page
    DESCRIPTION: This test case verifies automatically displaying undisplayed markets/selections on In-Play/Pre-Match <Sport> Event Details Page
    PRECONDITIONS: - Live and Pre Match events are available
    PRECONDITIONS: - To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    extra_time_result_market_name = 'extra_time_result'
    scorecast_market_name = 'scorecast'

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

        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event.event_id
        self.__class__.team1 = event.team1
        self.__class__.team2 = event.team2
        self.__class__.selection_ids = event.selection_ids
        self.__class__.extra_time_result_market = self.expected_market_sections.extra_time_result

    def test_002_go_to_match_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: Go to event Details page of <Sport> event
        EXPECTED: Event Details page is opened
        EXPECTED: Main Markets collection is opened by default
        EXPECTED: Corresponding markets are displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        expected_tab = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        self.assertEqual(current_tab, expected_tab,
                         msg=f'"{expected_tab}" is not active tab, active tab is "{current_tab}"')

    def test_003_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        EXPECTED: All available markets are displayed
        """
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.all_markets,
                         msg='All Markets is not active tab after click, active tab is %s' % current_tab)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        match_result = markets.get(self.expected_market_sections.match_result)
        self.assertTrue(match_result, msg='MATCH RESULT section is not found')

    def test_004_in_ti_tool_create_undisplayed_market_plus_undisplayed_selection_for_opened_sport_event(self):
        """
        DESCRIPTION: In TI tool: Create undisplayed market + undisplayed selection for opened <Sport> event
        EXPECTED: Undisplayed market & selection are created in TI tool
        """
        selections, markets = self.ob_config.add_custom_markets_with_selections(event_id=self.eventID,
                                                                                markets=[(self.extra_time_result_market_name, {'cashout': True})],
                                                                                class_id=self.ob_config.football_config.autotest_class.class_id,
                                                                                category_id=self.ob_config.football_config.category_id,
                                                                                type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                                                                                market_displayed=False,
                                                                                selections_displayed=False,
                                                                                team1=self.team1,
                                                                                team2=self.team2)
        self.__class__.extra_time_selection_ids = selections[self.extra_time_result_market_name]
        self.__class__.marketID = markets[self.extra_time_result_market_name]

    def test_005_in_ti_tool_display_market_then_display_selection_for_opened_sport_event(self):
        """
        DESCRIPTION: In TI tool: Display market then display selection for opened <Sport> event
        EXPECTED: Market and its selection are displayed
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)

        [self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)
         for selection_name, selection_id in self.extra_time_selection_ids.items()]

    def test_006_in_application_verify_opened_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: In application: Verify opened Event Details page of <Sport> event
        EXPECTED: Displayed market with selections automatically appear on the page
        EXPECTED: All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        """
        market_appears = self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(
            item_name=self.extra_time_result_market)
        self.assertTrue(market_appears, msg=f'Market "{self.extra_time_result_market}" does not appear')

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No Markets are present')

        extra_time_market = markets.get(self.extra_time_result_market)
        self.assertTrue(extra_time_market,
                        msg=f'Market "{self.extra_time_result_market}" is not found in "{markets.keys()}"')
        self.assertTrue(extra_time_market.is_expanded(),
                        msg=f'Market "{self.extra_time_result_market}" is not expanded')
        result = wait_for_result(lambda: len(extra_time_market.outcomes.items_as_ordered_dict) == len(self.selection_ids),
                                 name='All selections to display',
                                 timeout=10)
        self.assertTrue(result,
                        msg=f'Displayed "{len(extra_time_market.outcomes.items_as_ordered_dict)}" selections, '
                        f'but should "{len(self.selection_ids)}"')
        selections = extra_time_market.outcomes.items_as_ordered_dict
        expected_selections = [selection.upper() for selection in self.selection_ids.keys()] if self.brand == 'ladbrokes' else self.selection_ids.keys()
        self.assertListEqual(sorted(selections.keys()), sorted(expected_selections),
                             msg=f'List of "{sorted(selections.keys())}" is not equal to expected "{sorted(expected_selections)}"')

        match_result = markets.get(self.expected_market_sections.match_result)
        self.assertTrue(match_result,
                        msg=f'"{self.expected_market_sections.match_result}" section is not found in "{markets.keys()}"')
        self.assertTrue(match_result.is_expanded(),
                        msg=f'"{self.expected_market_sections.match_result}" market is not collapsed')

        markets.get(self.extra_time_result_market).collapse()
        self.assertFalse(markets.get(self.extra_time_result_market).is_expanded(expected_result=False),
                         msg='Extra time market is not collapsed after click')

        tab_appears = self.site.sport_event_details.markets_tabs_list.wait_item_appears(
            item_name=self.expected_market_tabs.autotest_collection)
        self.assertTrue(tab_appears, msg=f'Tab "{self.expected_market_tabs.autotest_collection}" does not appear')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.autotest_collection)

        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.autotest_collection,
                         msg=f'Autotest Collection is not active tab after click, active tab is "{current_tab}"')

        market_appears = self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(
            item_name=self.extra_time_result_market)
        self.assertTrue(market_appears,
                        msg=f'Market "{self.extra_time_result_market}" does not appear')

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        extra_time_market = markets.get(self.extra_time_result_market)
        self.assertTrue(extra_time_market.is_expanded(),
                        msg=f'Market "{self.extra_time_result_market}" is not expanded')
        selections = extra_time_market.outcomes.items_as_ordered_dict
        self.assertEqual(sorted(selections.keys()), sorted(expected_selections))

    # fixme: disabled as corresponding issue BMA-26449 is not fixed for two years
    # def test_007_in_ti_tool_create_undisplayed_market_of_sport_event_add_displayed_selection_to_it_display_all(self):
    #     """
    #     DESCRIPTION: In TI tool: Create undisplayed market of <Sport> event > add undisplayed selection to it > then display all`
    #     EXPECTED: Selection is added to an undisplayed market of a <Sport> event
    #     """
    #     selections, markets = self.ob_config.add_custom_markets_with_selections(event_id=self.eventID,
    #                                                                             markets=[(self.scorecast_market_name, {'cashout': True})],
    #                                                                             class_id=self.ob_config.football_config.autotest_class.class_id,
    #                                                                             category_id=self.ob_config.football_config.category_id,
    #                                                                             type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
    #                                                                             market_displayed=False,
    #                                                                             selections_displayed=False,
    #                                                                             team1=self.team1,
    #                                                                             team2=self.team2)
    #
    #     [self.ob_config.change_market_state(event_id=self.eventID, market_id=market_id, displayed=True, active=True)
    #      for market_name, market_id in markets.items()]
    #
    #     [[self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)
    #       for selection_name, selection_id in market_selections.items()]
    #      for market_name, market_selections in selections.items()]
    #
    # def test_008_in_application_verify_opened_event_details_page_of_sport_event(self):
    #     """
    #     DESCRIPTION: In application: Verify opened Event Details page of <Sport> event
    #     EXPECTED: - Displayed market with selections automatically appear on the page
    #     EXPECTED: - All other markets are displayed in their actual state (expanded or collapsed)
    #     EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
    #     EXPECTED: - If order of newly created market is < 2, the market is shown expanded
    #     """
    #     market_appears = self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(
    #         item_name=self.expected_market_sections.scorecast)
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

    # fixme: disabled as corresponding story BMA-26771 won't be implemented
    # def test_009_verify_newly_added_yourcall_collection_markets(self):
    #     """
    #     DESCRIPTION: In TI tool: Create undisplayed YourCall market of <Sport> event > add undisplayed selection to it > then display all
    #     EXPECTED: Selection is added to an undisplayed market of a <Sport> event
    #     """
    #     selections, markets = self.ob_config.add_custom_markets_with_selections(
    #         event_id=self.eventID,
    #         markets=[('your_call',)],
    #         class_id=self.ob_config.football_config.autotest_class.class_id,
    #         category_id=self.ob_config.football_config.category_id,
    #         type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
    #         market_displayed=False,
    #         selections_displayed=False,
    #         team1=self.team1,
    #         team2=self.team2)
    #
    #     [self.ob_config.change_market_state(event_id=self.eventID, market_id=market_id, displayed=True, active=True)
    #      for market_name, market_id in markets.items()]
    #
    #     [[self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)
    #       for selection_name, selection_id in market_selections.items()]
    #      for market_name, market_selections in selections.items()]
    #
    #     self.__class__.selection_ids = selections['your_call']
    #
    #     tab_appears = self.site.sport_event_details.markets_tabs_list.wait_item_appears(item_name=self.expected_market_tabs.yourcall)
    #     self.assertTrue(tab_appears, msg='Tab %s does not appear' % self.expected_market_tabs.yourcall)
    #
    # def test_010_verify_newly_added_yourcall_markets(self):
    #     """
    #     DESCRIPTION: Verify newly added #YourCall markets
    #     EXPECTED: Markets are displayed with selections in corresponding collections
    #     EXPECTED: If new market belongs to a new collection, the collection automatically appears along with the market
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
    # def test_011_repeat_previous_step_on_collections_tab(self):
    #     """
    #     DESCRIPTION:Repeat previous step on #YourCall collections tab
    #     """
    #     self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.yourcall)
    #     current_tab = self.site.sport_event_details.markets_tabs_list.current
    #     self.assertEqual(current_tab, self.expected_market_tabs.yourcall,
    #                      msg='All Markets is not active tab after click, active tab is %s' % current_tab)
    #     self.test_010_verify_newly_added_yourcall_markets()
