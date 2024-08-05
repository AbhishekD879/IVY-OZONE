import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.environments.constants.base.markets_abbreviation import MarketAbbreviation
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.sports_specific
@pytest.mark.Rugby_league_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C66007751_Verify_data_displayed_under_Competitions_tab_for_Rugby_League_Sports(BaseBetSlipTest):
    """
    TR_ID: C66007751
    NAME: Verify data displayed under Competitions tab for Rugby League Sports.
    DESCRIPTION: This test case validates the data displayed under the Competitions tab for Rugby League Sport.
    PRECONDITIONS: In CMS, Sport pages-&gt; Sport Categories-&gt; Rugby league sport -&gt;tabs and modules should be configured.
    PRECONDITIONS: Market switcher should be enabled in System Config -&gt; Structure -&gt; Market Switcher.
    PRECONDITIONS: Two Aggregated Markets should be added to Market Switcher label table on below path in CMS.
    PRECONDITIONS: Sports categories -&gt; Sport pages  -&gt; Rugby League -&gt; Competitions -&gt; Market switcher Label section
    PRECONDITIONS: Config below 2 way markets as aggregated Market with display name "Game Lines"
    PRECONDITIONS: Moneyline, Handicap, Total Points(2 way markets which has 2 selections)
    PRECONDITIONS: Config below 2 way markets as aggregated Market with display name "Game Lines 3-Way"
    PRECONDITIONS: Moneyline 3-way, Handicap way, Total Points 3-way(3 way markets which has 3 selections)
    PRECONDITIONS: Note: Market aggregation should be done for either 2 way or 3-way markets only.
    """
    keep_browser_open = True
    sport_name = "rugbyleague"
    rugby_league_Category_id = 30
    competitions_tab = vec.sb.TABS_NAME_COMPETITIONS.title()
    aggregated_markets = ['Game Lines', 'Game Lines 3 Way']

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header2=None, header3=None,
                                                     aggregated=None, markets_qty=None):
        current_page = self.site.competition_league
        items = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        market_abbr = MarketAbbreviation.FIXTURE_HEADERS_MARKETS_ABBREVIATION
        cms_header1 = market_abbr.get(header1.lower().replace(' ', ''), None)
        header1 = [header1.upper(), cms_header1.upper()] if cms_header1 != None else [header1.upper()]
        self.assertIn(event.header1.upper(), header1,
                      msg=f'Actual fixture header "{event.header1}" does not equal to'
                          f'Expected "{header1}"')
        if header2:
            cms_header2 = market_abbr.get(header2.lower().replace(' ', ''), None)
            header2 = [header2.upper(), cms_header2.upper()] if cms_header2 != None else [header2.upper()]
            self.assertIn(event.header2.upper(), header2,
                          msg=f'Actual fixture header "{event.header2}" does not equal to'
                              f'Expected "{header2}"')
        cms_header3 = market_abbr.get(header3.lower().replace(' ', ''), None)
        header3 = [header3.upper(), cms_header3.upper()] if cms_header3 != None else [header3.upper()]
        self.assertIn(event.header3.upper(), header3,
                      msg=f'Actual fixture header "{event.header2}" does not equal to'
                          f'Expected "{header3}"')
        if aggregated:
            markets_count = list(events)[0].aggregated_template.get_aggregated_markets_count
            self.assertEqual(markets_count, markets_qty, f'Actual Number of Aggregate Markets is "{markets_count}"'
                                                         f'is not same as Expected Number of Aggregated Markets "{markets_qty}"')
        else:
            bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
            self.assertEqual(bet_buttons, bet_button_qty,
                             msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                                 f'Expected Buttons: "{bet_button_qty}".')

    def choose_events_for_aggregate_markets(self):
        sections = list(self.site.sports_page.tab_content.tt_competitions_categories_list.items_as_ordered_dict.values())
        event_objects = list()
        for section in sections:
            if not section.is_expanded():
                section.expand()
            for event in list(section.items_as_ordered_dict.values()):
                event_objects.append(event)
        return event_objects

    def select_active_events(self, all_events,
                             index_of_market):  # selecting two active events for aggregated markets to place multiple bet
        event1 = None
        event2 = None
        for event in all_events:
            market_section_objects = event.aggregated_template.get_market_sections
            bet_buttons = [button for button_name, button in
                           market_section_objects[index_of_market].get_bet_buttons.items() if
                           button_name.upper() not in ['N/A', 'SUSP']]
            if len(bet_buttons) == 0:
                continue
            else:
                if event1 == None:
                    event1 = event
                else:
                    event2 = event
                    break
        return [event1, event2]

    def click_random_bet_button(self, event, aggregated=False, index_of_market=None):
        if aggregated:
            market_section_objects = event.aggregated_template.get_market_sections
            bet_button_objects = list(market_section_objects[index_of_market].get_bet_buttons.values())
        else:
            bet_button_objects = list(event.template.get_available_prices().values())
        bet_button = next((button for button in bet_button_objects if
                           button.name.upper() not in ['N/A', 'SUSP']), None)  # getting active bet buttons
        bet_button.click()

    def verify_bet_placement(self, market, aggregated=False, market_names=[]):
        if aggregated:
            all_events = self.choose_events_for_aggregate_markets()
            # to place single bet, quick bet, multiple bet in every market for each aggregated market
            for index in range(len(market_names)):
                event1, event2 = self.select_active_events(all_events=all_events, index_of_market=index)

                # placing_single_bet
                if event1 != None:
                    self.click_random_bet_button(event1, aggregated=aggregated, index_of_market=index)
                    if self.device_type == 'mobile':
                        self.site.add_first_selection_from_quick_bet_to_betslip()
                    self.site.open_betslip()
                    self.place_single_bet()
                    self.check_bet_receipt_is_displayed()
                    self.site.close_betreceipt()
                else:
                    self._logger.info(f'there is no events for "{market_names[index]}"')
                    continue

                # placing multiple bet
                if event2 == None:
                    self._logger.info(f'there is no events for "{market_names[index]} to place multiple bet"')
                    continue
                self.click_random_bet_button(event1, aggregated=aggregated, index_of_market=index)
                if self.device_type == 'mobile':
                    self.site.add_first_selection_from_quick_bet_to_betslip()
                self.click_random_bet_button(event2, aggregated=aggregated, index_of_market=index)
                self.site.open_betslip()
                self.place_multiple_bet(number_of_stakes=1)
                self.check_bet_receipt_is_displayed()
                self.site.close_betreceipt()
            return

    def test_000_preconditions(self):
        """
        DESCRIPTION : Verifying competitions tab in enable or disable in cms
        DESCRIPTION : checking whether market switcher is enabled or disable for competitions tab.
        DESCRIPTION :
        """
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name=self.sport_name, status=True)
        self.assertTrue(status, msg=f'The sport "rugby_league" is not checked')
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')

        self.__class__.competition_tab_enabled = self.cms_config.get_sport_tab_status(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.rugby_league_config.category_id)

        self.competition_tab_data = self.cms_config.get_sports_tab_data(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.rugby_league_config.category_id)

        is_market_switcher_enabled = self.cms_config.get_system_configuration_item('MarketSwitcher').get('rugbyleague')

        if not is_market_switcher_enabled:
            raise CmsClientException('Market Switcher is Not Enabled for rugby_league')

        self.__class__.cms_markets = self.competition_tab_data.get('marketsNames', None)

        if not self.__class__.cms_markets:
            raise CmsClientException('No One Market added for Market Switcher')

        self.__class__.expected_display_names = list()
        self.__class__.expected_none_aggregated_market_names = list()
        self.__class__.expected_aggregate_market_names = list()

        for market in self.__class__.cms_markets:
            self.expected_display_names.append(market.get('title').strip().title())
            self.expected_aggregate_market_names.append(market.get('title').strip().title()) if ',' in market.get(
                'templateMarketName') else self.expected_none_aggregated_market_names.append(
                market.get('title').strip().title())

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        self.site.login()
        self.navigate_to_page(name='sport/rugby-league')
        self.site.wait_content_state('rugby-league')

    def test_002_navigate_to_rugby_league__ampgt_competitions_tab(self):
        """
        DESCRIPTION: Navigate to Rugby League -&amp;gt; Competitions tab
        EXPECTED: Navigation should be successful.
        EXPECTED: Data should be displayed in Competitions tab
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.rugby_league_config.category_id)
        tabs = self.site.contents.tabs_menu.items_as_ordered_dict
        if expected_tab_name not in tabs and not self.competition_tab_enabled:
            raise CmsClientException('competitions tab is not enabled')
        self.assertIn(expected_tab_name, list(tabs.keys()), f'expected tab {expected_tab_name} is not in {tabs}')
        tabs.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.click_button(expected_tab_name).click()
            current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab_name, msg=f'Actual tab: "{current_tab_name}" is not same as '
                                                                  f'Expected tab: "{expected_tab_name}"')

    def test_003_verify__market_switcher(self):
        """
        DESCRIPTION: Verify  Market Switcher.
        EXPECTED: If the aggregated market "Game Lines" is on top in market switcher label table, then it should be selected by default.
        EXPECTED: If Game Lines selected by default then aggregated markets should display on event card.
        """
        self.__class__.dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown arrow" is not expanded')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.dropdown.click()
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.assertTrue(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downward')
        # selecting aggregated market from market selector in competitions tab
        markets = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        for market_name, market in markets.items():
            if market_name.title() in self.expected_aggregate_market_names:
                market.click()
                # checking template names is similar to which we configure in cms for aggregated markets
                if market_name.title() in self.expected_aggregate_market_names:
                    self.__class__.fixture_markets = next((cms_market.get('templateMarketName') for cms_market in self.cms_markets if
                                            cms_market.get('title').title() == market_name.title()), None).upper().split(',')
                    if len(self.fixture_markets) == 2:
                        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=0,
                                                                          header1=self.fixture_markets[0],
                                                                          header3=self.fixture_markets[1],
                                                                          header2=None,
                                                                          aggregated=True,
                                                                          markets_qty=2)
                    else:
                        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=0,
                                                                          header1=self.fixture_markets[0],
                                                                          header2=self.fixture_markets[1],
                                                                          header3=self.fixture_markets[2],
                                                                          aggregated=True,
                                                                          markets_qty=3)

    def test_004_verify_aggregated_market_view_on_event_card(self):
        """
        DESCRIPTION: Verify Aggregated Market view on event card.
        EXPECTED: Aggregated markets odds will be shown in same order which we set in Market switcher label table.
        EXPECTED: Markets names should be wrapped to second line (no more than 2 lines, any market that is longer than 2 lines we should use ellipses '...' and on mouse hovering it should display full name. for mobiles by clicking on market name it should display full name of markets.
        EXPECTED: For below Markets respective abbreviation should show in SLP not in edp markets.
        EXPECTED: No Draw Handicap 1    --&amp;gt; No Draw Hcap 1
        EXPECTED: No Draw Handicap 2    --&amp;gt; No Draw Hcap 2
        EXPECTED: No Draw Handicap 3    --&amp;gt; No Draw Hcap 3
        EXPECTED: Total Match Points    --&amp;gt; Total Points
        EXPECTED: Handicap Betting  --&amp;gt; Hcap
        EXPECTED: Handicap 2-way    --&amp;gt; Hcap 2-way
        EXPECTED: If we set Aggregated markets as Moneyline, Handicap, Total Points in MS label table then first money line markets odds should display then Handicap market followed by Total points.
        EXPECTED: For total points market if we have more markets i.e. Total points over and Under 5 and Total Points over and under 6 then Total Points over and Under 5 market selections should show on event card with aggregated view.
        EXPECTED: For Total points over and under markets selections "O" should shown in Selection button prior to Over value selection and "U" for under selection.
        """
        #  covered in test_003_verify__market_switcher step

    def test_005_click_on_market_switcher(self):
        """
        DESCRIPTION: Click on Market Switcher.
        EXPECTED: Markets which are configured in market switcher labels table should display if we have events with configured markets.
        EXPECTED: If we don't have any single event with configured markets, that specific market shouldn't be shown in market switcher dropdown.
        """
        options = self.site.sports_page.tab_content.dropdown_market_selector
        self.__class__.actual_list = list(options.items_as_ordered_dict.keys())
        # if actual_list is empty, fetching the value again from the UI
        if self.actual_list == ['']:
            self.actual_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        # comparing UI markets are in expected list or not
        for market in self.actual_list:
            self.assertIn(market.title(), self.expected_display_names,
                          msg=f'Actual Market: "{market}" is not present in the '
                              f'Expected Markets list:"{self.expected_display_names}"')

    def test_006_verify_game_lines_3_way_on_market_switcher(self):
        """
        DESCRIPTION: Verify Game Lines 3-way on Market Switcher.
        EXPECTED: Result should be same step no 4.
        EXPECTED: For Game Lines 3-Way 3 odds should be shown.
        """
        #  covered in test_003_verify__market_switcher step

    def test_007_verify_other_markets_on_market_switcher(self):
        """
        DESCRIPTION: Verify other markets on Market Switcher.
        EXPECTED: Events should load with selected markets.
        """
        markets = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        for market_name, market in markets.items():
            if market_name.title() in self.expected_none_aggregated_market_names:
                market.click()
                accordions = self.site.sports_page.tab_content.tt_competitions_categories_list.items_as_ordered_dict
                for accordion_name, accordion in accordions.items():
                    if not accordion.is_expanded():
                        accordion.expand()
                    first_event_name, first_event = accordion.first_item
                    event_id = first_event.template.event_id
                    markets = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0].get('event').get('children')
                    for market in markets:
                        market = market.get('market').get('templateMarketName')
                        if market.replace('|', '') == market_name:
                            self.assertTrue(market.replace('|', ''), msg=f'market is same as not related to selected market {market_name}')
                            break

    def test_008_switch_between_two_aggregated_markets_simultaneously(self):
        """
        DESCRIPTION: Switch between two aggregated markets simultaneously.
        EXPECTED: Respect market odds should load properly without page refresh.
        """
        # covered in test_003_verify__market_switcher

    def test_009_verify_multiple_types_of_bet_placements_on_game_lines_and_game_lines_3_way_marketseg_single_double_acca_etc(self):
        """
        DESCRIPTION: Verify multiple types of bet placements on Game Lines and Game Lines 3-way markets.
        DESCRIPTION: e.g. Single, double, Acca etc.
        EXPECTED: Bets should be placed successfully.
        """
        self.navigate_to_page('sport/rugby-league/competitions')
        wait_for_haul(5)
        markets = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        for market_name, market in markets.items():
            if market_name.title() in self.expected_aggregate_market_names and market_name.title() in self.aggregated_markets:
                market.click()
                # placing bet for aggregated markets
                self.verify_bet_placement(market=market_name, aggregated=True, market_names=self.fixture_markets)